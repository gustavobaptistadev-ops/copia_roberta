# Lista de cidades atendidas que liberam o funil da clínica
_SERVED_CITIES = ["brasília", "brasilia", "taguatinga", "ceilândia", "ceilandia", "asa norte", "asa sul"]

def try_handle_particular_workflow(jid: str, text: str, current_step: str) -> str | None:
    """
    Controla o fluxo determinístico da conversa antes de acionar a LLM.
    Baseado na arquitetura da Roberta (Vittamed).
    """
    text_lower = text.strip().lower()
    
    # Passo 1: O paciente acabou de dar o nome ou mandou a primeira mensagem
    if current_step == "awaiting_identity":
        return "Entendi! E de qual cidade você fala?"
        
    # Passo 2: O paciente informou a cidade, validamos se está na lista
    if current_step == "awaiting_city":
        if any(city in text_lower for city in _SERVED_CITIES):
            return "Certo! Me conta: o que tem te incomodado na sua saúde ultimamente — alguma questão na pele, queda de cabelo, manchas ou outra coisa?"
        else:
            return "No momento, atendemos apenas nas unidades da região de Brasília."
            
    # Passo 3: O paciente informou os sintomas/queixa
    if current_step == "awaiting_symptoms":
        return "Poxa, imagino o quanto isso incomoda. Há quanto tempo você percebe esses sintomas?"
        
    # Passo 4: O paciente informou o tempo dos sintomas, perguntamos o interesse (ex: consulta particular)
    if current_step == "awaiting_interest":
        return "Compreendi perfeitamente. Para cuidarmos disso da melhor forma, você prefere agendar uma avaliação presencial ou telemedicina?"
        
    return None