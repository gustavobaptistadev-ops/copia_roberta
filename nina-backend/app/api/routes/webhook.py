from fastapi import APIRouter, HTTPException, Request
from app.pipeline.executor import PipelineExecutor

router = APIRouter()

@router.post("/nina/webhook")
async def receive_whatsapp_message(request: Request):
    """
    Recebe a mensagem do WhatsApp e executa o pipeline da Roberta.
    """
    try:
        body = await request.json()
        jid = body.get("jid")
        text = body.get("text")
        
        # Executa o pipeline de processamento
        pipeline = PipelineExecutor(jid=jid, text=text)
        response_text = pipeline.run()
        
        print(f"Mensagem de {jid}: {text} | Resposta da Roberta: {response_text}")
        
        return {
            "status": "success", 
            "response": response_text,
            "jid": jid
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro no pipeline: {str(e)}")