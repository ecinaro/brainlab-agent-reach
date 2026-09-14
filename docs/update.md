# Agent Reach — Güncelleme Rehberi

## İnsanlar için

Bu cümleyi yapay zekâ ajanına yapıştır:

```
Şu talimatları oku ve Agent Reach'i benim için güncelle: https://raw.githubusercontent.com/ecinaro/brainlab-agent-reach/main/docs/update.md
```

İngilizce istersen:

```
Update Agent Reach: https://raw.githubusercontent.com/ecinaro/brainlab-agent-reach/main/docs/update.md
```

---

## Yapay zekâ ajanları için

Kullanıcıyla Türkçe konuş. Kısa ve basit cümleler kur.

### ⚠️ Çalışma alanı kuralları

**Ajanın çalışma alanında (workspace) asla dosya oluşturma, repo klonlama ya da komut çalıştırma.** Geçici işler için `/tmp/`, kalıcı veriler için `~/.agent-reach/` kullan.

### Amaç

Agent Reach'i en son sürüme güncelle, üst akış araçlarını tazele, emekliye ayrılan yollardan yenilerine geç ve her şeyin çalıştığını doğrula. Kullanıcı elle hiçbir şey yapmak zorunda kalmamalı (sadece bir insanın yapabileceği işler hariç: Chrome eklentisi eklemek, bir siteye giriş yapmak gibi).

### Adım 1: Mevcut sürümü kontrol et

```bash
agent-reach check-update
```

Çıktı zaten en son sürümde olduğunu söylüyorsa Adım 5'e (doğrulama) geç. Değilse devam et.

### Adım 2: Agent Reach paketini güncelle

```bash
pip install --upgrade https://github.com/ecinaro/brainlab-agent-reach/archive/main.zip
```

> pip `externally-managed-environment` (PEP 668) hatası verirse kullanıcı ilk kurulumu
> pipx ya da venv ile yapmıştır. Uygun komutu kullan:
> `pipx install --force https://github.com/ecinaro/brainlab-agent-reach/archive/main.zip`
> ya da önce `~/.agent-reach-venv` ortamını etkinleştir.

### Adım 3: Üst akış araçlarını tazele

Kurulu araçları güncel tutmak için bunları çalıştır. **Sadece zaten kurulu olanı güncelle; kullanıcının hiç istemediği yeni araçları kurma** (tek istisna: masaüstünde OpenCLI, aşağıya bak).

```bash
# Kullanıcıda zaten olan Python tabanlı CLI'lar (güncelleme imzaları taze tutar)
which twitter >/dev/null 2>&1 && { pipx upgrade twitter-cli 2>/dev/null || uv tool upgrade twitter-cli 2>/dev/null; }
which bili    >/dev/null 2>&1 && { pipx upgrade bilibili-cli 2>/dev/null || uv tool upgrade bilibili-cli 2>/dev/null; }
which xhs     >/dev/null 2>&1 && { pipx upgrade xiaohongshu-cli 2>/dev/null || uv tool upgrade xiaohongshu-cli 2>/dev/null; }
which yt-dlp  >/dev/null 2>&1 && { pipx install --force 'yt-dlp[default]' 2>/dev/null || uv tool install --force 'yt-dlp[default]' 2>/dev/null || python -m pip install -U 'yt-dlp[default]' 2>/dev/null; }

# rdt-cli bir git kaynağına sabitlenmiştir (PyPI geride) — koddaki _RDT_GIT_SOURCE ile aynı sabit sürüm
which rdt >/dev/null 2>&1 && pipx install --force 'git+https://github.com/public-clis/rdt-cli.git@5e4fb3720d5c174e976cd425ccc3b879d52cac66' 2>/dev/null

# npm tabanlı
which mcporter >/dev/null 2>&1 && npm update -g mcporter 2>/dev/null
which opencli  >/dev/null 2>&1 && npm update -g @jackwener/opencli 2>/dev/null
```

> Windows PowerShell'de `which` yerine `Get-Command`, `npm` betik hatası verirse `npm.cmd` kullan.

