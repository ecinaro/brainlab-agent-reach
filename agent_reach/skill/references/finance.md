# Finans ve piyasa verileri

Xueqiu hisse fiyatları, arama ve popüler içerik. Fiyatlar gecikmeli olabilir; yatırım
tavsiyesi değildir.

## Önce durumu kontrol et

```bash
agent-reach doctor --json
```

`xueqiu.active_backend` doluysa o backend'i kullan; değerin `null` olması yalnızca Doctor'ın
canlı içerik doğrulamasını tamamlamadığı anlamına gelir. Xueqiu giriş yapılmış bir oturum veya
asgari bir cookie gerektirir; HTTP 400'ü "hisse yok" diye yorumlama.

## OpenCLI (masaüstünde Chrome'da zaten giriş varsa öncelikli)

```bash
# Mevcut oturumu doğrula
opencli xueqiu whoami -f yaml

# Hisse araması ve anlık fiyat
opencli xueqiu search "英伟达" -f yaml
opencli xueqiu stock NVDA -f yaml

# Popüler içerik ve popüler hisseler
opencli xueqiu hot -f yaml
opencli xueqiu hot-stock -f yaml

# Tüm salt-okunur komutları gör
opencli xueqiu --help
```

> Xueqiu Çince bir platformdur: şirket adıyla ararken Çince adı kullan (ör. NVIDIA için
> `英伟达`); hisse kodu biliniyorsa doğrudan `stock NVDA` gibi kodla sorgula.

OpenCLI yalnızca kullanıcının zaten açık ve kendi kontrolündeki tarayıcı oturumunu kullanır.
`opencli xueqiu login` komutunu otomatik çalıştırma; oturum yoksa kullanıcıdan önce Chrome'da
giriş yapmasını iste veya Xueqiu için gereken asgari cookie'yi açıkça içe aktar:

```bash
agent-reach configure --from-browser chrome --platform xueqiu
```

Bu yapılandırma yalnızca `xq_a_token` değerini okur ve kaydeder; başka platformların
cookie'lerini toplamaz.

## Doğrulama ve hata yönetimi

- Başarı ölçütü: hisse adı, kodu, fiyatı veya boş olmayan bir içerik listesi dönmesi. Exit 0
  olup alanların boş gelmesi başarı sayılmaz.
- HTTP 400 genellikle oturum/cookie sorunudur; hisse kodunun olmadığı anlamına gelmez.
- `whoami` başarılı ama `stock`/`hot` başarısızsa bunu adapter ayrıştırma veya platform API
  sorunu olarak raporla; "giriş yok" diye yanlış teşhis koyma.
