# Video ve podcast

YouTube, Bilibili ve Xiaoyuzhou podcast'leri için altyazı ve transkript.

## YouTube (yt-dlp)

### Video meta verilerini al

```bash
yt-dlp --dump-json "URL"
```

### Altyazı indir

```bash
# Altyazıyı indir (videoyu indirmeden). Türkçe altyazı için dil listesine "tr" ekle.
yt-dlp --write-sub --write-auto-sub --sub-lang "zh-Hans,zh,en" --skip-download -o "/tmp/%(id)s" "URL"

# Sonra .vtt dosyasını oku
cat /tmp/VIDEO_ID.*.vtt
```

> Windows'ta `/tmp/` yerine `$env:TEMP` kullan, `cat` yerine `Get-Content` çalışır.

### Yorumları al

```bash
# Yorumları çıkar (best-effort, eksiksiz olması garanti değil)
yt-dlp --write-comments --skip-download --write-info-json \
  --extractor-args "youtube:max_comments=20" \
  -o "/tmp/%(id)s" "URL"
# Yorumlar .info.json dosyasının comments alanında
```

### Video ara

```bash
yt-dlp --dump-json "ytsearch5:query"
```

> **Altyazı notu**: Elle yüklenen altyazılar güvenilir şekilde çıkarılır; otomatik oluşturulan
> altyazılarda satır tekrarları olabilir, sonradan temizlemek gerekebilir.
> **Yorum notu**: `--write-comments` web sayfası kazımasına dayanır (YouTube Data API değil);
> bazı yorumlar eksik kalabilir.

### Altyazı başarısız olursa yeniden deneme zinciri (sırayla, gerçek içerik gelince dur)

`doctor` yalnızca yt-dlp'nin kendisinin ve JS runtime'ın çalıştığını doğrular, belirli bir
videoya istek atmaz; bu yüzden `active_backend: yt-dlp`, hedef videonun altyazısının canlı
olarak doğrulandığı anlamına gelmez.

1. Önce yukarıdaki `yt-dlp --write-sub --write-auto-sub` komutunu kullan.
2. Bot doğrulaması çıkarsa, altyazı yanıtı boşsa veya altyazı dosyası oluşmadıysa ve OpenCLI
   bağlıysa: `opencli youtube transcript "URL" -f yaml`.
3. OpenCLI `Caption URL returned empty response` döndürürse **en fazla 3 kez yeniden dene**;
   bu, süresi dolan altyazı URL'sinin ara sıra geçersizleşmesidir — boş yanıtı "videonun
   altyazısı yok" diye yorumlama.
4. Hâlâ başarısızsa veya videoda gerçekten altyazı yoksa: `agent-reach transcribe "URL"` ile
   sesi indirip yazıya dök.

Başarı ölçütü, boş olmayan altyazı/transkript içeriği elde etmektir; komutun exit kodu veya
`doctor`'ın sürüm testi sonucu değil.

### Altyazı yoksa son çare: Whisper ile ses transkripsiyonu

```bash
# Videoda altyazı yoksa: sesi indirip Whisper ile yazıya dök (ücretsiz Groq key yeterli)
agent-reach transcribe "https://www.youtube.com/watch?v=VIDEO_ID"
agent-reach transcribe ./local_audio.mp3 -o /tmp/transcript.txt
```

> `agent-reach transcribe` yalnızca herkese açık http(s) URL'leri veya yerel ses dosyalarını
> kabul eder. `ytsearch5:` ile arama yaptıysan önce yt-dlp sonuçlarından belirli bir video
> URL'si seç, sonra onu yazıya dök.
> Önce key yapılandır: `agent-reach configure groq-key` (gizli giriş; ücretsiz, console.groq.com)
> veya `agent-reach configure openai-key`. Varsayılan auto modu yalnızca yapılandırılmış ilk
> sağlayıcıyı kullanır (önce Groq, yoksa OpenAI); başarısız olursa durur, sesi otomatik olarak
> başka bir sağlayıcıya göndermez.
> `--allow-provider-fallback`, sağlayıcılar arası geçişe açıkça izin verir; aynı ses içeriği hem
> Groq hem OpenAI tarafından işlenebilir ve OpenAI ücreti doğabilir. Yalnızca içeriğin iki
> sağlayıcıyla da paylaşılabileceği onaylandıktan sonra kullan.

