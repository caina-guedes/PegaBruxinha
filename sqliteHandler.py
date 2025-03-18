import sqlite3
from datetime import datetime
import sys
import re
from utils import validar_numero, validar_data, normalizar_data
from backDeLinhas import salva_linha, lista_linha
from funcoesBancoDeDados import exec, ja_liguei

comando  =  sys.argv[1].lower()  if  len(sys.argv)  >  1  else  ""


def salvar_chamada( numero , data_hora = None):
    """Salva uma chamada no banco de dados"""
    if data_hora_norm := normalizar_data(data_hora, 'entradaNoBanco'):
        data_hora = data_hora_norm
    elif not data_hora:
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        print("❌ Data inválida. Use o formato: AAAA-MM-DD HH:MM:SS você passou: ", data_hora)
        return
    
    if not validar_numero(numero):
        print("❌ Número inválido. Use o formato: 11987654321 você passou: ", numero)
        return
    try:
        exec(f"INSERT INTO chamadas (numero, data_hora) VALUES ({numero}, '{data_hora}')")
        print(f"Chamada salva: {numero} em {data_hora}")
    except sqlite.Error as e:
        print(f"❌ Erro ao tentar salvar chamada com os dados data: '{data_hora}' e número : {numero} o banco de dados: {e}")
        return


def listar_chamadas(numero='', data=''):
    """Lista chamadas filtradas por número ou data"""
    query = "SELECT * FROM chamadas WHERE 1=1"
    if numero:
        query += f" AND numero = {numero}"
    if data:
        data_norm = normalizar_data(data, '')
        if not data_norm:
            print("❌ Data inválida. Use o formato: AAAA-MM-DD HH:MM:SS a data que você enviou foi ", data)
            return
        data = data_norm
        query += f" AND data_hora LIKE '{data}%'"

    try:
        chamadas = exec(query,mostrar=True)
        if chamadas:
            for chamada in chamadas:
                print(f"Número: {chamada[1]} | Data/Hora: {chamada[2]}")
        else:
            print("Nenhuma chamada encontrada.")
    except sqlite3.Error as e:
        print(f"❌ Erro ao acessar o banco de dados: {e}")



if __name__ == "__main__":
    if comando == "ajuda":
        print("""
        📞 Ajuda:
        salvar <numero> [data] - Salva uma chamada para o número especificado. Se a data não for informada, a data atual será usada.
        ja_liguei <numero> - Verifica se o número já foi chamado.
        listar [numero] [data] - Lista todas as chamadas. Se um número for informado, lista as chamadas para esse número. Se uma data for informada, lista as chamadas naquela data.
        """)

    if comando == "ja_liguei":
        if len(sys.argv) == 3:
            if ja_liguei(sys.argv[2]):
                print(f"📞 Já liguei para o número {sys.argv[2]}")
            else:
                print(f"📵 Nunca liguei para o número {sys.argv[2]}")
        else:
            print("📌 Uso: python sqliteHandler.py ja_liguei <numero>")
    if comando == "listar":
        if len(sys.argv) == 2:
            listar_chamadas()
        elif len(sys.argv) == 3:
            if sys.argv[2].isdigit():
                print('cheguei na opcao de listar que deve vir um numero e o argumento é: ', sys.argv[2])
                listar_chamadas(numero=sys.argv[2])
            elif normalizar_data(sys.argv[2], ''):
                #print('cheguei na opcao de listar que deve vir uma data e o argumento é: ', sys.argv[2])
                data_norm = normalizar_data(sys.argv[2], '')
                listar_chamadas(data=data_norm)
            else:
                print("você passou argumento inválido para listar não é data válida nem número válido")
        elif len(sys.argv) == 4:
            if sys.argv[2].isdigit() and normalizar_data(sys.argv[3], ''):
                listar_chamadas(sys.argv[2], normalizar_data(sys.argv[3]))
            elif sys.argv[3].isdigit() and not normalizar_data(sys.argv[2], ''):
                print('data inválida a data fornecida foi: ', sys.argv[2])
            elif not sys.argv[2].isdigit() and normalizar_data(sys.argv[3], ''):
                print('numero inválido o numero fornecido foi: ', sys.argv[2])
            else:
                print('numero e data inválidos o numero fornecido foi: ', sys.argv[2], ' e a data foi: ', sys.argv[3])
        else:
            print("📌 Uso: python sqliteHandler.py listar [numero] [data]")            
    
    if comando == "salvar":
        if len(sys.argv) == 3:
            salvar_chamada(sys.argv[2])
        elif len(sys.argv) == 4:
            salvar_chamada(sys.argv[2],sys.argv[3])
        else:
            print("📌 Uso: python sqliteHandler.py salvar <numero> [data]")
    if comando == "salvar_linha":
        """preciso melhorar bastante essa parte aqui para aceitar argumentos vazios e coisas do genero"""
        if 4 < len(sys.argv) <= 10:
            #print("📞 Linha salva: {nome_empresa} "        
            salva_linha(*sys.argv[1:])
        else:
            print('o tamanho do sys.argv é',len(sys.argv))
            print("📌 Uso: python sqliteHandler.py salvar_linha <lista_numero_1> <lista_numero_2> <nome_empresa> <resultado> <emailObtidoEmLigacao> <dataPrimeiroEmail> <dataSegundoEmail> <dataTerceiroEmail>")
    if comando == "listar_linhas":
        if len(sys.argv) == 2:
            lista_linha()
        elif len(sys.argv) == 3:
            if validar_numero(sys.argv[2]):
                print('validei o numero aquiiii')
                lista_linha(telefone = sys.argv[2])
            else:
                lista_linha(empresa = sys.argv[2])
        elif len(sys.argv) == 4:
            lista_linha(sys.argv[2], sys.argv[3])
        else:
            print("📌 Uso: python sqliteHandler.py listar_linhas [telefone] [empresa]")
    # Fechar a conexão
    
# Salvar uma chamada
# python3 sqliteHandler.py salvar <numero> [data]
# exemplo
# python3 sqliteHandler.py salvar 11987654321
# python3 sqliteHandler.py salvar 11987654321 '2021-07-01 12:00:00'
# verificar se ja liguei para um número específico
# python3 sqliteHandler.py ja_liguei <numero>
# exemplo
# python3 sqliteHandler.py ja_liguei 11987654321
# Listar chamadas
# python3 sqliteHandler.py listar [numero] [data]
# exemplo
# python3 sqliteHandler.py listar
# python3 sqliteHandler.py listar 11987654321
# python3 sqliteHandler.py listar 2021-07-01
# Salvar uma linha
# python3 sqliteHandler.py salvar_linha <lista_numero_1> <lista_numero_2> <nome_empresa> <resultado> 
#  <emailObtidoEmLigacao> <dataPrimeiroEmail> <dataSegundoEmail> <dataTerceiroEmail>
# exemplo
# python3 sqliteHandler.py salvar_linha 11987654321 11987654322 'Empresa 1' 'Contato 1' 
# '2021-07-01' '2021-07-02' '2021-07-03'
# Listar linhas
# python3 sqliteHandler.py listar_linhas [telefone] [empresa]
# exemplo
# python3 sqliteHandler.py listar_linhas
# python3 sqliteHandler.py listar_linhas 11987654321
# python3 sqliteHandler.py listar_linhas 'Empresa 1'
# python3 sqliteHandler.py listar_linhas 11987654321 'Empresa 1'
# Ajuda
# python3 sqliteHandler.py ajuda