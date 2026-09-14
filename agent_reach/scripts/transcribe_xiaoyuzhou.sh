#!/bin/bash
# Xiaoyuzhou podcast yazıya dökme betiği
# Kullanım: bash transcribe.sh [--polish] <Xiaoyuzhou bağlantısı> [çıktı dosyası yolu]
# Ortam değişkeni: GROQ_API_KEY (zorunlu)
#
# --polish: yazıya dökmeden sonra Groq Llama 3.3 70B ile metne Çince noktalama + makul paragraflar ekler
#           (Whisper Çince noktalamada zayıftır; açıkken metin çok daha rahat okunur)

set -e

POLISH=0
while [ $# -gt 0 ]; do
    case "$1" in
        --polish) POLISH=1; shift ;;
        --) shift; break ;;
        -h|--help)
            echo "Kullanım: bash transcribe.sh [--polish] <Xiaoyuzhou bağlantısı> [çıktı dosyası yolu]"
            exit 0 ;;
        --*)
            echo "Bilinmeyen seçenek: $1" >&2
            exit 1 ;;
        *) break ;;
    esac
done

URL="${1:?Kullanım: bash transcribe.sh [--polish] <Xiaoyuzhou bağlantısı> [çıktı dosyası yolu]}"
OUTPUT="${2:-}"

PYTHON_CMD=()
ensure_python() {
    if [ "${#PYTHON_CMD[@]}" -gt 0 ]; then
        return 0
    fi
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_CMD=(python3)
    elif command -v python >/dev/null 2>&1; then
        PYTHON_CMD=(python)
    elif command -v py >/dev/null 2>&1; then
        PYTHON_CMD=(py -3)
    else
        echo "❌ Python bulunamadı (denenenler: python3, python, py -3)" >&2
        return 1
    fi
}

ensure_python || exit 1
if ! XIAOYUZHOU_URL="$URL" "${PYTHON_CMD[@]}" <<'PY'
import os
from urllib.parse import urlsplit

try:
    parsed = urlsplit(os.environ["XIAOYUZHOU_URL"])
    hostname = (parsed.hostname or "").lower()
except ValueError:
    raise SystemExit(1)

allowed_host = (
    hostname == "xiaoyuzhoufm.com"
    or hostname.endswith(".xiaoyuzhoufm.com")
)
raise SystemExit(0 if parsed.scheme.lower() in {"http", "https"} and allowed_host else 1)
PY
then
    echo "❌ Yalnızca xiaoyuzhoufm.com ve alt alan adlarının http/https bağlantıları desteklenir" >&2
    exit 1
fi

# Try env var first, then agent-reach config.yaml
if [ -z "$GROQ_API_KEY" ]; then
    CONFIG_FILE="$HOME/.agent-reach/config.yaml"
    if [ -f "$CONFIG_FILE" ]; then
        ensure_python || exit 1
        CONFIG_FOR_PYTHON="$CONFIG_FILE"
        if command -v cygpath >/dev/null 2>&1; then
            CONFIG_FOR_PYTHON=$(cygpath -w "$CONFIG_FILE")
        fi
        GROQ_API_KEY=$(AGENT_REACH_CONFIG_FILE="$CONFIG_FOR_PYTHON" \
            "${PYTHON_CMD[@]}" -c 'import os, yaml; print((yaml.safe_load(open(os.environ["AGENT_REACH_CONFIG_FILE"])) or {}).get("groq_api_key", ""))' \
            2>/dev/null || true)
    fi
fi
GROQ_API_KEY="${GROQ_API_KEY:?GROQ_API_KEY ortam değişkenini ayarla veya agent-reach configure groq-key çalıştır}"

# Groq API limiti: dosya başına 25MB
MAX_CHUNK_SIZE_MB=20
AUDIO_BITRATE="64k"
CURL_CONNECT_TIMEOUT=15
PAGE_TIMEOUT=60
AUDIO_TIMEOUT=1800
GROQ_TIMEOUT=600
MAX_PAGE_BYTES=5242880
MAX_AUDIO_BYTES=1073741824
MAX_API_RESPONSE_BYTES=33554432
MAX_DURATION_SECONDS=10800

TEMP_ROOT="${TMPDIR:-/tmp}"
if ! WORK_DIR=$(mktemp -d "${TEMP_ROOT%/}/agent-reach-xiaoyuzhou.XXXXXX"); then
    echo "❌ Geçici klasör oluşturulamadı" >&2
    exit 1
fi

cleanup() {
    rm -rf -- "$WORK_DIR"
}
trap cleanup EXIT

echo "📻 Xiaoyuzhou podcast yazıya dökme"
echo "===================="

