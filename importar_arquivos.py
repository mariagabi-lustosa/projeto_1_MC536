import psycopg2

# Conectar ao banco
conexao = psycopg2.connect(
    dbname='projeto_1',
    user='postgres',
    password='Sua_Senha_123',
    host='localhost',
    port='5432'
)

cursor = conexao.cursor()

# 1. Importar Trajetoria_Curso
with open('/home/gabi/Downloads/projeto_mc536/indicadores_trajetoria_educacao_superior_2019_2023.csv', 'r') as f:
    cursor.copy_expert("""
        COPY "Trajetoria_Curso" (curso_cod, ano_referencia, num_ingressantes, num_concluintes, taxa_desistencia)
        FROM STDIN
        WITH (FORMAT csv, HEADER true, DELIMITER ';')
    """, f)

# 2. Importar Estabelecimento_Economico
with open('/home/gabi/Downloads/projeto_mc536/RAIS_ano_base_2023_TABELA 2.csv', 'r') as f:
    cursor.copy_expert("""
        COPY "Estabelecimento_Economico" (ano, uf_sigla, estab_total, estab_com_vinculo, estab_sem_vinculo)
        FROM STDIN
        WITH (FORMAT csv, HEADER true, DELIMITER ';')
    """, f)

# 3. Importar Emprego_Por_Setor_E_Municipio
with open('/home/gabi/Downloads/projeto_mc536/RAIS_ano_base_2023_TABELA 4.csv', 'r') as f:
    cursor.copy_expert("""
        COPY "Emprego_Por_Setor_E_Municipio" (ano, municipio_cod, setor_nome, num_pessoas_empregadas, num_empregos_ofertados)
        FROM STDIN
        WITH (FORMAT csv, HEADER true, DELIMITER ';')
    """, f)

# 4. Importar Remuneracao_Media_Por_UF
with open('/home/gabi/Downloads/projeto_mc536/RAIS_ano_base_2023_TABELA 6.csv', 'r') as f:
    cursor.copy_expert("""
        COPY "Remuneracao_Media_Por_UF" (ano, uf_sigla, setor_nome, media_remuneracao, variacao_remuneracao)
        FROM STDIN
        WITH (FORMAT csv, HEADER true, DELIMITER ';')
    """, f)

# Commit e fechar
conexao.commit()
cursor.close()
conexao.close()
