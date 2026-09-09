"""Vektör deposu: parçaları ve vektörlerini diske yazar, arama yapar.

SENİN YAZACAĞIN 2. DOSYA.

Sözleşme `tests/test_store.py` içinde. Bu dosyada API çağrısı yok, saf
numpy; bu yüzden testler internetsiz ve anahtarsız çalışıyor.
"""

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np

from app import config
from app.chunk import Chunk


@dataclass
class SearchHit:
    chunk: Chunk
    score: float


def save_index(chunks: List[Chunk], vectors: np.ndarray, path=None) -> None:
    """Parçaları ve vektörlerini tek bir .npz dosyasına yazar.

    TODO: np.savez ile kaydet. Chunk bir dataclass olduğu için doğrudan
    yazılamaz; text, source ve index alanlarını ayrı dizilere aç.
    Kaydetmeden önce vectors.shape[0] == len(chunks) olduğunu doğrula,
    değilse ValueError fırlat. Bu kontrol seni ileride saatlerce
    sürecek bir hata avından kurtaracak.
    """
    path = path or config.INDEX_PATH
    raise NotImplementedError("save_index henüz yazılmadı")


def load_index(path=None) -> Tuple[List[Chunk], np.ndarray]:
    """Diskten indeksi okur.

    TODO: np.load ile oku, Chunk listesini geri kur, (chunks, vectors)
    döndür. Dosya yoksa anlaşılır bir FileNotFoundError ver: kullanıcıya
    "önce python -m app.ingest çalıştır" demeli.
    """
    path = path or config.INDEX_PATH
    raise NotImplementedError("load_index henüz yazılmadı")


def search(query_vector: np.ndarray, vectors: np.ndarray, chunks: List[Chunk],
           top_k: int = None) -> List[SearchHit]:
    """Sorguya en yakın parçaları benzerlik sırasına göre döndürür.

    TODO: burayı sen yaz. Vektörler embed.normalize ile birim uzunlukta
    olduğu için kosinüs benzerliği tek satır: vectors @ query_vector.
    Sonra np.argsort ile en yüksek top_k skoru al ve SearchHit listesi kur.

    Dikkat: argsort küçükten büyüğe sıralar. Ters çevirmeyi unutma,
    yoksa en alakasız parçaları döndürürsün ve bu sessizce yanlış çalışan
    bir hata olur, hiçbir yerde patlamaz.
    """
    top_k = top_k or config.TOP_K
    raise NotImplementedError("search henüz yazılmadı")
