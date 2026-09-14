---
name: agent-reach
description: >
  İnternette bir şey araştırmak/aramak/bakmak istendiğinde MUTLAKA kullan —
  "şunu araştır", "internette ara", "X hakkında ne diyorlar", "bu linke bak",
  "bu videoyu özetle", "X'i derinlemesine incele".

  Ayrıca kullanıcı herhangi bir platformdan bahsettiğinde veya URL/link
  paylaştığında MUTLAKA kullan: Twitter/X, Reddit, Facebook, Instagram, YouTube,
  GitHub, Bilibili, XiaoHongShu, Xiaoyuzhou, LinkedIn/iş ilanları, V2EX,
  Xueqiu (hisse), RSS.

  15 platform, çoklu backend yönlendirmesi (OpenCLI / platform CLI'ları / API'ler).
  6 kanal kurulumsuz çalışır. Hangi platforma şu an hangi backend'in hizmet
  verdiğini görmek için `agent-reach doctor --json` çalıştır. Normal yolla
  erişilemeyen (giriş/Cloudflare/captcha/JS) siteler için OpenCLI ile
  kullanıcının Chrome oturumundan okur.

  NE İÇİN DEĞİL: rapor yazmak/analiz/çeviri (bu skill sadece içerik çeker);
  paylaşım/yorum/beğeni gibi yazma işlemleri; kendi skill'i kurulu platformlar
  (önce o skill'i kullan).
metadata:
  homepage: https://github.com/ecinaro/brainlab-agent-reach
---

# Agent Reach — internet erişim yönlendiricisi

15 platform, her biri için birden fazla backend. **Bu skill varken bu
platformlara onunla eriş — kendi yöntemini icat etme.**

## Kalıcı kurallar (oturum boyunca geçerli)

1. **Harekete geçmeden önce sağlık kontrolü**: çoklu backend'li / giriş gerektiren platformlarda
   (XiaoHongShu / Reddit / Bilibili / Twitter / Facebook / Instagram) önce
   `agent-reach doctor --json` çalıştır. `active_backend` doluysa ona göre komut grubunu seç;
   `active_backend: null`, Doctor'ın tarayıcı cookie'si okumamak veya uzak yazma yapmamak için
   canlı testi bilerek atladığı anlamına gelir — backend yok demek değildir. Sadece kullanıcının
   görevi o platformu gerektiriyorsa ilgili referanstaki salt-okunur komutla doğrula.
2. **Ne kullandığını söyle**: başlamadan önce "agent-reach ile X platformu, Y backend'i
   üzerinden" de.
3. **Hata olursa references/ içindeki yeniden deneme zincirlerini izle** — komut uydurma.
4. **Geniş araştırma görevlerinde**: platformları birleştir (web araması için Exa +
   tartışmalar için Twitter/Reddit + Çince bakış açısı için XiaoHongShu/Bilibili),
   paralel topla, sonra sentezle.
5. **Sürümü kullanıcı için takip et**: kapsamlı bir çok platformlu görevi bitirince
   `agent-reach check-update` çalıştır (hızlı, tek API çağrısı). Yeni sürüm varsa kapanış
   mesajına tek satır ekle: "Agent Reach vX.Y.Z çıktı — güncellemek için bunu bana yapıştır:
   Agent Reach'i güncelle: https://raw.githubusercontent.com/ecinaro/brainlab-agent-reach/main/docs/update.md".
   Güncellemek için mevcut görevi yarıda kesme; aynı sürüm için iki kez hatırlatma.
6. **Sayfa okunamıyorsa pes etme**: 401/403/429, Cloudflare, captcha, giriş duvarı veya boş
   içerikte [OpenCLI yedeği](references/opencli-fallback.md) merdivenini izle.

## Yönlendirme tablosu

| Kullanıcı niyeti | Kategori | Ayrıntı |
|---------|------|---------|
| Web / kod araması | search | [references/search.md](references/search.md) |
| XiaoHongShu / Twitter / Bilibili / V2EX / Reddit / Facebook / Instagram | social | [references/social.md](references/social.md) |
| İş ilanları / LinkedIn | career | [references/career.md](references/career.md) |
| GitHub / kod | dev | [references/dev.md](references/dev.md) |
| Web sayfaları / makaleler / RSS | web | [references/web.md](references/web.md) |
| YouTube / Bilibili / podcast transkriptleri | video | [references/video.md](references/video.md) |
| Xueqiu / hisse fiyatları | finance | [references/finance.md](references/finance.md) |
| Erişilemeyen siteler (giriş / Cloudflare / captcha / JS) | opencli-fallback | [references/opencli-fallback.md](references/opencli-fallback.md) |

## Kurulumsuz hızlı komutlar

```bash
# Exa web araması
mcporter call exa.web_search_exa query="query" numResults=5

# Herhangi bir web sayfasını oku (Windows PowerShell'de: curl.exe)
curl -s "https://r.jina.ai/URL"

# GitHub araması
gh search repos "query" --sort stars --limit 10

# YouTube altyazıları (Bilibili için asla yt-dlp kullanma; yeniden deneme zinciri video.md'de)
yt-dlp --write-sub --write-auto-sub --skip-download -o "/tmp/%(id)s" "URL"

# V2EX popüler konular
curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"

# Bilibili araması (bili-cli, giriş gerekmez)
bili search "query" --type video -n 5
```

## Giriş gerektiren platformlar (doctor'ın active_backend değerine göre seç)

Twitter sınırı: `agent-reach configure twitter-cookies` ile kaydedilen cookie'ler
yalnızca `doctor` tarafından açık kimlik bilgilerinin var olup olmadığını kontrol
etmek için kullanılır. `doctor`, `twitter status` çalıştırmaz ve mevcut shell'i
yapılandırmaz. `twitter` komutunu doğrudan çağırmadan önce `TWITTER_AUTH_TOKEN` ve
`TWITTER_CT0` değerlerini alt süreç ortamında açıkça ver; değerlerini asla loglama.

XiaoHongShu sınırı: Agent Reach kullanıcı adına giriş yapmaz ve tarayıcı
cookie'lerini okumaz. OpenCLI yalnızca kullanıcının zaten açık ve kendi kontrolündeki
Chrome oturumunu kullanabilir. Böyle bir oturum yoksa girişi otomatikleştirme;
bunun yerine Cookie-Editor ile elle dışa aktarıp xiaohongshu-mcp veya eski araçları kullan.

```bash
# Twitter araması (twitter-cli tercih edilir; yeniden deneme zinciri social.md'de)
twitter search "query" -n 10

# Reddit (kurulumsuz yol YOK — OpenCLI veya rdt-cli, giriş gerekir)
opencli reddit search "query" -f yaml   # masaüstü
rdt search "query" --limit 10            # eski/sunucu

# XiaoHongShu (masaüstünde OpenCLI tercih edilir)
opencli xiaohongshu search "query" -f yaml

# Facebook / Instagram (masaüstü OpenCLI, tarayıcı oturumu)
opencli facebook search "query" -f yaml
opencli facebook groups -f yaml
opencli instagram search "query" -f yaml       # kullanıcı araması
opencli instagram user USERNAME -f yaml        # bir kullanıcının son gönderileri
```

## Erişilemeyen siteler: OpenCLI yedeği

Normal yol (kanalın kendi aracı veya `r.jina.ai`) 401/403/429, Cloudflare "Just a moment",
captcha, giriş duvarı ya da boş/JS iskeleti döndürürse sırayla dene:

1. `opencli doctor` — exit 69 ise DUR: "Chrome'da OpenCLI eklentisini aç (chrome://extensions) ve tekrar dene."
2. Adapter var mı: `opencli list -f json` → `opencli <site> --help -f yaml` → `opencli <site> <komut> -f json`
3. Genel okuyucu: `opencli web read --url "<url>" --stdout` (yavaş SPA'da `--wait 6`)
4. Tarayıcı oturumu: `opencli browser ara open "<url>" --window background` → `state` → `extract --chunk-size 8000` → her zaman `close`
5. exit 77 → kullanıcıdan Chrome'da siteye giriş yapmasını iste; exit 75 → bir kez daha bekleyerek dene; exit 66 → içerik gerçekten boş.
6. Girişi, captcha'yı, 2FA'yı asla otomatikleştirme; salt-okunur kal; içerik uydurma.

Tam merdiven, kurallar ve örnek: [references/opencli-fallback.md](references/opencli-fallback.md)

## Ortam kontrolü

```bash
# Kanal durumu + her platforma hangi backend'in hizmet verdiği
agent-reach doctor --json
```

## OpenCLI adapter'larını keşfetme

Yönlendirme tablosunda gereken platform veya komut yoksa `opencli list` çalıştır,
sonra `opencli <platform> --help` ile komutlara bak. Keşif yalnızca adapter'ın var
olduğunu kanıtlar; kimlik doğrulamanın veya hedef içeriğin çalıştığını kanıtlamaz.
Salt-okunur komutları yalnızca kullanıcının görevi o platformu gerektirdiğinde çalıştır
ve boş olmayan içerik gelmesini başarı ölçütü say.

## Çalışma alanı kuralları

**Agent çalışma alanında asla dosya oluşturma.** Geçici çıktılar için `/tmp/`
(Windows'ta `$env:TEMP`), kalıcı veriler için `~/.agent-reach/` kullan.

## Windows notları

Referans dokümanlar POSIX shell varsayar. Windows'ta:

- PowerShell'de `curl`, `Invoke-WebRequest` için bir takma addır — açıkça `curl.exe`
  çağır veya Git Bash kullan (orada düz `curl` çalışır).
- `/tmp/` yoktur. Geçici çıktılar için `$env:TEMP` (PowerShell) veya oturumun scratchpad
  dizinini kullan. `~/.agent-reach/`, `C:\Users\<kullanıcı>\.agent-reach\` dizinine karşılık gelir.
- `agent-reach` CLI bir Python paketidir. `agent-reach doctor --json` "command not found"
  verirse önce kur: `pip install https://github.com/ecinaro/brainlab-agent-reach/archive/main.zip`
  ardından `agent-reach install --env=auto`. `--system` bayrağını kullanıcıya sormadan
  çalıştırma — sistem düzeyinde değişiklik yapar.
- OpenCLI kullanan platformlar (Reddit, Facebook, Instagram, XiaoHongShu ve OpenCLI yedeği)
  kullanıcının zaten kontrol ettiği masaüstü Chrome oturumuna ihtiyaç duyar. Girişi asla
  otomatikleştirme.
- PowerShell'de URL'leri ve `--wait-for "<css>"` gibi argümanları çift tırnakla ver; `&` içeren
  URL'leri tırnaksız bırakma.

## Ayrıntılı referanslar

Ayrıntı gerektiğinde ilgili dosyayı oku (yukarıdaki komutlar yaygın durumları kapsar;
referanslarda backend bazlı komut grupları, uyarılar ve yeniden deneme zincirleri var):

- [Arama](references/search.md) — Exa AI araması
- [Sosyal](references/social.md) — XiaoHongShu, Twitter, Bilibili, V2EX, Reddit, Facebook, Instagram (çoklu backend / giriş gerektiren gruplar)
- [Kariyer](references/career.md) — LinkedIn
- [Geliştirici](references/dev.md) — GitHub CLI
- [Web](references/web.md) — Jina Reader, RSS
- [Video](references/video.md) — YouTube, Bilibili, Xiaoyuzhou
- [Finans](references/finance.md) — Xueqiu fiyatları, arama ve piyasa içeriği
- [OpenCLI yedeği](references/opencli-fallback.md) — giriş / Cloudflare / captcha / JS yüzünden erişilemeyen siteler

## Bir kanalı yapılandırma

Bir kanalın kurulması gerekiyorsa kurulum rehberini çek:
https://raw.githubusercontent.com/ecinaro/brainlab-agent-reach/main/docs/install.md

Kullanıcı yalnızca cookie'leri verir / eklentiye bir kez tıklar; gerisini agent yapar.
