import csv
import psycopg2
import sys
import argparse
import os

# Global maps to track unique values for each table
area_map = {}
curso_map = {}
instituicao_map = {}
municipio_map = {}
uf_map = {}
setor_map = {}

def safe_int(value, default=None):
    """ Converts a value to an integer, returning a default if conversion fails.
    
    Args:
        value: The value to convert.
        default: The default value to return if conversion fails.
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value, default=None):
    """ Converts a value to a float, returning a default if conversion fails.

    Args:
        value: The value to convert.
        default: The default value to return if conversion fails.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def load_education_data(cursor, connection, education_path):
    """ Load education data from a CSV file into the database.

    Args:
        cursor: The database cursor.
        connection: The database connection.
        education_path: Path to the CSV file.
    """
    print(f"\nLoading data from {education_path}...")
    processed_rows = 0
    skipped_rows = 0

    try:
        with open(education_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')

            for row in reader:
                try:
                    # Extract and clean data from the row
                    inst_cod = safe_int(row['inst_cod'])
                    inst_nome = row['inst_nome'].strip()

                    categoria_adm = row['categoria_adm'].strip()
                    org_academica = row['org_academica'].strip()

                    curso_cod = safe_int(row['curso_cod'])
                    curso_nome = row['curso_nome'].strip()
                    grau_academico = safe_int(row['grau_academico'])
                    modo_ensino = row['modo_ensino'].strip()

                    area_cod = safe_int(row['area_cod'])
                    nome_area_atuacao = row['nome_area_atuacao'].strip()

                    ano_referencia = safe_int(row['ano_referencia'])
                    num_ingressantes = safe_int(row['num_ingressantes'])
                    num_concluintes = safe_int(row['num_concluintes'])
                    taxa_desistencia = safe_float(row['taxa_desistencia'])

                    uf_nome = row['uf_nome'].strip()
                    uf_sigla = row['uf_sigla'].strip()

                    # Inserts Unidade_Federativa
                    if uf_sigla and uf_sigla not in uf_map:
                        cursor.execute(
                            """
                            INSERT INTO public."Unidade_Federativa" (uf_sigla, uf_nome)
                            VALUES (%s, %s)
                            ON CONFLICT (uf_sigla) DO NOTHING;
                            """,
                            (uf_sigla, uf_nome)
                        )
                        uf_map[uf_sigla] = uf_nome

                    # Inserts Area_Atuacao
                    if area_cod and area_cod not in area_map:
                        cursor.execute(
                            """
                            INSERT INTO public."Area_Atuacao" (area_cod, nome_area_atuacao)
                            VALUES (%s, %s)
                            ON CONFLICT (area_cod) DO NOTHING;
                            """,
                            (area_cod, nome_area_atuacao)
                        )
                        area_map[area_cod] = nome_area_atuacao

                    # Insert Instituicao_Superior
                    if inst_cod and inst_cod not in instituicao_map:
                        cursor.execute(
                            """
                            INSERT INTO public."Instituicao_Superior" (inst_cod, inst_nome, categoria_adm, org_academica, uf_sigla)
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT (inst_cod) DO NOTHING;
                            """,
                            (inst_cod, inst_nome, categoria_adm, org_academica, uf_sigla)
                        )
                        instituicao_map[inst_cod] = inst_nome

                    # Inserts Curso
                    if curso_cod and curso_cod not in curso_map:
                        cursor.execute(
                            """
                            INSERT INTO public."Curso" (curso_cod, curso_nome, grau_academico, modo_ensino, area_cod, inst_cod)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            ON CONFLICT (curso_cod) DO NOTHING;
                            """,
                            (curso_cod, curso_nome, grau_academico, modo_ensino, area_cod, inst_cod)
                        )
                        curso_map[curso_cod] = curso_nome

                    # Inserts Trajetoria_Curso
                    if curso_cod and ano_referencia:
                        cursor.execute(
                            """
                            INSERT INTO public."Trajetoria_Curso" (curso_cod, ano_referencia, num_ingressantes, num_concluintes, taxa_desistencia)
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT (curso_cod, ano_referencia) DO NOTHING;
                            """,
                            (curso_cod, ano_referencia, num_ingressantes, num_concluintes, taxa_desistencia)
                        )

                    processed_rows += 1

                except (KeyError, ValueError, TypeError) as e:
                    print(f"Skipping row due to data error: {row} - Error: {e}")
                    skipped_rows += 1
                except psycopg2.Error as e:
                    print(f"Database error processing row: {row} - Error: {e}")
                    connection.rollback()
                    skipped_rows += 1

                if (processed_rows + skipped_rows) % 500 == 0:
                    print(f"Processed {processed_rows + skipped_rows} rows...", end='\r')
                    sys.stdout.flush()

    except FileNotFoundError:
        print(f"Error: File not found at {education_path}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
    finally:
        print(f"\nFinished loading {education_path}. Total rows processed: {processed_rows + skipped_rows}, Inserted: {processed_rows}, Skipped: {skipped_rows}.")
    
    return


def load_rais_4_data(cursor, connection, rais_4_path):
    """ Load RAIS data from CSV files into the database.

    Args:
        cursor: The database cursor.
        connection: The database connection.
        rais_4_path: Path to the RAIS Tabela 4 CSV file.
    """
    print(f"\nLoading RAIS data from {rais_4_path}...")
    processed_rows = 0
    skipped_rows = 0

    try:
        with open(rais_4_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')

            for row in reader:
                try:
                    # Extract and clean data from the row
                    uf_sigla = row['uf_sigla'].strip()

                    municipio_cod = safe_int(row['municipio_cod'])
                    municipio_nome = row['municipio_nome'].strip()

                    setor_nome = row['setor_nome'].strip()

                    ano = safe_int(row['ano'])
                    num_pessoas_empregadas = safe_int(row['num_pessoas_empregadas'])
                   
                    # Inserts Setor_Economico
                    if setor_nome and setor_nome not in setor_map:
                        cursor.execute(
                            """
                            INSERT INTO public."Setor_Economico" (setor_nome)
                            VALUES (%s)
                            ON CONFLICT (setor_nome) DO NOTHING;
                            """,
                            (setor_nome,)
                        )
                        setor_map[setor_nome] = setor_nome

                    # Inserts Municipio
                    if municipio_cod and municipio_cod not in municipio_map:
                        cursor.execute(
                            """
                            INSERT INTO public."Municipio" (municipio_cod, municipio_nome, uf_sigla)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (municipio_cod) DO NOTHING;
                            """,
                            (municipio_cod, municipio_nome, uf_sigla)
                        )
                        municipio_map[municipio_cod] = municipio_nome
                    

                    # Inserts Emprego_Por_Setor_E_Municipio
                    if ano and municipio_cod and setor_nome:
                        cursor.execute(
                            """
                            INSERT INTO public."Emprego_Por_Setor_E_Municipio" (ano, municipio_cod, setor_nome, num_pessoas_empregadas)
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT (ano, municipio_cod, setor_nome) DO NOTHING;
                            """,
                            (ano, municipio_cod, setor_nome, num_pessoas_empregadas)
                        )

                    processed_rows += 1

                except (KeyError, ValueError, TypeError) as e:
                    print(f"Skipping row due to data error: {row} - Error: {e}")
                    skipped_rows += 1
                except psycopg2.Error as e:
                    print(f"Database error processing row: {row} - Error: {e}")
                    connection.rollback()
                    skipped_rows += 1

                if (processed_rows + skipped_rows) % 500 == 0:
                    print(f"Processed {processed_rows + skipped_rows} rows...", end='\r')
                    sys.stdout.flush()
    except FileNotFoundError:
        print(f"Error: File not found at {rais_4_path}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
    finally:
        print(f"\nFinished loading {rais_4_path}. Total rows processed: {processed_rows + skipped_rows}, Inserted: {processed_rows}, Skipped: {skipped_rows}.")

def load_rais_6_data(cursor, connection, rais_6_path):
    """ Load RAIS Tabela 6 data from a CSV file into the database.

    Args:
        cursor: The database cursor.
        connection: The database connection.
        rais_6_path: Path to the RAIS Tabela 6 CSV file.
    """
    print(f"\nLoading RAIS Tabela 6 data from {rais_6_path}...")
    processed_rows = 0
    skipped_rows = 0

    try: 
        with open(rais_6_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')

            for row in reader:
                try:
                    # Extract and clean data from the row
                    uf_sigla = row['uf_sigla'].strip()
                    
                    ano = safe_int(row['ano'])

                    media_remuneracao = safe_float(row['media_remuneracao'])

                    # Inserts Remuneracao_Media_Por_UF
                    if ano and uf_sigla and media_remuneracao is not None:
                        cursor.execute(
                            """
                            INSERT INTO public."Remuneracao_Media_Por_UF" (ano, uf_sigla, media_remuneracao)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (ano, uf_sigla) DO NOTHING;
                            """,
                            (ano, uf_sigla, media_remuneracao)
                        )

                    processed_rows += 1

                except (KeyError, ValueError, TypeError) as e:
                    print(f"Skipping row due to data error: {row} - Error: {e}")
                    skipped_rows += 1
                except psycopg2.Error as e:
                    print(f"Database error processing row: {row} - Error: {e}")
                    connection.rollback()
                    skipped_rows += 1

                if (processed_rows + skipped_rows) % 500 == 0:
                    print(f"Processed {processed_rows + skipped_rows} rows...", end='\r')
                    sys.stdout.flush()

    except FileNotFoundError:
        print(f"Error: File not found at {rais_6_path}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
    finally:
        print(f"\nFinished loading {rais_6_path}. Total rows processed: {processed_rows + skipped_rows}, Inserted: {processed_rows}, Skipped: {skipped_rows}.")

    return


def main(datasets_directory):
    """ Main function to load data into the database.

    Args:
        datasets_directory: Directory containing the datasets to load.
    """
    try:
        connection = psycopg2.connect(
            dbname='name', # Change this to your actual database name
            user='user', # Change this to your actual username
            password='password', # Change this to your actual password
            host='host', # Change this to your actual host
            port='9999' # Change this to your actual port
        )
        cursor = connection.cursor()
        
        education_path = f'{datasets_directory}/indicadores_educacao.csv'
        load_education_data(cursor, connection, education_path)

        rais_4_path = f'{datasets_directory}/rais_tabela4_joined.csv'
        rais_6_path = f'{datasets_directory}/rais_tabela6_joined.csv'
        load_rais_4_data(cursor, connection, rais_4_path)
        load_rais_6_data(cursor, connection, rais_6_path)

        connection.commit()
        print("Dados inseridos com sucesso.")

    except Exception as e:
        print(f"Error: {e}")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Load education data into the database.'
    )
    parser.add_argument(
        '-d',
        '--datasets_directory',
        default=None,
        help='Directory containing the datasets to load.'
    )
    args = parser.parse_args()
    datasets_directory = args.datasets_directory
    main(datasets_directory)
