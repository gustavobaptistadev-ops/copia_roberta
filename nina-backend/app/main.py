from fastapi import FastAPI
from app.api.routes.webhook import router as webhook_router

app = FastAPI(title="Roberta IA - Clínica Vittamed")

# Inclui as rotas da API
app.include_router(webhook_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"status": "online", "message": "Roberta IA backend rodando com sucesso!"}