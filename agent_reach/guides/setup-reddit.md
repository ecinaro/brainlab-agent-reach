# Reddit kurulum rehberi

## Ne işe yarar?

Reddit, tarayıcı dışından gelen neredeyse tüm doğrudan erişimi engeller (veri merkezi ve ISP proxy IP'leri dahil). JSON API 403 döner.

Agent Reach, Reddit araması ve okuması için **rdt-cli** kullanır:
- **Arama:** `rdt search "anahtar kelime"`
- **Gönderi + yorumların tamamını okuma:** `rdt read POST_ID`

Ücretsiz; proxy ve API anahtarı gerekmez. Giriş gerekir (`rdt login`, tarayıcıdan Cookie'yi otomatik çeker).

> Masaüstünde Chrome kullanıyorsan **OpenCLI** daha kolay bir yoldur: Chrome'da reddit.com'a giriş yapman yeterli. Kurulum: `agent-reach install --env=auto --system --channels=opencli`, sonra `opencli reddit search "anahtar kelime" -f yaml`. Detay: [docs/opencli-chrome-kurulum.md](../../docs/opencli-chrome-kurulum.md)

## Ajanın kendi yapabileceği adımlar

1. rdt-cli kurulu mu kontrol et:
```bash
which rdt && echo "installed" || echo "not installed"
```

2. Kurulu değilse kur (PyPI sürümü şimdilik geride, en yeni sürümü GitHub'dan kur):
```bash
pipx install 'git+https://github.com/public-clis/rdt-cli.git'
```

Ya da tek komutla:
```bash
agent-reach install --env=auto --system --channels=reddit
```

## Kullanım örnekleri

Reddit'te ara:
```bash
rdt search "python best practices" -n 5
```

Gönderiyi ve yorumları tamamen oku:
```bash
rdt read POST_ID
```

## Kullanıcının elle yapması gerekenler

Hiçbir şey. Kullanıcı açıkça izin verdikten sonra rdt-cli
`agent-reach install --env=auto --system --channels=reddit` ile kurulur.

## Yedek: Exa araması

Exa'yı (mcporter üzerinden) zaten ayarladıysan Reddit içeriğini Exa ile de arayabilirsin:

```bash
mcporter call exa.web_search_exa query="site:reddit.com python best practices" numResults=5
```

rdt-cli şu an önerilen yoldur, ek ayar gerekmeden çalışır.
