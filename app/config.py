"""Merkezi ayarlar. Sabitleri koda gömmek yerine tek yerde topluyoruz."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Dizinler
ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "data" / "docs"
INDEX_PATH = ROOT / "data" / "index.npz"

# API. base_url değiştirilebilir olduğu için OpenAI, Groq, Together veya
# yerelde çalışan Ollama ile aynı kod çalışır.
API_KEY = os.getenv("API_KEY", "")
BASE_URL = os.getenv("BASE_URL", "https://api.openai.com/v1")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")

# Parçalama. Bu iki sayı cevap kalitesini en çok etkileyen ayar;
# değiştirdikten sonra `python -m app.eval` ile ölç.
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "80"))

# Kaç parça context olarak verilecek
TOP_K = int(os.getenv("TOP_K", "4"))