# Step 1: ses URL'si ve başlığı çıkar
echo "🔍 Sayfa ayrıştırılıyor..."
PAGE=$(curl --fail --show-error --location --silent \
    --connect-timeout "$CURL_CONNECT_TIMEOUT" \
    --max-time "$PAGE_TIMEOUT" \
    --max-filesize "$MAX_PAGE_BYTES" \
    "$URL")
AUDIO_URL=$(echo "$PAGE" | perl -ne 'while (/(https:\/\/media\.xyzcdn\.net\/[^"]*\.(?:m4a|mp3))/gi) { print "$1\n" }' | head -1)
TITLE=$(echo "$PAGE" | perl -ne 'if (/"title":"([^"]*)"/) { print "$1\n"; last }' | head -1)

if [ -z "$AUDIO_URL" ]; then
    echo "❌ Sayfadan ses bağlantısı çıkarılamadı"
    exit 1
fi

echo "📝 Başlık: $TITLE"
echo "🔗 Ses: $AUDIO_URL"

# Step 2: sesi indir
echo "⬇️  Ses indiriliyor..."
EXT="${AUDIO_URL##*.}"
curl --fail --show-error --location --silent \
    --connect-timeout "$CURL_CONNECT_TIMEOUT" \
    --max-time "$AUDIO_TIMEOUT" \
    --max-filesize "$MAX_AUDIO_BYTES" \
    -o "$WORK_DIR/original.$EXT" \
    "$AUDIO_URL"
FILE_SIZE=$(ls -lh "$WORK_DIR/original.$EXT" | awk '{print $5}')
echo "📦 Dosya boyutu: $FILE_SIZE"

# Step 3: süreyi al
if ! DURATION_RAW=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 \
    "$WORK_DIR/original.$EXT" 2>/dev/null); then
    echo "❌ ffprobe ses süresini okuyamadı" >&2
    exit 1
