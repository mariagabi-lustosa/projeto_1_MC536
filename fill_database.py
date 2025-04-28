import psycopg2
import argparse
import os
import pandas as pd
import numpy as np
import csv
import json
import datetime
import re

def safe_int(value, default=None):
    if value in (None, ''):
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value, default=None):
    if value in (None, ''):
        return default
    try:
        return float(str(value).replace(',', '.'))
    except (ValueError, TypeError):
        return default

# dividimos o dataset em 3 partes: instiuição, cursos, e a junção dos dois
inst_map = {}
inst_id_counter = 1

curso_map = {}
curso_id_counter = 1

enrollment_id_counter = 1

# dataset iNDICADORES (INEP)
def load_enrollment_data(conn, cursor, file_path):
    processed_rows = 0
    skipped_rows = 0

    try:
        # Agora usando pandas para ler o CSV
        df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')

        for _, row in df.iterrows():
            try:
                # — Extrai e converte campos por nome da coluna —
                inst_cod            = str(row['inst_cod']).strip()
                inst_nome           = str(row['inst_nome']).strip()
                categoria_adm       = str(row['categoria_adm']).strip()
                org_academica       = str(row['org_academica']).strip()
                curso_cod           = str(row['curso_cod']).strip()
                curso_nome          = str(row['curso_nome']).strip()
                grau_academico      = str(row['grau_academico']).strip()
                modo_ensino         = str(row['modo_ensino']).strip()
                area_cod            = str(row['area_cod']).strip()
                nome_area_atuacao   = str(row['nome_area_atuacao']).strip()
                ano_referencia      = safe_int(row['ano_referencia'])
                num_ingressantes    = safe_int(row['num_ingressantes'])
                num_concluintes     = safe_int(row['num_concluintes'])
                taxa_desistencia    = safe_float(row['taxa_desistencia'])

                # ve se n eh vazio
                if not all([
                    inst_cod, inst_nome,
                    curso_cod, curso_nome,
                    ano_referencia is not None
                ]):
                    skipped_rows += 1
                    continue

                # inserindo no banco de dados Instituição
                global inst_id_counter
                key_inst = inst_cod


                if key_inst not in inst_map:
                    cursor.execute(
                        """
                        INSERT INTO public."Institution"
                          ("ID", code, name, category_adm, org_academica)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (code) DO NOTHING;
                        """,
                        (inst_id_counter, inst_cod, inst_nome,
                         categoria_adm, org_academica)
                    )
                    cursor.execute(
                        'SELECT "ID" FROM public."Institution" WHERE code = %s',
                        (inst_cod,)
                    )
                    inst_id = cursor.fetchone()[0]
                    inst_map[key_inst] = inst_id
                    if inst_id >= inst_id_counter:
                        inst_id_counter = inst_id + 1
                else:
                    inst_id = inst_map[key_inst]

                # Curso  
                global curso_id_counter
                key_curso = curso_cod
                if key_curso not in curso_map:
                    cursor.execute(
                        """
                        INSERT INTO public."curso"
                          ("ID", code, name)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (code) DO NOTHING;
                        """,
                        (curso_id_counter, curso_cod, curso_nome)
                    )
                    cursor.execute(
                        'SELECT "ID" FROM public."curso" WHERE code = %s',
                        (curso_cod,)
                    )
                    curso_id = cursor.fetchone()[0]
                    curso_map[key_curso] = curso_id
                    if curso_id >= curso_id_counter:
                        curso_id_counter = curso_id + 1
                else:
                    curso_id = curso_map[key_curso]

                # Enrolltment curse
                global enrollment_id_counter
                cursor.execute(
                    """
                    INSERT INTO public."curso_Enrollment"
                      ("ID", institution_id, curso_id,
                       grau_academico, modo_ensino,
                       area_code, area_name, year,
                       num_ingressantes, num_concluintes,
                       dropout_rate)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """,
                    (enrollment_id_counter, inst_id, curso_id,
                     grau_academico, modo_ensino,
                     area_cod, nome_area_atuacao,
                     ano_referencia, num_ingressantes,
                     num_concluintes, taxa_desistencia)
                )
                enrollment_id_counter += 1
                processed_rows += 1

            except (KeyError, ValueError, TypeError) as e:
                skipped_rows += 1

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise

    finally:
        print(
            f"Processados: {processed_rows + skipped_rows}, "
            f"Inseridos: {processed_rows}, "
            f"Pulados: {skipped_rows}"
        )



