import os
from openai import OpenAI
from dotenv import load_dotenv
from app.services.extractor import get_patient_profile

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_nina_agent(jid: str, text: str) -> str:
    """
    Chama a LLM (OpenAI) injetando o contexto coletado pelo funil determinístico.
    """
    profile = get_patient_profile(jid)
    
    system_prompt = f"""
    Você é a Roberta, assistente virtual da Clínica Vittamed. 
    O paciente já passou pela triagem inicial. Seguem os dados coletados:
    - Nome: {profile.get('name')}
    - Cidade: {profile.get('city')}
    - Sintomas/Queixa: {profile.get('symptoms')}
    - Duração do problema: {profile.get('duration')}
    
    Seja acolhedora, empática e ajude o paciente a finalizar o agendamento da consulta ou tirar dúvidas finais com base nesses dados.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Desculpe, tive um pequeno problema técnico. Como posso ajudar com o seu agendamento?"