"""Getirme kalitesi ölçümü.

SENİN YAZACAĞIN 4. DOSYA (ve mülakatta en çok konuşulacak olan).

RAG projelerinin çoğu burada ayrılıyor: "iyi çalışıyor gibi" diyenlerle
"k=4'te hit oranı 0.85, k=2'de 0.60" diyenler. İkincisi mühendislik.

    python -m app.eval
"""

import sys
from typing import List, Tuple

from app import config
from app.embed import embed_texts
from app.store import load_index, search

# Altın set: soru ve o sorunun cevabının geçtiği kaynak dosya.
# data/docs/ içine yeni doküman ekledikçe buraya da soru ekle.
ALTIN_SET: List[Tuple[str, str]] = [
    ("Fatura elli bin lirayı aşarsa kim onaylıyor?", "ornek-surec.md"),
    ("Onay verilmezse süreç ne kadar sonra iptal oluyor?", "ornek-surec.md"),
    ("İzin talebi hangi adımdan sonra İK'ya düşüyor?", "ornek-surec.md"),
]


def hit_at_k(k: int = None) -> float:
    """İlk k sonucun içinde doğru kaynağın çıkma oranı.

    TODO: burayı sen yaz.
      1. load_index ile indeksi oku.
      2. ALTIN_SET'teki soruları embed_texts ile vektöre çevir
         (hepsini tek çağrıda gönder, tek tek değil, hem hızlı hem ucuz).
      3. Her soru için search çalıştır, dönen parçaların source alanında
         beklenen dosya var mı bak.
      4. Doğru sayısı / toplam soru sayısını döndür.
    """
    k = k or config.TOP_K
    raise NotImplementedError("hit_at_k henüz yazılmadı")


def main() -> int:
    print(f"Altın set: {len(ALTIN_SET)} soru\n")
    for k in (1, 2, 4, 8):
        oran = hit_at_k(k)
        cubuk = "#" * int(oran * 20)
        print(f"  hit@{k:<2} {oran:5.2f}  {cubuk}")
    print(
        "\nchunk_size ve chunk_overlap değerlerini .env'den değiştirip"
        "\nyeniden indeksle, bu sayıların nasıl oynadığını gör."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
