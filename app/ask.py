"""Soru sorma: arama + prompt kurma + cevap.

SENİN YAZACAĞIN 3. DOSYA.

Burada test yok, çünkü çıktı bir dil modelinden geliyor ve deterministik
değil. Kaliteyi `python -m app.eval` ile ölçüyorsun. Bu dosyada asıl iş
prompt'u kurmak; RAG'de cevabın uydurma olup olmaması büyük ölçüde burada
belirleniyor.

    python -m app.ask "Fatura onay limiti nedir?"
"""

import sys
from typing import List

from openai import OpenAI

from app import config
from app.embed import embed_texts
from app.store import SearchHit, load_index, search

_client = OpenAI(api_key=config.API_KEY, base_url=config.BASE_URL)


def prompt_kur(soru: str, hits: List[SearchHit]) -> List[dict]:
    """Modele gidecek mesajları hazırlar.

    TODO: burayı sen yaz. Bir sistem mesajı ve bir kullanıcı mesajı
    döndürmeli.

    Sistem mesajında olması gerekenler:
      - Yalnızca verilen bağlamdaki bilgiyi kullan.
      - Bağlamda cevap yoksa "bu dokümanlarda bulamadım" de. Uydurma.
        (Bu tek cümle, RAG sistemlerinde hatalı cevapların büyük kısmını
        önlüyor. Modele "bilmiyorum deme izni" vermezsen uyduruyor.)
      - Cevabı Türkçe ver ve hangi kaynağı kullandığını [1], [2] diye
        numarayla belirt.

    Kullanıcı mesajında olması gerekenler:
      - Numaralanmış bağlam parçaları; her birinin başında kaynak dosya adı.
      - En sonda kullanıcının sorusu.

    İpucu: bağlamı sorunun ÜSTÜNE koy. Uzun bağlamlarda modeller sona yakın
    yazılanı daha iyi takip ediyor; soru en sonda dursun.
    """
    raise NotImplementedError("prompt_kur henüz yazılmadı")


def sor(soru: str) -> str:
    chunks, vektorler = load_index()
    sorgu_vektoru = embed_texts([soru])[0]
    hits = search(sorgu_vektoru, vektorler, chunks)

    mesajlar = prompt_kur(soru, hits)
    cevap = _client.chat.completions.create(
        model=config.CHAT_MODEL,
        messages=mesajlar,
        temperature=0.1,  # süreç sorusunda yaratıcılık istemiyoruz
    )
    metin = cevap.choices[0].message.content

    satirlar = [metin, "", "Kaynaklar:"]
    for i, hit in enumerate(hits, start=1):
        onizleme = hit.chunk.text[:60].replace("\n", " ")
        satirlar.append(f"  [{i}] {hit.chunk.source} — {onizleme}... (benzerlik {hit.score:.2f})")
    return "\n".join(satirlar)


def main() -> int:
    if len(sys.argv) < 2:
        print('Kullanım: python -m app.ask "sorunuz"')
        return 1
    print(sor(" ".join(sys.argv[1:])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
