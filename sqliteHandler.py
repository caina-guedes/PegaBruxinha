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
    if data_hora:
        data_hora_norm = normalizar_data(data_hora, modo = 'entradaNoBanco')
        if not data_hora_norm:
            print("❌ Data inválida. Use o formato: AAAA-MM-DD HH:MM:SS a sua data foi:", data_hora)
            return
        data_hora = data_hora_norm

    if not validar_numero(numero):
        print("❌ Número inválido. Use o formato: 11987654321")
        return
    if not data_hora:
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elif not validar_data(data_hora):
        print("❌ Data inválida. Use o formato: AAAA-MM-DD HH:MM:SS")
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
            else:
                print('cheguei na opcao de listar que deve vir uma data e o argumento é: ', sys.argv[2])
                listar_chamadas(data=sys.argv[2])
        elif len(sys.argv) == 4:
            listar_chamadas(sys.argv[2], sys.argv[3])
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
    
 # def listar_chamadas(numero = '', data = ''):
#     """Lista todas as chamadas ou apenas as de um número específico ou de uma data específica"""
#     print(f"aqui estão as variaveis numero:  {numero} e data= '{data}'" )
#     if data:
#         data_norm = normalizar_data(data)
#         if not data_norm:
#             print("❌ Data inválida. Use o formato: AAAA-MM-DD HH:MM:SS, a data que voce enviou foi: ",data)
#             return
#         data  =  data_norm
#     try:
#         if numero and not data:
#             chamadas  =  exec(f"SELECT * FROM chamadas WHERE numero = {numero}")
#             print(f"Chamadas para o número {numero}:")
#             for chamada in chamadas:
#                 print(f"Data/Hora: {chamada[2]}")
#             return
#         elif data and not numero:
#             chamadas  =  exec(f"SELECT * FROM chamadas WHERE data_hora LIKE '{data}%'" )
#             print(f"Chamadas no dia {data}:")
#             for chamada in chamadas:
#                 print(f"Número: {chamada[1]}")
#             return
#         elif numero and data:
#             chamadas  =  exec(f"SELECT * FROM chamadas WHERE numero = {numero} AND data_hora LIKE '{data}%'")
#             print(f"Chamadas para o número {numero} no dia {data}:")
#             for chamada in chamadas:
#                 print(f"Data/Hora: {chamada[2]}")
#             return
#         elif not numero and not data:     
#             chamadas  =  exec("SELECT * FROM chamadas")
#             for chamada in chamadas:
#                 print(f"Número: {chamada[1]} | Data/Hora: {chamada[2]}")
#         if not chamadas:
#             print("Nenhuma chamada encontrada")
#     except sqlite3.Error as e:
#         print(f"❌ Erro ao acessar o banco de dados: {e}")
