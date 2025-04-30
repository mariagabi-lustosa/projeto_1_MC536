query2 = """
SELECT 
    ano,
    area,
    estado,
    instituicao,
    SUM(ingressantes) AS total_ingressantes
FROM 
    ingressantes
WHERE 
    ano = 2023
    AND area = 'Engenharia'
    AND estado = 'SP'
GROUP BY 
    ano, area, estado, instituicao;
"""

query_sqlite(db_path, query)
