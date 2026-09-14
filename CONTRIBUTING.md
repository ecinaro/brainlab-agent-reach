# Agent Reach'e katkı rehberi

Agent Reach'e katkı vermek istediğin için teşekkürler! Bu belge nasıl katkı verebileceğini anlatır.

> Bu repo, [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) projesinin Türkçe çatalıdır. Türkçe sürüme özel değişiklikler (çeviri, OpenCLI yedek yolu) buraya; genel hata düzeltmeleri ve yeni kanallar mümkünse orijinal projeye gönderilmelidir.

## Başlarken

1. Repoyu GitHub'da fork'la
2. Fork'unu bilgisayarına klonla
3. Katkın için yeni bir dal (branch) aç
4. Değişikliklerini yap
5. Testleri ve lint'i çalıştır
6. Pull request gönder

## Geliştirme ortamı

```bash
# Fork'unu klonla
git clone https://github.com/KULLANICI_ADIN/brainlab-agent-reach.git
cd brainlab-agent-reach

# Geliştirme modunda kur
pip install -e ".[dev]"

# pre-commit kancalarını kur (isteğe bağlı ama önerilir)
pre-commit install
```

## Kod stili

Kod kalitesi için şu araçları kullanıyoruz:

- **ruff**: Lint ve import sıralama
- **mypy**: Tip kontrolü
- **pytest**: Testler

PR göndermeden önce hepsini çalıştır:

```bash
# Lint
ruff check agent_reach tests
ruff format agent_reach tests

# Tip kontrolü
mypy agent_reach

# Testler
pytest
```

## Yeni kanal ekleme

Agent Reach tüm platformlar için ortak bir kanal arayüzü kullanır. Yeni bir platform eklemek için:

1. `agent_reach/channels/` altında yeni bir dosya oluştur
2. Kanal sözleşmesini uygula (örnek için mevcut kanallara bak)
3. `tests/test_channels.py` içine test ekle
4. Yeni kanalı `agent_reach/doctor.py` içine ekle
5. Dokümanları güncelle (Türkçe dokümanlar varsayılan; mümkünse `docs/README_en.md` de)

Platformun özel bir aracı yoksa ya da giriş/Cloudflare engeli varsa önce OpenCLI yedeğinin ([opencli-fallback.md](agent_reach/skill/references/opencli-fallback.md)) işi görüp görmediğine bak.

## Pull request kuralları

- Büyük yeniden yazımlar yerine **küçük ve odaklı değişiklikler** tercih edilir
- Yeni özellikler için test ekle
- Gerekirse dokümanları güncelle
- Mevcut kod stiline uy
- İlgili issue'ları belirt

## Hata bildirme

Hata bildirirken şunları ekle:

- Python sürümü
- İşletim sistemi
- Hatayı tekrar oluşturma adımları
- Beklenen ve gerçekleşen davranış
- Varsa hata mesajları
- OpenCLI ile ilgiliyse `opencli doctor` çıktısı

## Sorular?

Soruların için bir issue açabilirsin: https://github.com/ecinaro/brainlab-agent-reach/issues
