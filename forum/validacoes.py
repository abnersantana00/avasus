import datetime
from xml.dom import ValidationErr
# Função para validar o CPF


def validaData(data):
    try:
        data = datetime.date.fromisoformat(data)
    except ValueError or AttributeError:
        return False
    dias_ano = 365.2425
    idade = int((datetime.date.today() - data).days / dias_ano)
    if idade >= 18:
        return True
    else:
        return False