fi
if DURATION=$(DURATION_RAW="$DURATION_RAW" MAX_DURATION_SECONDS="$MAX_DURATION_SECONDS" \
    "${PYTHON_CMD[@]}" -c '
import os
import sys
from decimal import Decimal, InvalidOperation

raw = os.environ["DURATION_RAW"]
try:
    value = Decimal(raw)
except InvalidOperation:
    raise SystemExit(2)
if not value.is_finite() or value < 0:
    raise SystemExit(2)
if value > Decimal(os.environ["MAX_DURATION_SECONDS"]):
    raise SystemExit(3)
print(int(value))
'); then
    :
else
    duration_status=$?
    if [ "$duration_status" -eq 3 ]; then
        echo "❌ Ses süresi 3 saatlik limiti aşıyor" >&2
    else
        echo "❌ ffprobe geçersiz ses süresi döndürdü: ${DURATION_RAW:-<empty>}" >&2
    fi
    exit 1
fi
DURATION_MIN=$((DURATION / 60))
DURATION_SEC=$((DURATION % 60))
echo "⏱️  Süre: ${DURATION_MIN} dk ${DURATION_SEC} sn"

# Step 4: düşük bit hızlı mono MP3'e dönüştür
echo "🔄 Dönüştürülüyor..."
ffmpeg -y -i "$WORK_DIR/original.$EXT" -t "$MAX_DURATION_SECONDS" -b:a "$AUDIO_BITRATE" -ac 1 "$WORK_DIR/mono.mp3" 2>/dev/null
MONO_SIZE=$(stat -c%s "$WORK_DIR/mono.mp3" 2>/dev/null || stat -f%z "$WORK_DIR/mono.mp3")
MONO_SIZE_MB=$(awk -v bytes="$MONO_SIZE" 'BEGIN { printf "%.1f", bytes / 1024 / 1024 }')
echo "📦 Dönüştürme sonrası: ${MONO_SIZE_MB}MB"

# Step 5: boyuta göre parçala
MAX_BYTES=$((MAX_CHUNK_SIZE_MB * 1024 * 1024))

if [ "$MONO_SIZE" -le "$MAX_BYTES" ]; then
    # Parçalamaya gerek yok
    cp "$WORK_DIR/mono.mp3" "$WORK_DIR/chunk_0.mp3"
    NUM_CHUNKS=1
    echo "📎 Parçalamaya gerek yok"
else
    # Kaç chunk gerektiğini hesapla
    NUM_CHUNKS=$(( (MONO_SIZE / MAX_BYTES) + 1 ))
    CHUNK_DURATION=$(( DURATION / NUM_CHUNKS + 10 ))  # 10 sn tampon ekle
    echo "✂️  $NUM_CHUNKS parçaya bölünüyor (parça başına yaklaşık $((CHUNK_DURATION / 60)) dk)..."
    
    for i in $(seq 0 $((NUM_CHUNKS - 1))); do
        START=$((i * CHUNK_DURATION))
        ffmpeg -y -i "$WORK_DIR/mono.mp3" -ss "$START" -t "$CHUNK_DURATION" -c copy "$WORK_DIR/chunk_${i}.mp3" 2>/dev/null
        CHUNK_SIZE=$(ls -lh "$WORK_DIR/chunk_${i}.mp3" | awk '{print $5}')
        echo "   Parça $((i+1))/$NUM_CHUNKS: $CHUNK_SIZE"
    done
fi

# Step 6: Groq Whisper API ile yazıya dök
# Not: Whisper prompt'u bilerek Çince bırakıldı; ses Çince (Mandarin) olduğu için
# modele Çince noktalama üretmesini bu şekilde söylemek daha iyi sonuç verir.
echo "🎙️  Yazıya dökülüyor (Groq Whisper large-v3)..."

for i in $(seq 0 $((NUM_CHUNKS - 1))); do
    echo -n "   Parça $((i+1))/$NUM_CHUNKS... "
    
    RESPONSE=$(curl --silent --show-error \
        --connect-timeout "$CURL_CONNECT_TIMEOUT" \
        --max-time "$GROQ_TIMEOUT" \
        --max-filesize "$MAX_API_RESPONSE_BYTES" \
        -w "\n%{http_code}" \
        https://api.groq.com/openai/v1/audio/transcriptions \
        -H "Authorization: Bearer $GROQ_API_KEY" \
        -F file="@$WORK_DIR/chunk_${i}.mp3" \
        -F model="whisper-large-v3" \
        -F language="zh" \
        -F prompt="以下是一段中文普通话播客录音，请输出包含完整中文标点（，。？！：；“”‘’）的转写文本。" \
        -F response_format="text")
    
    HTTP_CODE=$(echo "$RESPONSE" | tail -1)
    BODY=$(echo "$RESPONSE" | sed '$d')
    
    if [ "$HTTP_CODE" != "200" ]; then
        echo "❌ API hatası (HTTP $HTTP_CODE)"
        echo "$BODY"
        
        # Hız limitiyse bekleyip yeniden dene
        if [ "$HTTP_CODE" = "429" ]; then
            # Bekleme süresini hata mesajından çıkar, varsayılan 120 sn
            WAIT_SEC=$(echo "$BODY" | perl -ne 'if (/in (\d+)m/) { print "$1\n"; exit }')
            WAIT_SEC=${WAIT_SEC:-2}
            WAIT_SEC=$((WAIT_SEC * 60 + 30))
            if [ "$WAIT_SEC" -gt 900 ]; then
                WAIT_SEC=900
            fi
            echo "   ⏳ Hız limiti, ${WAIT_SEC} sn bekleyip yeniden deneniyor..."
            sleep "$WAIT_SEC"
            RESPONSE=$(curl --silent --show-error \
                --connect-timeout "$CURL_CONNECT_TIMEOUT" \
                --max-time "$GROQ_TIMEOUT" \
                --max-filesize "$MAX_API_RESPONSE_BYTES" \
                -w "\n%{http_code}" \
                https://api.groq.com/openai/v1/audio/transcriptions \
                -H "Authorization: Bearer $GROQ_API_KEY" \
                -F file="@$WORK_DIR/chunk_${i}.mp3" \
                -F model="whisper-large-v3" \
                -F language="zh" \
                -F prompt="以下是一段中文普通话播客录音，请输出包含完整中文标点（，。？！：；“”‘’）的转写文本。" \
                -F response_format="text")
            HTTP_CODE=$(echo "$RESPONSE" | tail -1)
            BODY=$(echo "$RESPONSE" | sed '$d')
            
            if [ "$HTTP_CODE" != "200" ]; then
                echo "   ❌ Yeniden deneme başarısız"
                exit 1
            fi
        else
            case "$HTTP_CODE" in
                5??)
                    echo "   Yedek olarak deneyebilirsin: agent-reach transcribe \"$AUDIO_URL\""
                    ;;
            esac
            exit 1
        fi
    fi
    
    echo "$BODY" > "$WORK_DIR/transcript_${i}.txt"
    CHARS=$(wc -m < "$WORK_DIR/transcript_${i}.txt")
    echo "✅ ($CHARS karakter)"
done

