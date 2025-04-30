### projeto_MC536

### Membros:  
&nbsp;&nbsp;&nbsp;Maria Gabriela Lustosa de Oliveira - RA:83183901  
&nbsp;&nbsp;&nbsp;Gabriel Cabra; - RA:83183901  
&nbsp;&nbsp;&nbsp;Flavia Juliana Ventilari dos Santos - RA: 260438  


### Glossário

## [Descrição do Projeto](#descrica-do-projeto)
## [Esquema dos Databases](#esquema-dos-databases)
## [Datasets](#datasets)
## [Tecnologias Ultilizadas](#linguagens-ultilizadas)
## [Organização do Projeto](#Organização-do-projeto)
## [Data Processing](#data-processing)
## [Queries](#queries)


### Descrição do Projeto

Nosso projeto para a disciplica MC536 - Banco de Dados visa estabelecer uma ligação entre os dados de conluintes do ensino superior no Brasil em determinada área do conhecimento, e os dados referentes as ofertas de emprego para essas áreas, analisando os dados com base em UF, Município e >>>.

### Descrição dos Databases

![Preview do Modelo Conceitual](models/conceptual_model.png)
![Preview do Modelo Relacional](models/relational_model.png)
## [Modelo Físico:](models/physical_model.sql)




### Tecnologias Ultilizadas

**DataBase**:PostgreSQL 
**Linguagem**: Python
**Bibliotecas**: panda, sql ect etc deps vejo

## Organização do Projeto

<pre> ```markdown 📁 meu-repo/ ├── README.md ├── datasets/ │ ├── indicadores_educacao.csv │ ├── rais_tabela4_2021.csv │ ├── rais_tabela4_2023.csv │ ├── rais_tabela4_joined.csv │ ├── rais_tabela6_2021.csv │ ├── rais_tabela6_2023.csv │ └── rais_tabela6_joined.csv ├── models/ │ ├── conpectual_models.png │ ├── physical_model.sql │ └── relational_model.png ├── preprocessed_dataset/ │ ├── RAIS_ano_base_2021_TABELA4.csv │ ├── RAIS_ano_base_2021_TABELA6.csv │ ├── RAIS_ano_base_2023_TABELA4.csv │ ├── RAIS_ano_base_2023_TABELA6.csv │ └── indicadores_trajetoria_educacao_superior_2019_2023.csv ├── projeto1/ ├── arquivos/ │ ├── create_database.py │ ├── fill_database.py │ ├── process_datasets.py │ └── querries.py ├── main.py ``` </pre>




