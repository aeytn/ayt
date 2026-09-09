"""Doküman parçalama.

SENİN YAZACAĞIN 1. DOSYA.

Neden ilk bu: RAG'in cevap kalitesini en çok belirleyen adım burası. Kötü
parçalanmış bir doküman, dünyanın en iyi modelinde bile yarım cevap üretir.

Sözleşme `tests/test_chunk.py` içinde yazılı. Testleri çalıştır, kırmızıdan
yeşile getir:

    pytest tests/test_chunk.py -v
"""

from dataclasses import dataclass
from typing import List

from app import config


@dataclass
class Chunk:
    """Bir doküman parçası ve nereden geldiği bilgisi."""

    text: str
    source: str  # dosya adı
    index: int  # dokümanın kaçıncı parçası


def split_text(text: str, size: int = None, overlap: int = None) -> List[str]:
    """Metni örtüşmeli parçalara böler.

    Kurallar (testler bunları kontrol ediyor):
      1. Hiçbir parça `size` karakterden uzun olamaz.
      2. Ardışık iki parça `overlap` kadar örtüşür, yani ikinci parça
         birincinin son `overlap` karakterini de içerir.
      3. Mümkünse cümle ortasından bölme: `size` sınırına yaklaşırken
         geriye doğru en yakın cümle sonunu (. ! ? veya satır sonu) ara,
         orada böl. Cümle sonu bulunamazsa sert bölme yap.
      4. Boş ya da yalnızca boşluktan oluşan parça döndürme.

    TODO: burayı sen yaz.

    İpucu: bir imleç (cursor) tut, döngüde ilerlet. Her adımda önce
    `text[cursor : cursor + size]` aday parçayı al, sonra 3. kuralı uygula,
    en son imleci `bitiş - overlap` konumuna taşı. Sonsuz döngüye düşmemek
    için imlecin her turda mutlaka ilerlediğinden emin ol.
    """
    size = size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP
    raise NotImplementedError("split_text henüz yazılmadı")


def chunk_document(text: str, source: str) -> List[Chunk]:
    """Bir dokümanı Chunk nesnelerine çevirir.

    TODO: split_text sonucunu Chunk listesine dönüştür, index'leri sırayla ver.
    """
    raise NotImplementedError("chunk_document henüz yazılmadı")
