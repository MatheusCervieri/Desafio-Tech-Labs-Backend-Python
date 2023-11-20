import re
from datetime import datetime

def validar_cpf(cpf):
    cpf_pattern = re.compile(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$')
    return bool(cpf_pattern.match(cpf))

def validar_data_nascimento(data_nascimento):
    try:
        datetime.strptime(data_nascimento, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
def validar_estado_civil(estado_civil):
    estados_civis_validos = ['solteiro', 'casado', 'divorciado', 'viuvo']
    return estado_civil.lower() in estados_civis_validos