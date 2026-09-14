<h1 align="center">👁️ Agent Reach (Türkçe)</h1>

<p align="center">
  <strong>Yapay zekâ ajanına internet gözü tak.</strong>
</p>

<p align="center">
  Twitter, Reddit, YouTube, GitHub ve giriş isteyen siteleri ajanın okuyabilsin diye araçları senin yerine seçer, kurar ve kontrol eder.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="MIT License"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10+-green.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+"></a>
  <a href="https://github.com/ecinaro/brainlab-agent-reach/stargazers"><img src="https://img.shields.io/github/stars/ecinaro/brainlab-agent-reach?style=for-the-badge" alt="GitHub Stars"></a>
</p>

<p align="center">
  <strong>Türkçe</strong> · <a href="docs/README_en.md">English</a> · <a href="docs/README_zh.md">中文</a> · <a href="docs/README_ja.md">日本語</a> · <a href="docs/README_ko.md">한국어</a>
</p>

---

## 🚀 Ajanına sadece bunu yapıştır

```
Şu talimatları oku ve Agent Reach'i benim için kur: https://raw.githubusercontent.com/ecinaro/brainlab-agent-reach/main/docs/install.md
```

Bu kadar. Gerisini ajan kendisi yapar. Senden sadece Chrome'a bir eklenti eklemeni ve sitelere giriş yapmanı isteyecek.

Zaten kurduysan, güncellemek için:

```
Şu talimatları oku ve Agent Reach'i benim için güncelle: https://raw.githubusercontent.com/ecinaro/brainlab-agent-reach/main/docs/update.md
```

> Bu bir çatal (fork). Orijinal proje: [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach). Bu sürümde her şey Türkçe ve OpenCLI, erişilemeyen tüm siteler için yedek yol olarak eklendi.

---

## Bu ne?

Claude Code, Cursor, Codex gibi yapay zekâ ajanları kod yazmayı bilir ama internette çoğu yere giremez. Twitter para ister, Reddit engeller, bazı siteler giriş ister, bazıları Cloudflare ile kapıyı kapatır.

Agent Reach bu kapıları açan araçları kurar. Sonra `agent-reach doctor` ile hangisinin çalıştığını söyler. Okumayı ajan bu araçlarla kendisi yapar.

Hiçbir yol işe yaramazsa ajan **OpenCLI** ile senin Chrome'unu kullanır. Site karşısında normal bir kullanıcı görür: seni.

---

## Neler okuyabilir?

