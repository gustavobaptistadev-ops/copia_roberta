# Dicionário em memória para guardar o perfil coletado de cada paciente durante os testes
_PATIENT_PROFILES = {}

def extract_and_store_data(jid: str, current_step: str, text: str):
    """
    Extrai e armazena os dados informados pelo paciente conforme ele avança no funil.
    """
    if jid not in _PATIENT_PROFILES:
        _PATIENT_PROFILES[jid] = {"name": None, "city": None, "symptoms": None, "duration": None}
        
    profile = _PATIENT_PROFILES[jid]
    
    if current_step == "awaiting_identity":
        profile["name"] = text
    elif current_step == "awaiting_city":
        profile["city"] = text
    elif current_step == "awaiting_symptoms":
        profile["symptoms"] = text
    elif current_step == "awaiting_interest":
        profile["duration"] = text

def get_patient_profile(jid: str) -> dict:
    return _PATIENT_PROFILES.get(jid, {})