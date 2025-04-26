import pandas as pd

# Definir os caminhos originais dos arquivos
caminho_trajetoria = '/home/gabi/Downloads/projeto_mc536/indicadores_trajetoria_educacao_superior_2019_2023.csv'
caminho_tabela2 = '/home/gabi/Downloads/projeto_mc536/RAIS_ano_base_2023_TABELA 2.csv'
caminho_tabela4 = '/home/gabi/Downloads/projeto_mc536/RAIS_ano_base_2023_TABELA 4.csv'
caminho_tabela6 = '/home/gabi/Downloads/projeto_mc536/RAIS_ano_base_2023_TABELA 6.csv'

# Definir os novos caminhos para salvar os arquivos tratados
novo_trajetoria = '/home/gabi/Downloads/projeto_mc536/tratado_trajetoria.csv'
novo_tabela2 = '/home/gabi/Downloads/projeto_mc536/tratado_tabela2.csv'
novo_tabela4 = '/home/gabi/Downloads/projeto_mc536/tratado_tabela4.csv'
novo_tabela6 = '/home/gabi/Downloads/projeto_mc536/tratado_tabela6.csv'

# 1. Pré-processar Trajetoria_Curso
colunas_trajetoria = [
    'CO_IES', 'NO_IES', 'TP_CATEGORIA_ADMINISTRATIVA', 'TP_ORGANIZACAO_ACADEMICA',
    'CO_CURSO', 'NO_CURSO', 'CO_REGIAO', 'CO_UF', 'CO_MUNICIPIO',
    'TP_GRAU_ACADEMICO', 'TP_MODALIDADE_ENSINO',
    'CO_CINE_ROTULO', 'NO_CINE_ROTULO', 'CO_CINE_AREA_GERAL', 'NO_CINE_AREA_GERAL',
    'NU_ANO_INGRESSO', 'NU_ANO_REFERENCIA', 'NU_PRAZO_INTEGRALIZACAO', 'NU_ANO_INTEGRALIZACAO',
    'NU_PRAZO_ACOMPANHAMENTO', 'NU_ANO_MAXIMO_ACOMPANHAMENTO',
    'QT_INGRESSANTE', 'QT_PERMANENCIA', 'QT_CONCLUINTE', 'QT_DESISTENCIA', 'QT_FALECIDO',
    'TAP', 'TCA', 'TDA', 'TCAN', 'TADA'
]

df_trajetoria = pd.read_csv(
    caminho_trajetoria,
    delimiter=',',
    encoding='utf-8',
    skiprows=9,
    names=colunas_trajetoria,
    low_memory=False
)

colunas_interesse = ['CO_CURSO', 'NU_ANO_REFERENCIA', 'QT_INGRESSANTE', 'QT_CONCLUINTE', 'TDA']
df_trajetoria = df_trajetoria[colunas_interesse]

# Renomear para o formato do banco
df_trajetoria = df_trajetoria.rename(columns={
    'CO_CURSO': 'curso_cod',
    'NU_ANO_REFERENCIA': 'ano_referencia',
    'QT_INGRESSANTE': 'num_ingressantes',
    'QT_CONCLUINTE': 'num_concluintes',
    'TDA': 'taxa_desistencia'
})

df_trajetoria.to_csv(novo_trajetoria, index=False, sep=';')

# 2. Pré-processar Estabelecimento_Economico
df_tabela2 = pd.read_csv(caminho_tabela2, delimiter=',', encoding='utf-8')
df_tabela2 = df_tabela2.rename(columns={
    'Ano': 'ano',
    'UF': 'uf_sigla',
    'Total_Estabelecimentos': 'estab_total',
    'Com_Vinculo': 'estab_com_vinculo',
    'Sem_Vinculo': 'estab_sem_vinculo'
})
df_tabela2 = df_tabela2[['ano', 'uf_sigla', 'estab_total', 'estab_com_vinculo', 'estab_sem_vinculo']]
df_tabela2.to_csv(novo_tabela2, index=False, sep=';')

# 3. Pré-processar Emprego_Por_Setor_E_Municipio
df_tabela4 = pd.read_csv(caminho_tabela4, delimiter=',', encoding='utf-8')
df_tabela4 = df_tabela4.rename(columns={
    'Ano': 'ano',
    'Municipio_Cod': 'municipio_cod',
    'Setor_Nome': 'setor_nome',
    'Num_Pessoas': 'num_pessoas_empregadas',
    'Num_Empregos': 'num_empregos_ofertados'
})
df_tabela4 = df_tabela4[['ano', 'municipio_cod', 'setor_nome', 'num_pessoas_empregadas', 'num_empregos_ofertados']]
df_tabela4.to_csv(novo_tabela4, index=False, sep=';')

# 4. Pré-processar Remuneracao_Media_Por_UF
df_tabela6 = pd.read_csv(caminho_tabela6, delimiter=',', encoding='utf-8')
df_tabela6 = df_tabela6.rename(columns={
    'Ano': 'ano',
    'UF': 'uf_sigla',
    'Setor': 'setor_nome',
    'Media_Salarial': 'media_remuneracao',
    'Variacao_Salarial': 'variacao_remuneracao'
})
df_tabela6 = df_tabela6[['ano', 'uf_sigla', 'setor_nome', 'media_remuneracao', 'variacao_remuneracao']]
df_tabela6.to_csv(novo_tabela6, index=False, sep=';')

print("Arquivos tratados e salvos com sucesso!")