**OpenCLI eklentisi:** Chrome Web Mağazası'ndan kurulduysa Chrome kendisi günceller. Elle yüklendiyse (zip) kullanıcıdan yeni `opencli-extension-v*.zip` dosyasını https://github.com/jackwener/opencli/releases adresinden indirmesini ve `chrome://extensions` sayfasında **Güncelle**ye basmasını iste. Sonra `opencli doctor` çalıştır.

**OpenCLI'ı olmayan masaüstü kullanıcıları:** v1.5.0'dan beri OpenCLI, XiaoHongShu ve Reddit için tercih edilen yoldur (ayrıca Bilibili altyazılarını ekler). Bu Türkçe sürümde ayrıca **erişilemeyen tüm siteler için genel yedektir.** Kullanıcıya bir kez öner. XiaoHongShu için OpenCLI yalnızca Chrome'da zaten var olan ve kullanıcının açıkça kontrol ettiği oturumu kullanabilir. Güncelleme asla kullanıcı adına giriş yapmamalı ve tarayıcı Cookie'si okumamalı:

> "Bu güncelleme OpenCLI desteği getiriyor. Kurayım mı? Kurulumdan sonra senin sadece Chrome Web Mağazası'nda bir kez 'Chrome'a ekle'ye basman gerekiyor. OpenCLI sadece Chrome'da zaten açık olan oturumunu kullanır. Giriş yapılmış oturum yoksa senin yerine giriş yapmam; XiaoHongShu için Cookie-Editor ile MCP / eski araçları ayarlarız."

Evet derse: `agent-reach install --system --channels opencli` çalıştır ve eklenti adımında kullanıcıya yol göster ([opencli-chrome-kurulum.md](opencli-chrome-kurulum.md)). Hayır derse mevcut yollarla her şey çalışmaya devam eder.

### Adım 4: Birlikte yaşama (eski araçları KALDIRMA)

**Kullanıcıda zaten olan araçları asla kaldırma.** Emekliye ayrılan yollar (ör. yt-dlp artık Bilibili için kullanılmıyor; xhs-cli artık varsayılan olarak kurulmuyor) hâlâ çalıştıkları yerde yedek olarak iş görür. Agent Reach bunların etrafından kendiliğinden dolaşır. Kaldırma kararı kullanıcınındır, senin değil.

### Adım 5: Doğrula

```bash
agent-reach version
agent-reach doctor
```

`agent-reach doctor` (metin modu) bulunan ajan skill klasörlerinde bir Agent Reach skill'i olduğundan da emin olur. Kullanıcının orada zaten bir skill'i varsa doctor yerel değişiklikleri ezmez, korur. Paketle gelen skill dosyalarını (varsayılan dil Türkçe) bilerek yenilemek istediğinde `agent-reach skill --install` kullan.

Doctor çıktısını kontrol et:

- Her kanal net bir mesajla ✅ / [!] gösteriyor ve birden fazla yolu olan kanallar (XiaoHongShu / Reddit / Bilibili / Twitter / Web) hangi yolun kullanıldığını söylüyor.
- Daha önce çalışan bir kanal şimdi [X] / hata gösteriyorsa mesaj tam çözümü içerir (ör. venv'i yeniden kurma talimatı). Onu uygula, tekrar kontrol et.
- `--json` aynı veriyi makinenin okuyacağı biçimde verir (her kanal için `active_backend`).

### Adım 6: Kullanıcıya raporla

Kullanıcıya Türkçe söyle:

1. Şu an hangi sürümde olduğu (`agent-reach version`)
2. Kaç kanalın çalıştığı ve birden fazla yolu olan her platformun hangi yolu kullandığı (doctor'dan)
3. Onun yapması gereken bir şey var mı (ör. Chrome eklentisini eklemek, XiaoHongShu MCP / eski araç kullanıyorsa Cookie-Editor ile elle dışa aktarma)
4. Bu güncellemede neler değişti (`check-update` çıktısındaki sürüm notları)

Bitti.
