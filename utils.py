from datetime import datetime
import re

def validar_numero(numero):
    """Valida se o número contém apenas dígitos (ex: 11987654321)"""
    return bool(re.fullmatch(r'\d{10,11}', numero))

def normalizar_data(data_str, modo):
    formatos = [
        "%Y-%m-%d",                # 2024-03-09
        "%d/%m/%Y",                # 09/03/2024
        "%d-%m-%Y",                # 09-03-2024
        "%Y/%m/%d",                # 2024/03/09
        "%Y%m%d",                  # 20240309
        "%d %b %Y",                # 09 Mar 2024
        "%d %B %Y",                # 09 Março 2024 (português)
        "%b %d, %Y",               # Mar 09, 2024 (inglês)
        "%B %d, %Y",               # March 09, 2024 (inglês completo)
        "%Y-%m-%d %H:%M:%S",       # 2024-03-09 15:30:45
        "%d/%m/%Y %H:%M:%S",       # 09/03/2024 15:30:45
        "%d-%m-%Y %H:%M:%S",       # 09-03-2024 15:30:45
        "%Y/%m/%d %H:%M:%S",       # 2024/03/09 15:30:45
        "%Y%m%d %H:%M:%S",         # 20240309 15:30:45
        "%d %b %Y %H:%M:%S",       # 09 Mar 2024 15:30:45
        "%d %B %Y %H:%M:%S",       # 09 Março 2024 15:30:45 (português)
        "%b %d, %Y %H:%M:%S",      # Mar 09, 2024 15:30:45 (inglês)
        "%B %d, %Y %H:%M:%S",      # March 09, 2024 15:30:45 (inglês completo)
    ]
    data_str = data_str.strip() # remove espaços no início e no fim
    if not data_str:
        return False
    for formato in formatos:
        try:
            data = datetime.strptime(data_str, formato)
            if modo == 'entradaNoBanco':
                return data.strftime("%Y-%m-%d %H:%M:%S")  # Formato padronizado
            else:
                return data.strftime("%Y-%m-%d")  # Formato AAAA-MM-DD
        except ValueError:
            continue

    print(f"❌ Formato inválido: {data_str}")
    return False

def validar_data(data_hora):
    """Valida se a data está no formato AAAA-MM-DD HH:MM:SS"""
    try:
        datetime.strptime(data_hora, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False
