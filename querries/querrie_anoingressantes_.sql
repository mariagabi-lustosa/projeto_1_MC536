query_ano_curso_media = """
SELECT
    curso_nome AS curso_nome,
    ano_ingresso AS ano_referencia,
    SUM(ingressantes) AS num_ingressantes
FROM public."indicadores_educacao.csv"
JOIN public."rais_tabela6_2023.csv" t ON i.ano_referencia = t.ano
WHERE
    ano_ingresso=  2023
    AND t.remuneracao = 3000
GROUP BY curso_nome, ano_ingresso
ORDER BY ano_ingresso;
"""


execute_query(5, "admissions in aourses with average Remuneration of 3000, bwtween 2019-2023", query)
