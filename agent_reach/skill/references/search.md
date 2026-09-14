# Arama araçları

Exa AI arama motoru.

## Exa AI araması

Yüksek kaliteli AI arama motoru; teknik dokümantasyon, resmi örnekler ve ilgili web
sayfalarını bulmak için uygundur.

```bash
mcporter call exa.web_search_exa query="query" numResults=5
mcporter call exa.web_search_exa query="library API code example" numResults=5
```

### Kullanım senaryoları

| Senaryo | Parametre |
|-----|------|
| Web araması | `web_search_exa(query: "...", numResults: 5)` |
| Teknik / kod kaynakları | `web_search_exa(query: "framework adı API örneği", numResults: 5)` |

> Exa MCP'deki `get_code_context_exa` kullanımdan kaldırıldı ve varsayılan olarak kayıtlı
> değil. Kod soruları için de `web_search_exa` kullan; bir repo içinde kesin arama
> gerekiyorsa `dev.md` içindeki GitHub aramasına geç.

### Özellikler

- İngilizce içerikte ve teknik dokümantasyonda güçlü
- Sorgu ifadeleriyle resmi dokümanlar ve kod örnekleri bulunabilir
- Sonuç kalitesi yüksek

## Diğer arama araçlarıyla karşılaştırma

| Araç | Kaynak | Uygun senaryo |
|-----|------|---------|
| Exa | agent-reach | İngilizce / teknik / kod araması |
| Zhipu araması | my-mcp-tools | Çince arama |
| GitHub araması | agent-reach (dev.md) | Repo / kod araması |
| OpenCLI arama adapter'ları (`opencli google search`, `opencli duckduckgo search`, `opencli brave search`) | OpenCLI | Diğer araçlar engellendiğinde; bkz. [opencli-fallback.md](opencli-fallback.md) |
