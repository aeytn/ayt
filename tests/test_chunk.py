"""split_text ve chunk_document sözleşmesi.

Bu testler şu an kırmızı. Görevin hepsini yeşile çevirmek.
Testleri değiştirme, kodu değiştir.
"""

import pytest

from app.chunk import Chunk, chunk_document, split_text

METIN = (
    "Fatura sisteme girildiğinde tutar kontrolü yapılır. "
    "Tutar elli bin lirayı aşmıyorsa birim yöneticisi onayına düşer. "
    "Tutar elli bin lirayı aşıyorsa mali işler direktörü de onaylamalıdır. "
    "İki onay tamamlanmadan ödeme adımı tetiklenmez. "
    "Onay yedi gün içinde verilmezse süreç otomatik olarak iptal edilir."
)


def test_hicbir_parca_size_asmaz():
    parcalar = split_text(METIN, size=120, overlap=20)
    assert parcalar, "en az bir parça dönmeli"
    assert all(len(p) <= 120 for p in parcalar)


def test_tum_metin_kapsaniyor():
    """Parçaları birleştirince orijinal metnin her kelimesi bulunmalı."""
    parcalar = split_text(METIN, size=120, overlap=20)
    birlesik = " ".join(parcalar)
    for kelime in METIN.split():
        assert kelime in birlesik, f"'{kelime}' hiçbir parçada yok"


def test_parcalar_ortusuyor():
    parcalar = split_text(METIN, size=120, overlap=30)
    if len(parcalar) < 2:
        pytest.skip("örtüşmeyi ölçmek için en az iki parça gerekli")
    for onceki, sonraki in zip(parcalar, parcalar[1:]):
        kuyruk = onceki[-30:].strip()
        assert kuyruk and kuyruk in sonraki, "ardışık parçalar örtüşmüyor"


def test_bos_parca_donmez():
    parcalar = split_text("   \n\n   ", size=100, overlap=10)
    assert parcalar == []


def test_kisa_metin_tek_parca():
    parcalar = split_text("Kısa bir cümle.", size=500, overlap=50)
    assert parcalar == ["Kısa bir cümle."]


def test_cumle_sonundan_bolmeyi_tercih_eder():
    """size sınırı cümlenin ortasına denk geldiğinde geriye doğru bölmeli."""
    metin = "Birinci cümle burada bitiyor. İkinci cümle epeyce uzun sürüyor."
    parcalar = split_text(metin, size=40, overlap=5)
    assert parcalar[0].rstrip().endswith("."), (
        f"ilk parça cümle sonunda bitmeli, şu an: {parcalar[0]!r}"
    )


def test_chunk_document_kaynak_ve_index_verir():
    parcalar = chunk_document(METIN, source="ornek-surec.md")
    assert all(isinstance(p, Chunk) for p in parcalar)
    assert all(p.source == "ornek-surec.md" for p in parcalar)
    assert [p.index for p in parcalar] == list(range(len(parcalar)))
