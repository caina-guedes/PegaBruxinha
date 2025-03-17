import sqlite3

def conectar():
    """Estabelece uma conexão com o banco de dados."""
    return sqlite3.connect("chamadas.db")



def execute(querry, save=True,mostrar=False):
    """Executa uma query no banco de dados e salva as alterações por padrão."""
    if mostrar:
        print(querry)
    with conectar() as conn:
        c = conn.cursor()
        c.execute(querry)
        if save:
            conn.commit()
        return c.fetchall()
def exec(querry,save=True,mostrar=False):
    try:
        return execute(querry,save,mostrar)
    except:
        try:
            create()
            return execute(querry,save,mostrar)
        except:
            print('querry do erro: ',querry)
            return execute(querry,save,mostrar)
def create():

    # Cria a tabela do registro de chamadas se não existir
    exec('''
    CREATE TABLE IF NOT EXISTS chamadas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero TEXT NOT NULL,
        data_hora TEXT NOT NULL
    )
    ''')
    # Cria a tabela de backup de linhas se não existir
    exec('''
    CREATE TABLE IF NOT EXISTS historico_linhas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lista_numero_1 TEXT,
        lista_numero_2 TEXT,
        nome_empresa TEXT NOT NULL,
        resultado TEXT,
        emailObtidoEmLigacao TEXT,
        dataPrimeiroEmail TEXT,
        dataSegundoEmail TEXT,
        dataTerceiroEmail TEXT,
        data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (lista_numero_1, lista_numero_2, nome_empresa)
    )
    ''')

    exec("CREATE INDEX IF NOT EXISTS idx_numero ON chamadas (numero);")
    exec("CREATE INDEX IF NOT EXISTS idx_empresa ON historico_linhas (nome_empresa);")



def ja_liguei(numero):
    """Verifica se o número já foi chamado."""
    resp = exec(f"SELECT 1 FROM chamadas WHERE numero = {numero} LIMIT 1")
    return len(resp) == 1

        