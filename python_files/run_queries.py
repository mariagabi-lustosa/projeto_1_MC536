import psycopg2
import pandas as pd

DB_NAME='database' # Change this to your actual database name
DB_USER='user' # Change this to your actual username
DB_PASS='password' # Change this to your actual password
DB_HOST='host' # Change this to your actual host
DB_PORT='9999' # Change this to your actual port

def execute_query(query_index, description, sql_query):
    """ Executes a SQL query and prints the results in a formatted way. 

    Args:
        query_index (int): The index of the query.
        description (str): A description of the query.
        sql_query (str): The SQL query to be executed.
    """
    connection = None
    print(f"\n--- Query {query_index}: {description} ---")
    print("SQL:")
    print(sql_query)
    print("\nResults:")

    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASS,
            host=DB_HOST, port=DB_PORT
        )
        cursor = connection.cursor()
        cursor.execute(sql_query)

        if cursor.description:
            colnames = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()

            if results:
                df = pd.DataFrame(results, columns=colnames)
                print(df.to_string(index=False))
                df.to_csv(f'query_{query_index}_result.csv', index=False)
            else:
                print("Query correctly executed, but no results.")
        else:
            print("Query correctly executed (no return).")

    except psycopg2.Error as e:
        print(f"\nDatabase error in query {query_index}: {e}")
        print(f"SQLSTATE: {e.pgcode}")
        print(f"Details: {e.pgerror}")
        if connection:
            connection.rollback()
    except Exception as e:
        print(f"\nUnexpected error in query {query_index}: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if connection:
            connection.close()
    print("-" * (len(description) + 14))

def main():
    """ Main function to execute a series of SQL queries. """
    query_1 = [
            1,
            "Identifica os 20 municípios com mais empregos formais em um setor e ano específicos",
            """
            SELECT 
                m.municipio_nome,
                uf.uf_sigla,
                s.setor_nome,
                ep.ano,
                ep.num_pessoas_empregadas
            FROM "Emprego_Por_Setor_E_Municipio" ep
            JOIN "Municipio" m ON ep.municipio_cod = m.municipio_cod
            JOIN "Unidade_Federativa" uf ON m.uf_sigla = uf.uf_sigla
            JOIN "Setor_Economico" s ON ep.setor_nome = s.setor_nome
            WHERE s.setor_nome ILIKE '%Agropecuária%' AND ep.ano = 2023
            ORDER BY ep.num_pessoas_empregadas DESC
            LIMIT 20;
            """
    ]
    execute_query(query_1[0], query_1[1], query_1[2])

    query_2 = [
        2,
        "Relação entre taxa de desistência média e variação de remuneração por área do conhecimento em um determinado período de tempo",
        """
        WITH TaxaDesistenciaPorArea AS (
            SELECT 
                a.area_cod,
                a.nome_area_atuacao,
                AVG(tc.taxa_desistencia) AS media_taxa_desistencia
            FROM "Trajetoria_Curso" tc
            JOIN "Curso" c ON tc.curso_cod = c.curso_cod
            JOIN "Area_Atuacao" a ON c.area_cod = a.area_cod
            WHERE tc.ano_referencia BETWEEN 2020 AND 2023  -- período desejado
            GROUP BY a.area_cod, a.nome_area_atuacao
        ),

        RemuneracaoPorArea AS (
            SELECT 
                a.area_cod,
                AVG(r_fim.media_remuneracao - r_ini.media_remuneracao) AS variacao_remuneracao
            FROM "Curso" c
            JOIN "Area_Atuacao" a ON c.area_cod = a.area_cod
            JOIN "Instituicao_Superior" i ON c.inst_cod = i.inst_cod
            JOIN "Remuneracao_Media_Por_UF" r_ini ON r_ini.uf_sigla = i.uf_sigla AND r_ini.ano = 2020
            JOIN "Remuneracao_Media_Por_UF" r_fim ON r_fim.uf_sigla = i.uf_sigla AND r_fim.ano = 2023
            GROUP BY a.area_cod
        )

        SELECT 
            t.nome_area_atuacao,
            ROUND(t.media_taxa_desistencia, 2) AS media_taxa_desistencia,
            ROUND(r.variacao_remuneracao, 2) AS variacao_remuneracao
        FROM TaxaDesistenciaPorArea t
        JOIN RemuneracaoPorArea r ON t.area_cod = r.area_cod
        ORDER BY variacao_remuneracao DESC NULLS LAST;
        """
    ]
    execute_query(query_2[0], query_2[1], query_2[2])

    query_3 = [
        3,
        "Relação entre estados com queda na remuneração e taxa de desistência média dos cursos de graduação",
        """
        WITH RemuneracaoDelta AS (
            SELECT 
                uf_sigla,
                MAX(CASE WHEN ano = 2023 THEN media_remuneracao END) -
                MIN(CASE WHEN ano = 2020 THEN media_remuneracao END) AS delta_remuneracao
            FROM "Remuneracao_Media_Por_UF"
            WHERE ano IN (2020, 2023)
            GROUP BY uf_sigla
        ),
        DesistenciaDelta AS (
            SELECT 
                i.uf_sigla,
                AVG(CASE WHEN tc.ano_referencia = 2023 THEN tc.taxa_desistencia END) -
                AVG(CASE WHEN tc.ano_referencia = 2020 THEN tc.taxa_desistencia END) AS delta_desistencia
            FROM "Trajetoria_Curso" tc
            JOIN "Curso" c ON tc.curso_cod = c.curso_cod
            JOIN "Instituicao_Superior" i ON c.inst_cod = i.inst_cod
            WHERE tc.ano_referencia IN (2020, 2023)
            GROUP BY i.uf_sigla
        )
        SELECT 
            uf.uf_nome,
            ROUND(d.delta_desistencia, 2) AS aumento_desistencia,
            ROUND(r.delta_remuneracao, 2) AS variacao_remuneracao
        FROM DesistenciaDelta d
        JOIN RemuneracaoDelta r ON d.uf_sigla = r.uf_sigla
        JOIN "Unidade_Federativa" uf ON uf.uf_sigla = d.uf_sigla
        WHERE d.delta_desistencia > 0 AND r.delta_remuneracao < 0
        ORDER BY d.delta_desistencia DESC;
        """
    ]
    execute_query(query_3[0], query_3[1], query_3[2])

    query_4 = [
        4,
        "Relação entre estados com aumento de remuneração e taxa de desistência média dos cursos de graduação",
        """
        WITH RemuneracaoPorUF AS (
            SELECT 
                uf_sigla,
                MAX(CASE WHEN ano = 2022 THEN media_remuneracao END) AS remuneracao_fim,
                MIN(CASE WHEN ano = 2020 THEN media_remuneracao END) AS remuneracao_inicio
            FROM "Remuneracao_Media_Por_UF"
            WHERE ano IN (2020, 2022)
            GROUP BY uf_sigla
        ),
        DesistenciaPorUF AS (
            SELECT 
                i.uf_sigla,
                AVG(tc.taxa_desistencia) AS media_desistencia
            FROM "Trajetoria_Curso" tc
            JOIN "Curso" c ON tc.curso_cod = c.curso_cod
            JOIN "Instituicao_Superior" i ON c.inst_cod = i.inst_cod
            WHERE tc.ano_referencia BETWEEN 2020 AND 2022
            GROUP BY i.uf_sigla
        )
        SELECT 
            uf.uf_nome,
            ROUND(r.remuneracao_fim - r.remuneracao_inicio, 2) AS variacao_remuneracao,
            ROUND(d.media_desistencia, 2) AS taxa_media_desistencia
        FROM RemuneracaoPorUF r
        JOIN DesistenciaPorUF d ON r.uf_sigla = d.uf_sigla
        JOIN "Unidade_Federativa" uf ON uf.uf_sigla = r.uf_sigla
        WHERE r.remuneracao_fim > r.remuneracao_inicio
        ORDER BY taxa_media_desistencia DESC;
        """
    ]
    execute_query(query_4[0], query_4[1], query_4[2])

    query_5 = [
        5,
        "Partindo de um ano de referência, identifica quantos foram os ingressantes de uma determinada área em uma instituição específica",
        """
        SELECT 
            i.inst_nome,
            a.nome_area_atuacao,
            tc.ano_referencia,
            SUM(tc.num_ingressantes) AS total_ingressantes
        FROM "Trajetoria_Curso" tc
        JOIN "Curso" c ON tc.curso_cod = c.curso_cod
        JOIN "Area_Atuacao" a ON c.area_cod = a.area_cod
        JOIN "Instituicao_Superior" i ON c.inst_cod = i.inst_cod
        WHERE 
            tc.ano_referencia = 2023
            AND a.nome_area_atuacao = 'Computação e Tecnologias da Informação e Comunicação (TIC)'
            AND (i.inst_nome = ''
                OR i.inst_cod = 54)
        GROUP BY 
            i.inst_cod, i.inst_nome, a.nome_area_atuacao, tc.ano_referencia;
        """
    ]
    execute_query(query_5[0], query_5[1], query_5[2])

if __name__ == "__main__":
    main()
