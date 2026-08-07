import os
import redis
from dotenv import load_dotenv

load_dotenv()

# Força o uso de 127.0.0.1 para evitar problemas de resolução de "localhost" no Windows
REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")

# Tenta conectar ao Redis real. Se falhar, mostra o motivo exato.
try:
    redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
    _use_redis = True
    print("Conectado ao Redis com sucesso!")
except Exception as e:
    _use_redis = False
    _memory_db = {}
    print(f"⚠️ AVISO: Falha ao conectar ao Redis. Erro detalhado: {e}")
    print("Usando armazenamento em memória temporário para os testes.")

def get_user_step(jid: str) -> str:
    """Busca o passo atual do usuário (via Redis ou memória local)."""
    key = f"nina:particular:workflow:{jid}"
    if not _use_redis:
        return _memory_db.get(key, "awaiting_identity")
    
    step = redis_client.get(key)
    if not step:
        return "awaiting_identity"
    return step

def set_user_step(jid: str, step: str):
    """Salva o próximo passo do usuário (via Redis ou memória local)."""
    key = f"nina:particular:workflow:{jid}"
    if not _use_redis:
        _memory_db[key] = step
        return
        
    redis_client.set(key, step)