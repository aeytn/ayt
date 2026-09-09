# Süreç Asistanı

İş süreci dokümanları üzerinde soru cevaplayan bir RAG (retrieval-augmented generation) asistanı.

Bir kurumda yüzlerce süreç dokümanı olur: iş akışı tanımları, onay matrisleri, istisna kuralları. "Fatura 50 bin TL'yi aşarsa onaya kim giriyor?" sorusunun cevabı bu dokümanların birinde, üçüncü sayfada bir tabloda durur. Bu proje o soruyu doğal dille soruyor, ilgili paragrafları buluyor ve cevabı **kaynak göstererek** veriyor.

Proje, on dört yıllık BPM ve RPA geliştirme deneyimimin doğrudan içinden çıktı: elli üzerinde iş akışı geliştirdim ve her birinin dokümantasyonunu yazdım. Bu asistanın çözdüğü problem, o dokümanların içinde kaybolan bilgi.

## Ne yapıyor

```
Doküman (.md, .txt, .pdf)
        │
        ▼
   parçalama           ~500 karakterlik, örtüşmeli parçalar
        │
        ▼
   embedding           her parça için vektör, tek seferlik
        │
        ▼
   vektör deposu       .npz dosyası, disk üzerinde
        │
        ▼
   soru → embedding → kosinüs benzerliği → en yakın k parça
        │
        ▼
   LLM'e context olarak ver → cevap + kaynak referansı
```

## Kurulum

```bash
git clone https://github.com/aeytn/ayt.git
cd ayt
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env        # sonra .env içine API anahtarını yaz
```

## Kullanım

```bash
# 1. Dokümanları indeksle (data/docs/ altındaki her şeyi okur)
python -m app.ingest

# 2. Soru sor
python -m app.ask "Fatura onay limiti aşıldığında akış nereye gidiyor?"

# 3. Cevap kalitesini ölç
python -m app.eval
```

Örnek çıktı:

```
Cevap: 50.000 TL üzerindeki faturalar birim yöneticisi onayından sonra
mali işler direktörüne yönlendirilir. İki onay da alınmadan ödeme adımı
tetiklenmez.

Kaynaklar:
  [1] ornek-surec.md, "Onay Matrisi" bölümü (benzerlik 0.83)
  [2] ornek-surec.md, "İstisna Kuralları" bölümü (benzerlik 0.71)
```

## Tasarım kararları

**Neden harici vektör veritabanı yok?** İlk sürümde parça sayısı birkaç bini geçmiyor; numpy ile kosinüs benzerliği yeterli ve her adımı görünür kılıyor. Pinecone veya pgvector eklemek, ölçek gerçekten gerektiğinde anlamlı. Erken soyutlama, ne olduğunu anlamayı zorlaştırıyor.

**Neden örtüşmeli parçalama?** Süreç dokümanlarında bir kural çoğu zaman iki cümleye yayılır ("...onaya gider. Onay alınmazsa süreç iptal edilir."). Parçalar örtüşmezse ikinci cümle bağlamsız kalıyor ve model kuralı yarım okuyor.

**Neden cevabın yanında kaynak var?** Süreç sorularında yanlış cevabın maliyeti yüksek. Kaynak göstermeyen bir asistan, kullanıcıyı doğrulayamadığı bir cevaba mecbur bırakıyor.

**Neden ayrı bir değerlendirme adımı?** `app/eval.py` içinde cevabı bilinen soru seti var. Parçalama boyutunu veya k değerini değiştirdiğimde işlerin iyileşip iyileşmediğini hisle değil ölçerek görüyorum.

## Yol haritası

- [ ] PDF okuma (`pypdf`) — şu an yalnızca `.md` ve `.txt`
- [ ] Reranking: ilk 20 sonucu getirip cross-encoder ile 5'e indirmek
- [ ] PostgreSQL + pgvector'a geçiş, parça sayısı 10 bini aştığında
- [ ] Cevapların izlenmesi (latency, token maliyeti, kaynak isabeti)
- [ ] Soru cevap geçmişi üzerinden sık sorulan süreçleri raporlama

## Teknolojiler

Python · OpenAI uyumlu embedding ve chat API (base URL değiştirilebilir) · numpy · pytest

---

**Hatice Ayten Babaoğlu** — Yazılım mühendisi, 14 yıl BPM, RPA ve backend.
[LinkedIn](https://linkedin.com/in/aytenbabaoglu)
