# Sık karşılaşılan sorunlar

Önce her zaman şunu çalıştır:

```bash
agent-reach doctor
```

Hangi kanalın bozuk olduğunu ve çoğu zaman nasıl düzeleceğini söyler.

---

## OpenCLI: çıkış kodu 69 (Browser Bridge bağlı değil)

**Belirti:** `opencli ...` komutu 69 koduyla bitiyor ya da `opencli doctor` eklentiyi bağlı göstermiyor.

**Neden:** Chrome kapalı, OpenCLI eklentisi kurulu değil ya da kapalı.

**Çözüm:**

1. Chrome'u aç ve açık bırak.
2. `chrome://extensions` sayfasına git, OpenCLI eklentisinin **açık** olduğundan emin ol. Yoksa kur: https://chromewebstore.google.com/detail/opencli/ildkmabpimmkaediidaifkhjpohdnifk
3. Tekrar kontrol et:

```bash
opencli doctor
```

---

## OpenCLI: çıkış kodu 77 (giriş yapılmamış)

**Belirti:** Komut 77 koduyla bitiyor, "giriş gerekli" / AUTH_REQUIRED benzeri bir mesaj var.

**Neden:** O siteye Chrome'da giriş yapılmamış ya da oturum süresi dolmuş.

**Çözüm:** Chrome'da siteye **kendin** giriş yap, sonra komutu tekrar çalıştır. Ajan senin yerine giriş yapmaz, şifre istemez, captcha çözmez.

---

## OpenCLI: çıkış kodu 75 (zaman aşımı)

**Belirti:** Komut 75 koduyla bitiyor.

**Neden:** Sayfa zamanında yüklenmedi ya da Chrome meşgul/takılı.

**Çözüm:** Biraz bekleyip tekrar dene. Chrome'da takılı bir sekme ya da açılır pencere olup olmadığına bak. Olmazsa servisi yeniden başlat:

```bash
opencli daemon status
opencli daemon restart
```

---

## OpenCLI: `attach failed: chrome-extension://...`

**Neden:** Başka bir eklenti (ör. 1Password) Chrome'un hata ayıklayıcısını kullanıyor ve OpenCLI'ın bağlanmasını engelliyor.

**Çözüm:** O eklentiyi `chrome://extensions` sayfasından geçici olarak kapat, komutu tekrar dene.

---

## OpenCLI: komut bulunamadı / Windows'ta npm hatası

**Belirti:** `opencli: command not found` ya da PowerShell "betik çalıştırma devre dışı" diyor.

**Çözüm:**

- Node.js 20+ kurulu mu bak: `node -v`
- Kur: `npm install -g @jackwener/opencli`
- Windows PowerShell betik hatası verirse `npm.cmd install -g @jackwener/opencli` kullan.
- Terminali kapatıp aç. Hâlâ bulunamıyorsa `npm root -g` ile global klasörü bul ve PATH'e ekle.

Detaylı kurulum: [opencli-chrome-kurulum.md](opencli-chrome-kurulum.md)

---

## Bir site okunmuyor (Cloudflare, giriş duvarı, boş sayfa)

**Belirti:** `curl https://r.jina.ai/URL` boş, "Just a moment..." (Cloudflare), captcha ya da 401/403/429 dönüyor.

**Çözüm:** OpenCLI yedeğini kullan (masaüstü + Chrome gerekir):

```bash
opencli web read --url https://ornek.com/sayfa --stdout
```

Hâlâ giriş istiyorsa Chrome'da o siteye kendin giriş yap. Ajanın karar sırası: [opencli-fallback.md](../agent_reach/skill/references/opencli-fallback.md)

---

## Xueqiu: API 400 döndürüyor

**Belirti:** `agent-reach doctor` Xueqiu için ⚠️ gösteriyor, `HTTP Error 400` hatası var.

**Neden:** Xueqiu API'si giriş Cookie'si istiyor, anonim erişimle veri alınamıyor.

**Çözüm:** Chrome'da xueqiu.com'a giriş yap, sonra çalıştır:

```bash
agent-reach configure --from-browser chrome --platform xueqiu
```

`agent-reach doctor` ile ✅ olduğunu doğrula. Cookie süresi dolunca komutu tekrar çalıştır.

---

## Twitter/X: twitter-cli bağlanamıyor

**Belirti:** `twitter search` ya da başka komutlar hata veriyor.

**Neden:** twitter-cli, Twitter API'sine erişmek için `TWITTER_AUTH_TOKEN` ve `TWITTER_CT0`
ortam değişkenlerine ihtiyaç duyar. `agent-reach configure twitter-cookies` ile kaydedilen
değerler sadece doctor'ın ayarların tam olup olmadığını kontrol etmesi içindir; doctor
üst akıştaki kimlik doğrulamayı çalıştırmaz ve mevcut Shell'i ayarlamaz. Ağın x.com'a
erişmek için proxy gerektiriyorsa proxy de ayarlaman gerekir.

**Çözüm:**

### Yol 1: Ortam değişkeni ile proxy

```bash
export TWITTER_AUTH_TOKEN="..."
export TWITTER_CT0="..."
export HTTP_PROXY="http://user:pass@host:port"
export HTTPS_PROXY="http://user:pass@host:port"
twitter search "test" -n 1
```

### Yol 2: Genel proxy aracı

Tüm ağ trafiğini proxy aracına devret; böylece twitter-cli istekleri de proxy'den geçer:

```bash
# macOS — ClashX / Surge "Enhanced Mode" açık
# Linux — proxychains ya da tun2socks
proxychains twitter search "test" -n 1
```

### Yol 3: twitter-cli yerine Exa araması

twitter-cli çalışmıyorsa Twitter içeriğini doğrudan Exa ile arayabilirsin:

```bash
mcporter call exa.web_search_exa query="site:x.com arama kelimesi" numResults=5
```

### Yol 4: OpenCLI yedeği (masaüstü)

Chrome'da x.com'a giriş yaptıysan OpenCLI de kullanılabilir. Kullanılabilir komutlar için `opencli list` ve `opencli twitter --help`.

### Yol 5: Kimlik doğrulamayı kontrol et

```bash
twitter check
```

> "Missing credentials" dönerse, komutu çalıştıran işlemin ortamında
> `TWITTER_AUTH_TOKEN` ve `TWITTER_CT0` ayarlanmalı.
>
> **Yedek:** bird CLI kuruluysa (`npm install -g @steipete/bird`) o da çalışır. Agent Reach kurulu araçları kendiliğinden tespit eder.
