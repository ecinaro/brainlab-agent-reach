# Web okuma

Genel web sayfaları, RSS.

## Genel web sayfaları (Jina Reader)

```bash
# Herhangi bir web sayfasının içeriğini oku (Windows PowerShell'de: curl.exe)
curl -s "https://r.jina.ai/URL"

# Örnek
curl -s "https://r.jina.ai/https://example.com/article"
```

**Uygun senaryo**: Web sayfalarının çoğu doğrudan Jina Reader ile okunabilir.

## Web Reader (MCP)

```bash
# Web sayfası içeriğini oku (Markdown formatında)
mcporter call web-reader.webReader url="https://example.com"

# Görselleri koru
mcporter call web-reader.webReader url="https://example.com" retain_images=true

# Düz metin formatı
mcporter call web-reader.webReader url="https://example.com" return_format="text"
```

**Uygun senaryo**: Çıktı formatı üzerinde daha hassas kontrol gerektiğinde.

## RSS (feedparser)

```python
python3 -c "
import feedparser
for e in feedparser.parse('FEED_URL').entries[:5]:
    print(f'{e.title} — {e.link}')
"
```

**Uygun senaryo**: Blog, haber kaynağı, podcast gibi RSS feed'lerini takip etmek.

## Okunamıyorsa → OpenCLI yedeği

401/403/429, Cloudflare "Just a moment", captcha, giriş duvarı veya boş / yalnızca JS iskeleti
dönerse içerik uydurma; [opencli-fallback.md](opencli-fallback.md) merdivenini izle. En kısa yol:

```bash
opencli doctor
opencli web read --url "<url>" --stdout
```

## Seçim rehberi

| Senaryo | Önerilen araç |
|-----|---------|
| Genel web sayfası | Jina Reader (`curl r.jina.ai`) |
| Görsel / format kontrolü gerekiyor | web-reader MCP |
| RSS takibi | feedparser |
| Giriş / Cloudflare / captcha / JS yüzünden okunamıyor | OpenCLI yedeği ([opencli-fallback.md](opencli-fallback.md)) |
