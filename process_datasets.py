import pandas as pd
import argparse
import os

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


def process_rais_4(tabela4_csv, output_csv):
    """ Process the RAIS Tabela 4 CSV file and save it to a new location.

    Args:
        tabela4_csv: Path to the CSV file containing the RAIS Tabela 4 data.
        output_csv: Path to the directory where the processed CSV file will be saved.
    """
    df = pd.read_csv(
        tabela4_csv, 
        delimiter=',', 
        encoding='utf-8',
        low_memory=False,
        skiprows=12,
        header=[0,1]
    )

    # Delete unnecessary columns
    df.drop(columns=['Unnamed: 0_level_0', 'Unnamed: 6_level_0', 'Unnamed: 7_level_0', 'Unnamed: 10_level_0', 'Unnamed: 11_level_0', 'Unnamed: 14_level_0', 'Unnamed: 15_level_0', 'Unnamed: 18_level_0', 'Unnamed: 19_level_0', 'Unnamed: 22_level_0', 'Unnamed: 23_level_0', 'Unnamed: 25_level_0', 'Unnamed: 26_level_0', 'Unnamed: 27_level_0', 'Total'], inplace=True)

    # Rename columns
    df.rename(columns={
        'Agropecuária': 'Agropecuária',
        'Unnamed: 5_level_0': 'Agropecuária',
        'Indústria': 'Indústria',
        'Unnamed: 9_level_0': 'Indústria',
        'Construção': 'Construção',
        'Unnamed: 13_level_0': 'Construção',
        'Comércio': 'Comércio',
        'Unnamed: 17_level_0': 'Comércio',
        'Serviços': 'Serviços',
        'Unnamed: 21_level_0': 'Serviços'
    }, inplace=True)

    # Select relevant columns
    df.columns.names = ['Type', 'Year']  # label the MultiIndex columns if needed
    df.columns = [f"{type}_{year}" if type is not None else year for type, year in df.columns]

    df.rename(columns={
        'UF_Unnamed: 1_level_1': 'UF',
        'Código_Unnamed: 2_level_1': 'Código',
        'Município_Unnamed: 3_level_1': 'Município'
    }, inplace=True)

    df_melted = df.melt(
        id_vars=['UF','Código', 'Município'],     # columns you want to KEEP
        var_name='Área_Ano',                # the original column names
        value_name='Empregados'                   # the values
    )

    df_melted[['Área', 'Ano']] = df_melted['Área_Ano'].str.split('_', expand=True)

    # Drop the original combined column
    df_melted = df_melted.drop(columns='Área_Ano')

    # Optional: reorder columns
    df_melted = df_melted[['UF', 'Código', 'Município', 'Área', 'Ano', 'Empregados']]

    df_melted.rename(columns={
        'UF': 'uf_sigla',
        'Código': 'municipio_cod',
        'Município': 'municipio_nome',
        'Área': 'setor_nome',
        'Ano': 'ano',
        'Empregados': 'num_pessoas_empregadas'
    }, inplace=True)

    df_melted = df_melted.dropna()

    # Save the processed DataFrame to a new CSV file
    output_file = os.path.join(output_csv, 'rais_tabela4.csv')
    if os.path.exists(output_file):
        open(output_file, 'w').close()

    df_melted.to_csv(output_file, index=False, sep=';')

    return


def process_rais_6(tabela6_csv, output_csv):
    """ Process the RAIS Tabela 6 CSV file and save it to a new location.

    Args:
        tabela6_csv: Path to the CSV file containing the RAIS Tabela 6 data.
        output_csv: Path to the directory where the processed CSV file will be saved.
    """
    df = pd.read_csv(
        tabela6_csv, 
        delimiter=',', 
        encoding='utf-8',
        low_memory=False,
        
    )


def process_rais_9(tabela9_csv, output_csv):
    """ Process the RAIS Tabela 9 CSV file and save it to a new location.

    Args:
        tabela9_csv: Path to the CSV file containing the RAIS Tabela 9 data.
        output_csv: Path to the directory where the processed CSV file will be saved.
    """
    df_tabela9 = pd.read_csv(tabela9_csv, delimiter=',', encoding='utf-8')


def main(indicadores_csv, output_csv, rais_4_csv):
    """ Main function to process the CSV files.

    Args:
        indicadores_csv: Path to the CSV file containing the indicadores data.
        rais_4_csv: Path to the CSV file containing the RAIS Tabela 4 data.
        output_csv: Path to the directory where the processed CSV file will be saved.
    """
    if not os.path.exists(indicadores_csv):
        raise FileNotFoundError(f"The file {indicadores_csv} does not exist.")

    if not os.path.exists(os.path.dirname(output_csv)):
        raise FileNotFoundError(f"The directory {os.path.dirname(output_csv)} does not exist.")

    if not os.path.exists(rais_4_csv):
        raise FileNotFoundError(f"The file {rais_4_csv} does not exist.")
    
    process_indicadores(indicadores_csv, output_csv)
    process_rais_4(rais_4_csv, output_csv)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process CSV files relevants to the project."
    )
    parser.add_argument(
        "-i",
        "--indicadores",
        default="preprocessed_dataset/indicadores_trajetoria_educacao_superior_2019_2023.csv",
        help="Path to the CSV file containing the indicadores data."
    )
    parser.add_argument(
        "-r4",
        "--rais_4",
        default="preprocessed_dataset/RAIS_ano_base_2023_TABELA 4.csv",
        help="Path to the CSV file containing the RAIS Tabela 4 data."
    )
    parser.add_argument(
        "-o",
        "--output",
        default="datasets/",
        help="Path to the directory where the processed CSV file will be saved."
    )
    args = parser.parse_args()
    indicadores_csv = args.indicadores
    rais_4_csv = args.rais_4
    output_csv = args.output
    main(indicadores_csv, output_csv, rais_4_csv)
    
    
