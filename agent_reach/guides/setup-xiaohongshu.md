# XiaoHongShu kurulum rehberi

## Ne işe yarar?
XiaoHongShu notlarını okur ve arar. Masaüstünde önce OpenCLI kullanılır, sunucuda
[xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp);
xhs-cli sadece zaten kurmuş kullanıcılar için eski bir yedek yoldur.

## Ön koşullar
- OpenCLI: Chrome'da zaten var olan ve kullanıcının açıkça kontrol ettiği bir XiaoHongShu oturumu
- xiaohongshu-mcp / eski araçlar: Cookie-Editor tarayıcı eklentisi

## Kimlik doğrulama sınırı

Agent Reach XiaoHongShu'ya kullanıcı adına giriş yapmaz ve tarayıcı Cookie'si okumaz.

OpenCLI yalnızca Chrome'da zaten var olan ve kullanıcının açıkça kontrol ettiği oturumu kullanır.
`agent-reach configure xhs-cookies` Cookie'yi OpenCLI'a veya Chrome'a aktarmaz.
Hazır oturum yoksa otomatik giriş yapma; Cookie-Editor ile elle dışa aktarıp
xiaohongshu-mcp ya da eski araçları yapılandır:

1. Chrome'a [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) eklentisini kur
2. Kullanıcı dışa aktarılacak oturumu xiaohongshu.com üzerinde kendisi hazırlar
3. Cookie-Editor simgesine tıkla → Export → Header String
4. Dışa aktarılan metni ajana ver ve çalıştır:

```bash
agent-reach configure xhs-cookies
agent-reach doctor
```

Bu açık komut, kullanıcının verdiği xiaohongshu.com alan adına ait Cookie setini kaydeder/içe aktarır. Çalıştırmadan önce
Cookie adlarını ve kapsamını doğrula. xiaohongshu.com dışındaki alan adlarına ait Cookie'ler yok sayılır.

xiaohongshu-mcp konteyneri çalışıyorsa ayar komutu Cookie'yi konteynere aktarır; çalışmıyorsa sadece sahibinin
okuyabildiği (owner-only) yerel bir dosyaya yazar ve sonradan elle içe aktarma yolunu ekrana basar.

## Kullanım örnekleri

Önce `agent-reach doctor --json` çıktısındaki `active_backend`'e göre komutu seç. Eski xhs-cli örnekleri:

Not ara:
```bash
xhs search "anahtar kelime"
```

Not detayını oku:
```bash
xhs read NOTE_ID
```

Yorumları gör:
```bash
xhs comments NOTE_ID
```

OpenCLI aktifse:
```bash
opencli xiaohongshu search "anahtar kelime" -f yaml
```

## Sık sorulanlar

**S: Cookie'nin süresi mi doldu?**
C: Cookie-Editor ile tekrar elle dışa aktar, sonra
`agent-reach configure xhs-cookies` çalıştır ve gizli giriş istemine yapıştır.

**S: XiaoHongShu IP riski uyarısı mı veriyor?**
C: Konut (residential) proxy önerilir: `export HTTP_PROXY="http://user:pass@ip:port"`.

**S: xhs-cli sistemimi desteklemiyor mu?**
C: Python 3.10+ ve pipx'in kurulu olduğundan emin ol. Sonra `pipx install xiaohongshu-cli` çalıştır.

## Sunucu çözümü: Docker MCP

[xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) Docker çözümünü zaten kullanıyorsan o da çalışır:

```bash
docker run -d \
  --name xiaohongshu-mcp \
  -p 18060:18060 \
  xpzouying/xiaohongshu-mcp

mcporter config add xiaohongshu http://localhost:18060/mcp --scope home
```

Bu sunucu yolu yukarıdaki Cookie-Editor ile elle dışa aktarma akışını kullanır.