municipality_map = {}  # mapeia municipio_cod → municipality_id
municipality_id_counter = 1

sector_map = {}        # mapeia setor_nome → sector_id
sector_id_counter = 1

employment_id_counter = 1  # contador para Employment.ID


def load_rais_data(conn, cursor, tabela4_csv):
    """
    Processa o CSV da RAIS Tabela 4 e insere no banco de dados:
      - Municipality
      - Sector
      - Employment

    Parâmetros
    ----------
    conn : psycopg2.Connection
        Conexão aberta ao banco de dados.
    cursor : psycopg2.Cursor
        Cursor associado à conexão.
    tabela4_csv : str
        Caminho para o arquivo CSV processado.
    """
    processed_rows = 0
    skipped_rows = 0

    try:
        df = pd.read_csv(
            tabela4_csv,
            delimiter=';',
            encoding='utf-8'
        )

        for idx, row in df.iterrows():
            try:
                uf_sigla              = str(row['uf_sigla']).strip()
                municipio_cod         = str(row['municipio_cod']).strip()
                municipio_nome        = str(row['municipio_nome']).strip()
                setor_nome            = str(row['setor_nome']).strip()
                ano                   = int(row['ano'])
                num_pessoas_empregadas = int(row['num_pessoas_empregadas'])

                # — Validação mínima —
                if not all([
                    uf_sigla, municipio_cod, municipio_nome,
                    setor_nome, ano is not None
                ]):
                    skipped_rows += 1
                    continue

                # — Inserção/recuperação em Municipality —
                global municipality_id_counter
                key_municipality = municipio_cod
                if key_municipality not in municipality_map:
                    cursor.execute(
                        """
                        INSERT INTO public."Municipality"
                          ("ID", code, name, uf_sigla)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (code) DO NOTHING;
                        """,
                        (municipality_id_counter, municipio_cod, municipio_nome, uf_sigla)
                    )
                    cursor.execute(
                        'SELECT "ID" FROM public."Municipality" WHERE code = %s',
                        (municipio_cod,)
                    )
                    municipality_id = cursor.fetchone()[0]
                    municipality_map[key_municipality] = municipality_id
                    if municipality_id >= municipality_id_counter:
                        municipality_id_counter = municipality_id + 1
                else:
                    municipality_id = municipality_map[key_municipality]

                # — Inserção/recuperação em Sector —
                global sector_id_counter
                key_sector = setor_nome
                if key_sector not in sector_map:
                    cursor.execute(
                        """
                        INSERT INTO public."Sector"
                          ("ID", name)
                        VALUES (%s, %s)
                        ON CONFLICT (name) DO NOTHING;
                        """,
                        (sector_id_counter, setor_nome)
                    )
                    cursor.execute(
                        'SELECT "ID" FROM public."Sector" WHERE name = %s',
                        (setor_nome,)
                    )
                    sector_id = cursor.fetchone()[0]
                    sector_map[key_sector] = sector_id
                    if sector_id >= sector_id_counter:
                        sector_id_counter = sector_id + 1
                else:
                    sector_id = sector_map[key_sector]

                # — Inserção em Employment —
                global employment_id_counter
                cursor.execute(
                    """
                    INSERT INTO public."Employment"
                      ("ID", municipality_id, sector_id, year, num_pessoas_empregadas)
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (employment_id_counter, municipality_id, sector_id, ano, num_pessoas_empregadas)
                )
                employment_id_counter += 1
                processed_rows += 1

            except (KeyError, ValueError, TypeError) as e:
                skipped_rows += 1

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        print(
            f"Processados: {processed_rows + skipped_rows}, "
            f"Inseridos: {processed_rows}, "
            f"Pulados: {skipped_rows}"
        )


# ————— Mapas e contadores globais —————
state_map = {}          # mapeia uf_sigla → state_id
state_id_counter = 1

sector_map = {}         # mapeia setor_nome → sector_id
sector_id_counter = 1

salary_stats_id_counter = 1  # contador para Salary_Stats.ID

def load_rais6_data(conn, cursor, tabela6_csv):
    """
    Lê o CSV da RAIS Tabela 6 e carrega as tabelas:
      - State
      - Sector
      - Salary_Stats

    Parâmetros
    ----------
    conn : psycopg2.Connection
        Conexão ao banco.
    cursor : psycopg2.Cursor
        Cursor associado à conexão.
    tabela6_csv : str
        Caminho para o arquivo CSV da RAIS Tabela 6, já com colunas:
        ['ano','uf_sigla','setor_nome','media_remuneracao','variacao_remuneracao']
    """
    processed = 0
    skipped = 0

    try:
        # 1) carrega o CSV
        df = pd.read_csv(
            tabela6_csv,
            delimiter=';',
            encoding='utf-8'
        )

        # 2) itera por linha
        for _, row in df.iterrows():
            try:
                ano                  = int(row['ano'])
                uf                   = str(row['uf_sigla']).strip()
                setor                = str(row['setor_nome']).strip()
                media_remuneracao    = float(row['media_remuneracao'])
                variacao_remuneracao = float(row['variacao_remuneracao'])

                # validação mínima
                if not all([ano, uf, setor]):
                    skipped += 1
                    continue

                # — State —
                global state_id_counter
                if uf not in state_map:
                    cursor.execute(
                        """
                        INSERT INTO public."State"
                          ("ID", uf_sigla)
                        VALUES (%s, %s)
                        ON CONFLICT (uf_sigla) DO NOTHING;
                        """,
                        (state_id_counter, uf)
                    )
                    cursor.execute(
                        'SELECT "ID" FROM public."State" WHERE uf_sigla = %s',
                        (uf,)
                    )
                    sid = cursor.fetchone()[0]
                    state_map[uf] = sid
                    if sid >= state_id_counter:
                        state_id_counter = sid + 1
                else:
                    sid = state_map[uf]

                # — Sector —
                global sector_id_counter
                if setor not in sector_map:
                    cursor.execute(
                        """
                        INSERT INTO public."Sector"
                          ("ID", name)
                        VALUES (%s, %s)
                        ON CONFLICT (name) DO NOTHING;
                        """,
                        (sector_id_counter, setor)
                    )
                    cursor.execute(
                        'SELECT "ID" FROM public."Sector" WHERE name = %s',
                        (setor,)
                    )
                    sec_id = cursor.fetchone()[0]
                    sector_map[setor] = sec_id
                    if sec_id >= sector_id_counter:
                        sector_id_counter = sec_id + 1
                else:
                    sec_id = sector_map[setor]

                # — Salary_Stats —
                global salary_stats_id_counter
                cursor.execute(
                    """
                    INSERT INTO public."Salary_Stats"
                      ("ID", state_id, sector_id, year,
                       media_remuneracao, variacao_remuneracao)
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                    (salary_stats_id_counter, sid, sec_id,
                     ano, media_remuneracao, variacao_remuneracao)
                )
                salary_stats_id_counter += 1
                processed += 1

            except (KeyError, ValueError, TypeError):
                skipped += 1

        # 3) persiste tudo
        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        print(f"Processados: {processed+skipped}, Inseridos: {processed}, Pulados: {skipped}")

