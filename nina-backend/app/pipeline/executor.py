from app.services.particular_workflow import try_handle_particular_workflow
from app.core.redis_client import get_user_step, set_user_step
from app.core.agent import run_nina_agent
from app.services.extractor import extract_and_store_data

class PipelineExecutor:
    def __init__(self, jid: str, text: str):
        self.jid = jid
        self.text = text
        self.current_step = get_user_step(jid)

    def run(self) -> str:
        # Extrai os dados informados no passo atual antes de mudar de estado
        extract_and_store_data(self.jid, self.current_step, self.text)
        
        # Tenta responder pelo funil determinístico
        response = try_handle_particular_workflow(self.jid, self.text, self.current_step)
        
        if response:
            # Avança os estados do funil sequencialmente
            if self.current_step == "awaiting_identity":
                set_user_step(self.jid, "awaiting_city")
            elif self.current_step == "awaiting_city":
                set_user_step(self.jid, "awaiting_symptoms")
            elif self.current_step == "awaiting_symptoms":
                set_user_step(self.jid, "awaiting_interest")
            elif self.current_step == "awaiting_interest":
                set_user_step(self.jid, "completed")
                
            return response
            
        # Se o workflow retornar None (funil concluído), a IA assume com o perfil completo
        return run_nina_agent(self.jid, self.text)