# Step 6.5 (isteğe bağlı): Llama 3.3 70B ile metne noktalama + paragraf ekle
if [ "$POLISH" = "1" ]; then
    ensure_python || exit 1
    echo "✨ Düzenleniyor (Llama 3.3 70B noktalama + paragraf)..."
    for i in $(seq 0 $((NUM_CHUNKS - 1))); do
        echo -n "   Parça $((i+1))/$NUM_CHUNKS... "
        IN_FILE="$WORK_DIR/transcript_${i}.txt" \
        OUT_FILE="$WORK_DIR/polished_${i}.txt" \
        GROQ_API_KEY="$GROQ_API_KEY" \
        "${PYTHON_CMD[@]}" <<'PY'
import json, os, sys, urllib.request, urllib.error

KEY = os.environ["GROQ_API_KEY"]
IN = os.environ["IN_FILE"]
OUT = os.environ["OUT_FILE"]

MODEL = "llama-3.3-70b-versatile"
MAX_DEPTH = 3
# Intentionally Chinese: the transcript is Mandarin and the model must only add
# Chinese punctuation, so the instruction stays in the transcript's language.
PROMPT_TMPL = (
    "以下是一段中文普通话播客的语音转写片段，由于 Whisper 对中文标点支持较弱，"
    "整段几乎没有标点。请你**只做一件事**：在合适位置补充中文标点（，。！？：；），"
    "可以适度分段。\n\n"
    "**严格要求**：\n"
    "- 不得修改、删除、增加任何汉字或英文/数字\n"
    "- 不得改写、润色、总结\n"
    "- 不得添加任何解释、前言、后记\n"
    "- 直接输出加好标点+合理分段后的全文\n\n"
    "原文：\n{}"
)

def call_groq(text):
    body = json.dumps({
        "model": MODEL,
        "temperature": 0.2,
        "max_completion_tokens": 8192,
        "messages": [{"role": "user", "content": PROMPT_TMPL.format(text)}],
    }).encode()
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {KEY}",
            "Content-Type": "application/json",
            "User-Agent": "agent-reach-xiaoyuzhou/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        payload = r.read(32 * 1024 * 1024 + 1)
    if len(payload) > 32 * 1024 * 1024:
        raise ValueError("polish response exceeds 32 MiB limit")
    resp = json.loads(payload)
    return (
        resp["choices"][0]["message"]["content"].strip(),
        resp["choices"][0].get("finish_reason"),
    )

def polish(text, depth=0):
    try:
        out, fr = call_groq(text)
    except urllib.error.HTTPError as e:
        sys.stderr.write(f"polish HTTP {e.code}: {e.read().decode(errors='replace')[:200]}\n")
        return text  # fallback to raw
    except Exception as e:
        sys.stderr.write(f"polish error: {e}\n")
        return text
    if fr != "length" or depth >= MAX_DEPTH:
        return out
    # Çıktı kesildi: metni ortadan ikiye bölüp özyinelemeli işle
    mid = len(text) // 2
    return polish(text[:mid], depth + 1) + polish(text[mid:], depth + 1)

content = open(IN, encoding="utf-8").read().strip()
result = polish(content)
open(OUT, "w", encoding="utf-8").write(result + "\n")
print(f"✅ ({len(result)} karakter)")
PY
    done
fi

# Step 7: çıktıyı birleştir
echo "📄 Metin birleştiriliyor..."

if [ -z "$OUTPUT" ]; then
    if ! OUTPUT=$(mktemp "${TEMP_ROOT%/}/agent-reach-transcript.XXXXXX"); then
        echo "❌ Çıktı dosyası güvenle oluşturulamadı" >&2
        exit 1
    fi
fi

{
    echo "# $TITLE"
    echo ""
    echo "Kaynak: $URL"
    echo "Süre: ${DURATION_MIN} dk ${DURATION_SEC} sn"
    echo "Yazıya dökme zamanı: $(date '+%Y-%m-%d %H:%M')"
    if [ "$POLISH" = "1" ]; then
        echo "Düzenleme: Groq Llama 3.3 70B"
    fi
    echo ""
    echo "---"
    echo ""

    for i in $(seq 0 $((NUM_CHUNKS - 1))); do
        if [ "$POLISH" = "1" ] && [ -f "$WORK_DIR/polished_${i}.txt" ]; then
            cat "$WORK_DIR/polished_${i}.txt"
        else
            cat "$WORK_DIR/transcript_${i}.txt"
        fi
        echo ""
    done
} > "$OUTPUT"

TOTAL_CHARS=$(wc -m < "$OUTPUT")
echo ""
echo "✅ Tamamlandı!"
echo "📄 Çıktı: $OUTPUT"
echo "📊 Toplam karakter: $TOTAL_CHARS"
echo "===================="
