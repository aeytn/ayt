"""Dokümanları okur, parçalar, embedding'lerini çıkarır ve indeksi kaydeder.

Bu dosya BİTMİŞ: orkestrasyon katmanı, yani senin yazacağın parçaları
birbirine bağlayan yer. Çalıştırdığında chunk.py ve store.py'yi
tamamlamadıysan NotImplementedError alacaksın; sıra böyle ilerliyor.

    python -m app.ingest
"""

import sys
from typing import List

from app import config
from app.chunk import Chunk, chunk_document
from app.embed import embed_texts
from app.store import save_index

DESTEKLENEN = {".md", ".txt"}


def dokumanlari_oku() -> List[Chunk]:
    if not config.DOCS_DIR.exists():
        raise FileNotFoundError(f"Doküman klasörü yok: {config.DOCS_DIR}")

    chunks: List[Chunk] = []
    dosyalar = sorted(
        p for p in config.DOCS_DIR.rglob("*") if p.suffix.lower() in DESTEKLENEN
    )
    if not dosyalar:
        raise FileNotFoundError(
            f"{config.DOCS_DIR} içinde .md veya .txt dosyası bulunamadı"
        )

    for yol in dosyalar:
        metin = yol.read_text(encoding="utf-8")
        parcalar = chunk_document(metin, source=yol.name)
        chunks.extend(parcalar)
        print(f"  {yol.name}: {len(parcalar)} parça")

    return chunks


def main() -> int:
    print(f"Dokümanlar okunuyor: {config.DOCS_DIR}")
    chunks = dokumanlari_oku()
    print(f"Toplam {len(chunks)} parça.")

    print(f"Embedding çıkarılıyor ({config.EMBEDDING_MODEL})...")
    vektorler = embed_texts([c.text for c in chunks])

    save_index(chunks, vektorler)
    print(f"İndeks kaydedildi: {config.INDEX_PATH}")
    print(f"Boyut: {vektorler.shape[0]} vektör x {vektorler.shape[1]} boyut")
    return 0


if __name__ == "__main__":
    sys.exit(main())
