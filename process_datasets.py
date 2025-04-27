import pandas as pd
import argparse
import os

## Definir os caminhos originais dos arquivos
#caminho_trajetoria = '/home/gabi/Downloads/projeto_mc536/indicadores_trajetoria_educacao_superior_2019_2023.csv'
#caminho_tabela2 = '/home/gabi/Downloads/projeto_mc536/RAIS_ano_base_2023_TABELA 2.csv'
#caminho_tabela4 = '/home/gabi/Downloads/projeto_mc536/RAIS_ano_base_2023_TABELA 4.csv'
#caminho_tabela6 = '/home/gabi/Downloads/projeto_mc536/RAIS_ano_base_2023_TABELA 6.csv'
#
## Definir os novos caminhos para salvar os arquivos tratados
#novo_trajetoria = '/home/gabi/Downloads/projeto_mc536/tratado_trajetoria.csv'
#novo_tabela2 = '/home/gabi/Downloads/projeto_mc536/tratado_tabela2.csv'
#novo_tabela4 = '/home/gabi/Downloads/projeto_mc536/tratado_tabela4.csv'
#novo_tabela6 = '/home/gabi/Downloads/projeto_mc536/tratado_tabela6.csv'
## 2. Pré-processar Estabelecimento_Economico
#df_tabela2 = pd.read_csv(caminho_tabela2, delimiter=',', encoding='utf-8')
#df_tabela2 = df_tabela2.rename(columns={
#    'Ano': 'ano',
#    'UF': 'uf_sigla',
#    'Total_Estabelecimentos': 'estab_total',
#    'Com_Vinculo': 'estab_com_vinculo',
#    'Sem_Vinculo': 'estab_sem_vinculo'
#})
#df_tabela2 = df_tabela2[['ano', 'uf_sigla', 'estab_total', 'estab_com_vinculo', 'estab_sem_vinculo']]
#df_tabela2.to_csv(novo_tabela2, index=False, sep=';')
#
## 3. Pré-processar Emprego_Por_Setor_E_Municipio
#df_tabela4 = pd.read_csv(caminho_tabela4, delimiter=',', encoding='utf-8')
#df_tabela4 = df_tabela4.rename(columns={
#    'Ano': 'ano',
#    'Municipio_Cod': 'municipio_cod',
#    'Setor_Nome': 'setor_nome',
#    'Num_Pessoas': 'num_pessoas_empregadas',
#    'Num_Empregos': 'num_empregos_ofertados'
#})
#df_tabela4 = df_tabela4[['ano', 'municipio_cod', 'setor_nome', 'num_pessoas_empregadas', 'num_empregos_ofertados']]
#df_tabela4.to_csv(novo_tabela4, index=False, sep=';')
#
## 4. Pré-processar Remuneracao_Media_Por_UF
#df_tabela6 = pd.read_csv(caminho_tabela6, delimiter=',', encoding='utf-8')
#df_tabela6 = df_tabela6.rename(columns={
#    'Ano': 'ano',
#    'UF': 'uf_sigla',
#    'Setor': 'setor_nome',
#    'Media_Salarial': 'media_remuneracao',
#    'Variacao_Salarial': 'variacao_remuneracao'
#})
#df_tabela6 = df_tabela6[['ano', 'uf_sigla', 'setor_nome', 'media_remuneracao', 'variacao_remuneracao']]
#df_tabela6.to_csv(novo_tabela6, index=False, sep=';')
#
#print("Arquivos tratados e salvos com sucesso!")

def process_indicadores(indicadores_csv, output_csv):
    """ Process the indicadores CSV file and save it to a new location.

    Args:
        indicadores_csv: Path to the CSV file containing the indicadores data.
        output_csv: Path to the directory where the processed CSV file will be saved.
    """

    # Read the CSV file
    df = pd.read_csv(
        indicadores_csv, 
        delimiter=',', 
        encoding='utf-8',
        skiprows=8,
        low_memory=False,
        header=0
    )
    
    # Delete unnecessary columns
    df.drop(columns=['CO_REGIAO', 'CO_UF', 'CO_MUNICIPIO', 'CO_CINE_ROTULO', 'NO_CINE_ROTULO', 'NU_ANO_INGRESSO', 'NU_PRAZO_INTEGRALIZACAO', 'NU_ANO_INTEGRALIZACAO', 'NU_PRAZO_ACOMPANHAMENTO', 'NU_ANO_MAXIMO_ACOMPANHAMENTO', 'QT_PERMANENCIA', 'QT_DESISTENCIA', 'QT_FALECIDO', 'TAP', 'TCA', 'TCAN', 'TADA'], inplace=True)

    # Rename columns
    df.rename(columns={
        'CO_IES': 'inst_cod',
        'NO_IES': 'inst_nome',
        'TP_CATEGORIA_ADMINISTRATIVA': 'categoria_adm',
        'TP_ORGANIZACAO_ACADEMICA': 'org_academica',
        'CO_CURSO': 'curso_cod',
        'NO_CURSO': 'curso_nome',
        'TP_GRAU_ACADEMICO': 'grau_academico',
        'TP_MODALIDADE_ENSINO': 'modo_ensino',
        'CO_CINE_AREA_GERAL': 'area_cod',
        'NO_CINE_AREA_GERAL': 'nome_area_atuacao',
        'NU_ANO_REFERENCIA': 'ano_referencia',
        'QT_INGRESSANTE': 'num_ingressantes',
        'QT_CONCLUINTE': 'num_concluintes',
        'TDA': 'taxa_desistencia'
    }, inplace=True)

    # Select relevant columns
    df = df[['inst_cod', 'inst_nome', 'categoria_adm', 'org_academica', 'curso_cod', 'curso_nome', 'grau_academico', 'modo_ensino', 'area_cod', 'nome_area_atuacao', 'ano_referencia', 'num_ingressantes', 'num_concluintes', 'taxa_desistencia']]

    # Save the processed DataFrame to a new CSV file

    output_file = os.path.join(output_csv, 'indicadores_educacao.csv')

    if os.path.exists(output_file):
        open(output_file, 'w').close()

    df.to_csv(output_file, index=False, sep=';')

    return 


def main(indicadores_csv, output_csv):
    """ Main function to process the CSV files.

    Args:
        indicadores_csv: Path to the CSV file containing the indicadores data.
        output_csv: Path to the directory where the processed CSV file will be saved.
    """
    if not os.path.exists(indicadores_csv):
        raise FileNotFoundError(f"The file {indicadores_csv} does not exist.")

    if not os.path.exists(os.path.dirname(output_csv)):
        raise FileNotFoundError(f"The directory {os.path.dirname(output_csv)} does not exist.")
    
    process_indicadores(indicadores_csv, output_csv)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process CSV files relevants to the project."
    )
    parser.add_argument(
        "-i",
        "--indicadores",
        default="datasets/indicadores_trajetoria_educacao_superior_2019_2023.csv",
        help="Path to the CSV file containing the indicadores data."
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output.csv",
        help="Path to the directory where the processed CSV file will be saved."
    )
    args = parser.parse_args()
    indicadores_csv = args.indicadores
    output_csv = args.output
    main(indicadores_csv, output_csv)
    
    
