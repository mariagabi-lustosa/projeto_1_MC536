def query_ingressantes(db_path, ano, area, estado=None, instituicao=None):
    # Monta o filtro dinâmico
    filtros = f"ano = {ano} AND area = '{area}'"
    if estado:
        filtros += f" AND estado = '{estado}'"
    if instituicao:
        filtros += f" AND instituicao = '{instituicao}'"


query_ingressantes(db_path, ano=2023, area='Engenharia', estado='SP')


    query = f"""
    SELECT 
        ano,
        area,
        estado,
        instituicao,
        SUM(ingressantes) AS total_ingressantes
    FROM 
        ingressantes
    WHERE 
        {filtros}
    GROUP BY 
        ano, area, estado, instituicao;
    """

    conn = sqlite3.connect(db_path)
    resultado = pd.read_sql_query(query, conn)
    conn.close()

    print(resultado)