| Platform | Ne yapar | Kurulum gerekir mi? |
|---|---|---|
| 🌐 Herhangi bir web sayfası | Linki temiz metne çevirir ([Jina Reader](https://github.com/jina-ai/reader)) | Hayır, kurulumsuz çalışır |
| 🔍 Web araması | İnternette anlamına göre arar ([Exa](https://exa.ai)) | Hayır, kurulumda otomatik |
| 📺 YouTube | Altyazı çeker, video arar (yt-dlp) | Hayır |
| 📦 GitHub | Açık repoları okur ve arar (gh CLI) | Hayır. Özel repo için `gh auth login` |
| 📡 RSS | Her türlü RSS/Atom akışını okur | Hayır |
| 💻 V2EX | Popüler konular, konu detayı, kullanıcı | Hayır |
| 📺 Bilibili | Arama + video detayı (bili-cli) | Hayır. Altyazı için OpenCLI |
| 🐦 Twitter/X | Tweet arar, okur, akış gösterir | Evet: Cookie ya da OpenCLI |
| 📖 Reddit | Arar, gönderi ve yorum okur | Evet: OpenCLI ya da rdt-cli + Cookie |
| 📘 Facebook | Arama, sayfa, akış, grup listesi | Evet: OpenCLI |
| 📷 Instagram | Kullanıcı arama, profil, son gönderiler | Evet: OpenCLI |
| 📕 XiaoHongShu (小红书) | Arama, not okuma, yorumlar | Evet: OpenCLI ya da Cookie-Editor + MCP |
| 💼 LinkedIn | Açık sayfaları okur; tam profil ve iş arama | Kısmen: tam hali için mcp-server-linkedin |
| 📈 Xueqiu | Hisse fiyatı, popüler gönderiler | Evet: Cookie |
| 🎙️ Xiaoyuzhou podcast | Sesi yazıya döker (Groq Whisper) | Evet: ücretsiz Groq anahtarı |
| 🧩 **Diğer her site** (giriş, Cloudflare, boş gelen sayfa) | Senin Chrome'un üzerinden okur | Evet: OpenCLI + Chrome eklentisi |

> Twitter notu: Cookie'yi kaydetmek sadece `doctor` kontrolü içindir. `twitter` komutunu doğrudan çalıştırmadan önce `TWITTER_AUTH_TOKEN` ve `TWITTER_CT0` ortam değişkenlerini ayarlaman gerekir.

Hangisini nasıl açacağını bilmene gerek yok. Ajana "Twitter'ı kur" demen yeter, adım adım yol gösterir.

---

## Elle kurulum (insanlar için)

Ajan kullanmadan kendin kurmak istersen. Python 3.10 veya üstü lazım.

```bash
# 1. Paketi kur (PyPI'daki "agent-reach" bu proje DEĞİL, GitHub linkini kullan)
pip install https://github.com/ecinaro/brainlab-agent-reach/archive/main.zip

# 2. Bilgisayarını kontrol et (hiçbir şeyi değiştirmez)
agent-reach install --env=auto

# 3. Eksikleri gerçekten kur (izin veriyorsan)
agent-reach install --env=auto --system

# 4. Ajanına skill dosyasını kur
agent-reach skill --install

# 5. Neyin çalıştığına bak
agent-reach doctor
```

- `pip` "externally-managed-environment" hatası verirse `pipx install ...` kullan ya da önce bir `venv` aç.
- Windows'ta `python3` Microsoft Store'u açıyorsa `py -3` kullan.
- İsteğe bağlı kanallar: `agent-reach install --env=auto --system --channels=opencli,twitter,reddit` (hepsi için `--channels=all`).
- Önce ne yapacağını görmek için: `agent-reach install --env=auto --dry-run`.

---

## Neden OpenCLI lazım?

Ajanlar internette sık sık duvara çarpar:

- **Giriş duvarı:** Site "önce giriş yap" der. Ajanın hesabı yok.
- **Cloudflare / captcha:** Site "robot musun?" diye sorar. Ajan geçemez.
- **Boş sayfa:** Sayfa JavaScript ile yüklenir. Ajan boş HTML görür.
- **401 / 403 / 429 hataları:** Site ajanı engeller ya da yavaşlatır.

[OpenCLI](https://github.com/jackwener/opencli) bunu şöyle çözer:

- Senin Chrome'unda **zaten açık olan oturumu** kullanır. Site normal bir kullanıcı görür.
- Şifreni ajana **vermezsin**. Giriş yapan sensin, ajan sadece açık sayfayı okur.
- Her şey **senin bilgisayarında** kalır. Veri başka bir sunucuya gitmez.
- Ajan **sadece okur**. Beğenmez, paylaşmaz, mesaj atmaz.

Nasıl çalışır, tek satırda:

```
opencli  ⇄  localhost:19825 (arka plan servisi)  ⇄  Chrome eklentisi  ⇄  senin Chrome'un
```

---

## OpenCLI'ı Chrome'a kur (5 adım)

1. **Node.js 20 veya üstünü kur:** [nodejs.org](https://nodejs.org). Kontrol: `node -v`
2. **OpenCLI'ı kur:**
   ```bash
   npm install -g @jackwener/opencli
   ```
   Windows PowerShell `npm` için "script çalıştırma kapalı" derse `npm.cmd install -g @jackwener/opencli` yaz.
3. **Chrome eklentisini ekle:** [Chrome Web Mağazası'ndaki OpenCLI eklentisini](https://chromewebstore.google.com/detail/opencli/ildkmabpimmkaediidaifkhjpohdnifk) aç, "Chrome'a ekle"ye tıkla.
   Mağaza açılmazsa: [Releases](https://github.com/jackwener/opencli/releases) sayfasından `opencli-extension-v*.zip` dosyasını indir, klasöre çıkar, `chrome://extensions` aç, sağ üstten **Geliştirici modu**nu aç, **Paketlenmemiş öğe yükle** ile klasörü seç.
4. **Sitelere giriş yap:** Chrome'da okumak istediğin sitelere (Reddit, Facebook, Instagram, X...) normal şekilde giriş yap. Bunu sen yaparsın, ajan yapmaz.
5. **Kontrol et:**
   ```bash
   opencli doctor
   ```
   Eklentinin bağlı (connected) olduğunu görmelisin.

Daha detaylı anlatım: [docs/opencli-chrome-kurulum.md](docs/opencli-chrome-kurulum.md)

---

## Sorun mu var?

- **Çıkış kodu 69:** Chrome eklentisi bağlı değil. `chrome://extensions` aç, OpenCLI'ı etkinleştir, Chrome'u açık tut.
- **Çıkış kodu 77:** O siteye giriş yapmamışsın. Chrome'da giriş yap, tekrar dene.
- **Eklenti kapalı ya da daemon takıldı:** `opencli daemon restart`, sonra `opencli doctor`.
- **"attach failed: chrome-extension://..."**: 1Password gibi tarayıcıda hata ayıklayıcı kullanan başka bir eklentiyi geçici olarak kapat.

Diğer sorunlar: [docs/troubleshooting.md](docs/troubleshooting.md)

---

## Nasıl çalışır? (merak edenler için)

Agent Reach bir "yetenek katmanı"dır. Her platform için birden fazla yol (backend) bilir, sırayla dener, çalışan ilkini seçer. `agent-reach doctor` şu an hangi yolun kullanıldığını söyler.

```
channels/
├── web.py          → Jina Reader ▸ OpenCLI (yedek)
├── twitter.py      → twitter-cli ▸ OpenCLI ▸ bird
├── youtube.py      → yt-dlp
├── github.py       → gh CLI
├── bilibili.py     → bili-cli ▸ OpenCLI ▸ arama API'si
├── reddit.py       → OpenCLI ▸ rdt-cli
├── facebook.py     → OpenCLI
├── instagram.py    → OpenCLI
├── xiaohongshu.py  → OpenCLI ▸ xiaohongshu-mcp ▸ xhs-cli
├── linkedin.py     → mcp-server-linkedin ▸ Jina Reader
├── rss.py          → feedparser
└── exa_search.py   → Exa (mcporter üzerinden)
```

Ajana komut ezberletmen gerekmez. Ajan skill dosyasını ([agent_reach/skill/SKILL.md](agent_reach/skill/SKILL.md)) okur ve ne çağıracağını bilir. Hiçbir yol çalışmazsa [OpenCLI yedek rehberini](agent_reach/skill/references/opencli-fallback.md) izler.

---

## Güvenlik

- **Bilgilerin sende kalır.** Cookie ve anahtarlar sadece bilgisayarındaki `~/.agent-reach/config.yaml` dosyasında durur. Hiçbir yere yüklenmez.
- **Varsayılan olarak hiçbir şeyi değiştirmez.** `agent-reach install` sadece kontrol eder. Kurulum için açıkça `--system` demen gerekir.
- **Ajan giriş yapmaz, captcha çözmez.** Giriş ve doğrulamayı her zaman sen yaparsın. Cookie kullanan platformlarda ana hesabın yerine yedek bir hesap kullanmanı öneririz; platformlar otomatik erişimi fark edip hesabı kısıtlayabilir.

Kaldırmak için: `agent-reach uninstall` (önizleme: `--dry-run`), sonra `pip uninstall agent-reach`.

---

## Teşekkürler

- Orijinal proje: [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach). Bu repo onun Türkçe çatalıdır. Orijinal projenin sponsorları ve iletişim bilgileri [Çince README](docs/README_zh.md) dosyasında.
- Tarayıcı köprüsü: [jackwener/opencli](https://github.com/jackwener/opencli) (Apache-2.0).
- Kullanılan diğer açık kaynak araçlar: [twitter-cli](https://github.com/public-clis/twitter-cli) · [rdt-cli](https://github.com/public-clis/rdt-cli) · [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) · [xhs-cli](https://github.com/jackwener/xiaohongshu-cli) · [bili-cli](https://github.com/public-clis/bilibili-cli) · [yt-dlp](https://github.com/yt-dlp/yt-dlp) · [Jina Reader](https://github.com/jina-ai/reader) · [Exa](https://exa.ai) · [mcporter](https://github.com/nicobailon/mcporter) · [feedparser](https://github.com/kurtmckee/feedparser) · [mcp-server-linkedin](https://github.com/stickerdaniel/linkedin-mcp-server)

Bu Türkçe sürümle ilgili hata ve öneriler: [GitHub Issues](https://github.com/ecinaro/brainlab-agent-reach/issues)

Yeni başlayanlar için basit anlatım: [Yapay zekâ ajanına internet gözü tak: Agent Reach nedir?](docs/blog-agent-reach-nedir.md)

## Lisans

[MIT](LICENSE)
