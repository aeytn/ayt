"""Embedding çağrıları.

Bu dosya BİTMİŞ durumda ve bilerek öyle bırakıldı: bir embedding API'sinin
nasıl çağrıldığını gösteren referans örneğin olsun diye. Diğer dosyalardaki
TODO'ları yazarken buraya bakabilirsin.
"""

from typing import List

import numpy as np
from openai import OpenAI

from app import config

_client = OpenAI(api_key=config.API_KEY, base_url=config.BASE_URL)


def embed_texts(texts: List[str], batch_size: int = 64) -> np.ndarray:
    """Metin listesini vektör matrisine çevirir.

    Dönen değer (len(texts), boyut) şeklinde float32 bir numpy dizisi.
    Batch'liyoruz çünkü tek istekte binlerce metin göndermek hem token
    limitine takılıyor hem de bir hata olduğunda her şeyi baştan
    hesaplatıyor.
    """
    if not texts:
        return np.zeros((0, 0), dtype=np.float32)

    vectors: List[List[float]] = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        response = _client.embeddings.create(
            model=config.EMBEDDING_MODEL,
            input=batch,
        )
        # API sırayı koruyor ama garanti altına almak için index'e göre diziyoruz
        ordered = sorted(response.data, key=lambda item: item.index)
        vectors.extend(item.embedding for item in ordered)

    matrix = np.array(vectors, dtype=np.float32)
    return normalize(matrix)


def normalize(matrix: np.ndarray) -> np.ndarray:
    """Vektörleri birim uzunluğa indirger.

    Bunu bir kez burada yaparsak, benzerlik hesabında kosinüs formülünün
    payda kısmına hiç ihtiyaç kalmıyor: normalize edilmiş iki vektörün
    nokta çarpımı zaten kosinüs benzerliğine eşit.
    """
    if matrix.size == 0:
        return matrix
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return matrix / norms