def process_rais_9(tabela9_csv, output_csv):
    """
    Processa o CSV da RAIS Tabela 9:
      - Lê o arquivo bruto
      - Renomeia cabeçalhos
      - Seleciona apenas as colunas relevantes
      - Salva o CSV final

    Args:
        tabela9_csv (str): caminho para o CSV original da Tabela 9.
        output_csv (str): diretório onde será salvo 'rais_tabela9.csv'.
    """
    # 1) Leitura do CSV bruto
    df = pd.read_csv(
        tabela9_csv,
        delimiter=',',
        encoding='utf-8'
    )  # delimitação por vírgula :contentReference[oaicite:0]{index=0}

    # 2) Renomeia colunas para rótulos consistentes
    df.rename(columns={
        'Região/UF': 'regiao_uf',
        '2023': 'remuneracao_2023',
        '2024': 'remuneracao_2024',
        'Var. Absoluta': 'var_absoluta',
        'Var. Relativa (%)': 'var_relativa_perc'
    }, inplace=True)  # renomear rótulos :contentReference[oaicite:1]{index=1}

    # 3) Seleciona apenas as colunas esperadas
    df = df[
        ['regiao_uf',
         'remuneracao_2023',
         'remuneracao_2024',
         'var_absoluta',
         'var_relativa_perc']
    ]

    # 4) Grava o CSV processado
    os.makedirs(output_csv, exist_ok=True)
    output_file = os.path.join(output_csv, 'rais_tabela9.csv')
    df.to_csv(output_file, index=False, sep=';')  # salva com ponto-e-vírgula :contentReference[oaicite:2]{index=2}

    print(f"[OK] RAIS Tabela 9 processada e salva em: {output_file}")

