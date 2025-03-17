import sqlite3
from funcoesBancoDeDados import exec

# conn = sqlite3.connect("chamadas.db")

# c = conn.cursor()


def salva_linha(lista_numero_1='',lista_numero_2='',nome_empresa='',resultado='',emailObtidoEmLigacao='',dataPrimeiroEmail='',dataSegundoEmail='',dataTerceiroEmail=''):
    """Salva uma linha da tabela com os valores das duas colunas de telefones, nome da empresa, resultado da ligação, email obtido em ligação e datas dos emails"""
    print('lista_numero_1: ',lista_numero_1)
    print('lista_numero_2 : ',lista_numero_2 )
    print('nome_empresa : ', nome_empresa)
    print('resultado : ',resultado )
    print('emailObtidoEmLigacao : ', emailObtidoEmLigacao)
    print('dataPrimeiroEmail : ',dataPrimeiroEmail )
    print('dataSegundoEmail : ',dataSegundoEmail )
    print('dataTerceiroEmail : ', dataTerceiroEmail)
    try:
        a=exec(f"""INSERT INTO historico_linhas 
               (lista_numero_1,lista_numero_2, nome_empresa, resultado, emailObtidoEmLigacao, 
               dataPrimeiroEmail, dataSegundoEmail, dataTerceiroEmail) VALUES 
               ('{lista_numero_1}', '{lista_numero_2}', '{nome_empresa}', '{resultado}', '{emailObtidoEmLigacao}',
                 '{dataPrimeiroEmail}', '{dataSegundoEmail}', '{dataTerceiroEmail}')""",mostrar = True)
        print(f"📞 Linha salva: {nome_empresa} ")
    except sqlite3.IntegrityError:
        print("❌ Registro duplicado! Essa combinação de telefones e empresa já existe.")
    except sqlite3.Error as e:
        print(f"❌ Erro ao acessar o banco de dados: {e}")

def lista_linha(telefone='',empresa=''):
    """Lista linhas da tabela de acordo com os valores de telefone e/ou empresa
    Se telefone e empresa não forem informados, lista todas as linhas"""
    try:
        if not telefone and not empresa:
            linhas = exec("SELECT * FROM historico_linhas",save=False)
            for linha in linhas:
                print(f"Lista de números: {linha[1]} | {linha[2]} | Empresa: {linha[3]} | Resultado: {linha[4]} | Email obtido: {linha[5]} | Data do primeiro email: {linha[6]} | Data do segundo email: {linha[7]} | Data do terceiro email: {linha[8]}")
        
        elif telefone and not empresa:
            print('reconheci o tel no listar linhas mas não empresa')
            linhas = exec(f"SELECT * FROM historico_linhas WHERE lista_numero_1 like '%{telefone}%' OR lista_numero_2 like '%{telefone}%'",save=False)
            for linha in linhas:
                print(f"Lista de números: {linha[1]} | {linha[2]} | Empresa: {linha[3]} | Resultado: {linha[4]} | Email obtido: {linha[5]} | Data do primeiro email: {linha[6]} | Data do segundo email: {linha[7]} | Data do terceiro email: {linha[8]}")
        
        elif not telefone and empresa:
            linhas = exec(f"SELECT * FROM historico_linhas WHERE nome_empresa = '{empresa}'",save=False)
            for linha in linhas:
                print(f"Lista de números: {linha[1]} | {linha[2]} | Empresa: {linha[3]} | Resultado: {linha[4]} | Email obtido: {linha[5]} | Data do primeiro email: {linha[6]} | Data do segundo email: {linha[7]} | Data do terceiro email: {linha[8]}")
        elif telefone and empresa:
            linhas = exec(f"SELECT * FROM historico_linhas WHERE (lista_numero_1 like '%{telefone}%' OR lista_numero_2 like '%{telefone}%') AND nome_empresa = '{empresa}'",save=False)
            for linha in linhas:
                print(f"Lista de números: {linha[1]} | {linha[2]} | Empresa: {linha[3]} | Resultado: {linha[4]} | Email obtido: {linha[5]} | Data do primeiro email: {linha[6]} | Data do segundo email: {linha[7]} | Data do terceiro email: {linha[8]}")
        if not linhas:
            print("Nenhuma linha encontrada")
    except sqlite3.Error as e:
        print(f"❌ Erro ao acessar o banco de dados: {e}")