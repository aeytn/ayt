"""Vektör deposu sözleşmesi. API anahtarı gerektirmez, sahte vektörlerle çalışır."""

import numpy as np
import pytest

from app.chunk import Chunk
from app.store import SearchHit, load_index, save_index, search


def sahte_chunklar():
    return [
        Chunk(text="fatura onay limiti", source="a.md", index=0),
        Chunk(text="izin talebi süreci", source="a.md", index=1),
        Chunk(text="satın alma talebi", source="b.md", index=2),
    ]


def sahte_vektorler():
    """Birim uzunlukta, birbirine dik üç vektör."""
    return np.eye(3, dtype=np.float32)


def test_kaydet_ve_geri_yukle(tmp_path):
    yol = tmp_path / "index.npz"
    chunklar, vektorler = sahte_chunklar(), sahte_vektorler()

    save_index(chunklar, vektorler, path=yol)
    okunan_chunklar, okunan_vektorler = load_index(path=yol)

    assert [c.text for c in okunan_chunklar] == [c.text for c in chunklar]
    assert [c.source for c in okunan_chunklar] == [c.source for c in chunklar]
    assert [c.index for c in okunan_chunklar] == [c.index for c in chunklar]
    assert np.allclose(okunan_vektorler, vektorler)


def test_uyumsuz_uzunluk_hata_verir(tmp_path):
    with pytest.raises(ValueError):
        save_index(sahte_chunklar(), np.eye(2, dtype=np.float32), path=tmp_path / "x.npz")


def test_indeks_yoksa_anlasilir_hata(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_index(path=tmp_path / "olmayan.npz")


def test_arama_en_yakini_ilk_donduruyor():
    chunklar, vektorler = sahte_chunklar(), sahte_vektorler()
    # İkinci vektöre birebir eşit bir sorgu
    sorgu = np.array([0.0, 1.0, 0.0], dtype=np.float32)

    sonuclar = search(sorgu, vektorler, chunklar, top_k=2)

    assert len(sonuclar) == 2
    assert all(isinstance(s, SearchHit) for s in sonuclar)
    assert sonuclar[0].chunk.text == "izin talebi süreci"
    assert sonuclar[0].score > sonuclar[1].score, "skorlar azalan sırada olmalı"
    assert sonuclar[0].score == pytest.approx(1.0, abs=1e-5)


def test_top_k_parca_sayisini_asamaz():
    chunklar, vektorler = sahte_chunklar(), sahte_vektorler()
    sorgu = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    sonuclar = search(sorgu, vektorler, chunklar, top_k=10)
    assert len(sonuclar) == 3
