from dotenv import load_dotenv
import os

load_dotenv()

QWEN_API_KEY = os.getenv("QWEN_API_KEY", "")
QWEN_BASE_URL = os.getenv("QWEN_BASE_URL", "")
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-plus")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")

# os.getenv(name, default_value)

TEMPERATURE = float(os.getenv("TEMPERATURE"))
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES"))
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "你是一个简洁、友好的中文AI助手。")

EMBEDDING_BACKEND = os.getenv("EMBEDDING_BACKEND", "ollama")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "embeddinggemma")

RAG_DOCS_DIR = os.getenv("RAG_DOCS_DIR", "docs")
RAG_CHUNK_SIZE = int(os.getenv("RAG_CHUNK_SIZE", "80"))
RAG_CHUNK_OVERLAP = int(os.getenv("RAG_CHUNK_OVERLAP", "20"))
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "3"))
RAG_MIN_SCORE = float(os.getenv("RAG_MIN_SCORE", "0.45"))