## Bilibili (ağırlıklı bili-cli, altyazı için OpenCLI)

> ⚠️ **Bilibili'yi yt-dlp ile okuma**: Bilibili'nin bot koruması yt-dlp'yi tamamen 412 ile
> engelliyor (en son sürüm, doğrudan bağlantı/proxy/cookie ile denendi, hiçbiri işe yaramadı).
> yt-dlp yalnızca YouTube için kullanılır.

### Video ayrıntıları / arama / popüler / sıralama (bili-cli, salt-okunur, giriş gerekmez)

```bash
# Video ayrıntıları (başlık / yükleyen / süre / izlenme ve etkileşim / altyazı durumu)
bili video BVxxx

# Video ara (Çince içerik için Çince anahtar kelime daha iyi sonuç verir)
bili search "query" --type video -n 5

# Popüler videolar / sıralama
bili hot -n 10
bili rank -n 10

# Sesi indirip ASR'ye hazır WAV parçalarına böl (altyazı yoksa agent-reach transcribe ile birlikte)
bili audio BVxxx
```

### Altyazı (OpenCLI, masaüstü Chrome gerekir)

```bash
# Zaman damgalı, cümle cümle altyazı
opencli bilibili subtitle BVxxx

# OpenCLI arama ve video meta verisi de okuyabilir (alternatif)
opencli bilibili search "query" -f yaml
opencli bilibili video BVxxx -f yaml
```

### Kurulumsuz son çare: arama API'sine doğrudan istek

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
curl -s -c /tmp/bili_ck.txt -o /dev/null -A "$UA" "https://www.bilibili.com/"
curl -s -b /tmp/bili_ck.txt -A "$UA" -e "https://www.bilibili.com/" \
  "https://api.bilibili.com/x/web-interface/search/all/v2?keyword=QUERY&page=1"
```

> Bu blok bash sözdizimidir; Windows'ta Git Bash ile çalıştır.
>
> **bili-cli kurulumu**: `pipx install bilibili-cli` (upstream 2026-03'ten beri güncellenmiyor
> ama testlerde sağlıklı; salt-okunur kullanımda giriş gerekmez. `bili login` ile uygulamadan
> kod okutarak giriş yapmak akış/favoriler gibi kişisel özellikleri açar — bunu kullanıcı kendisi yapar).

## Xiaoyuzhou podcast

### Tek bölüm podcast transkripsiyonu (isteğe bağlı --polish ile noktalama iyileştirme)

```bash
# /tmp/ altına Markdown dosyası üretir. --polish, Llama 3.3 70B ile metne Çince noktalama ve makul paragraf ekler
~/.agent-reach/tools/xiaoyuzhou/transcribe.sh --polish "https://www.xiaoyuzhoufm.com/episode/EPISODE_ID"
```

> Transkripsiyon prompt'u Whisper'dan zaten Çince noktalama istiyor; noktalama yine de yetersizse
> `--polish` ekleyerek Groq üzerindeki ücretsiz Llama 3.3 70B ile noktalama ve paragraf düzeni
> ekleyebilirsin (9 dakikalık podcast için ~7 saniye ek süre). Her transkripsiyonda fazladan bir
> LLM çağrısı yapar; gerektiğinde kullan.

### Ön koşullar

1. **ffmpeg**: `brew install ffmpeg` (Windows'ta: `winget install Gyan.FFmpeg`)
2. **Groq API Key** (ücretsiz): https://console.groq.com/keys
3. **Key'i yapılandır**: `agent-reach configure groq-key` (gizli giriş)
4. **İlk çalıştırma**: `agent-reach install --env=auto --system --channels=xiaoyuzhou` (kullanıcının açık onayı gerekir)

### Durumu kontrol et

```bash
agent-reach doctor
```

> Markdown çıktı dosyası varsayılan olarak `/tmp/` altına kaydedilir.

## Seçim rehberi

| Senaryo | Önerilen araç |
|-----|---------|
| YouTube altyazısı | yt-dlp; başarısızsa OpenCLI (en fazla 3 kez) → agent-reach transcribe |
| Bilibili video ayrıntısı / arama | bili-cli |
| Bilibili altyazısı | opencli bilibili subtitle |
| Podcast transkripsiyonu | Xiaoyuzhou transcribe.sh |
| Altyazısız ses/video | agent-reach transcribe (Bilibili sesi için önce `bili audio`) |
