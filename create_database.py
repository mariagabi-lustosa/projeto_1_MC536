import psycopg2
import argparse
import os
import pandas as pd
import numpy as np
import csv
import json
import datetime
import re


def create_database(cursor):
    """ Create the database if it does not exist.
    
    Args:
        cursor: The database cursor.
    """
    
    table_schema = """
        BEGIN;


        CREATE TABLE IF NOT EXISTS public."Area_Atuacao"
        (
            area_cod character varying(10) COLLATE pg_catalog."default" NOT NULL,
            nome_area_atuacao character varying(100) COLLATE pg_catalog."default",
            CONSTRAINT "Area_Atuacao_pkey" PRIMARY KEY (area_cod)
        );

        CREATE TABLE IF NOT EXISTS public."Curso"
        (
            curso_cod integer NOT NULL,
            curso_nome character varying(150) COLLATE pg_catalog."default",
            grau_academico character varying(50) COLLATE pg_catalog."default",
            modo_ensino character varying(30) COLLATE pg_catalog."default",
            area_cod character varying(10) COLLATE pg_catalog."default",
            inst_cod integer,
            CONSTRAINT "Curso_pkey" PRIMARY KEY (curso_cod)
        );

        CREATE TABLE IF NOT EXISTS public."Emprego_Por_Setor_E_Municipio"
        (
            ano integer NOT NULL,
            municipio_cod integer NOT NULL,
            setor_nome character varying(100) COLLATE pg_catalog."default" NOT NULL,
            num_pessoas_empregadas integer,
            CONSTRAINT "Emprego_Por_Setor_E_Municipio_pkey" PRIMARY KEY (ano, municipio_cod, setor_nome)
        );

        CREATE TABLE IF NOT EXISTS public."Instituicao_Superior"
        (
            inst_cod integer NOT NULL,
            inst_nome character varying(150) COLLATE pg_catalog."default",
            categoria_adm character varying(50) COLLATE pg_catalog."default",
            org_academica character varying(50) COLLATE pg_catalog."default",
            uf_sigla character(2) NOT NULL,
            CONSTRAINT "Instituicao_Superior_pkey" PRIMARY KEY (inst_cod)
        );

        CREATE TABLE IF NOT EXISTS public."Municipio"
        (
            municipio_cod integer NOT NULL,
            municipio_nome character varying(100) COLLATE pg_catalog."default",
            uf_sigla character(2) COLLATE pg_catalog."default",
            CONSTRAINT "Municipio_pkey" PRIMARY KEY (municipio_cod)
        );

        CREATE TABLE IF NOT EXISTS public."Relacao_Area_Setor"
        (
            area_cod character varying(10) COLLATE pg_catalog."default" NOT NULL,
            setor_nome character varying(100) COLLATE pg_catalog."default" NOT NULL,
            grau_relacao numeric(3, 2),
            CONSTRAINT "Relacao_Area_Setor_pkey" PRIMARY KEY (area_cod, setor_nome)
        );

        CREATE TABLE IF NOT EXISTS public."Remuneracao_Media_Por_UF"
        (
            ano integer NOT NULL,
            uf_sigla character(2) COLLATE pg_catalog."default",
            media_remuneracao numeric(10, 2),
            CONSTRAINT "Remuneracao_Media_Por_UF_pkey" PRIMARY KEY (ano)
        );

        CREATE TABLE IF NOT EXISTS public."Setor_Economico"
        (
            setor_nome character varying(100) COLLATE pg_catalog."default" NOT NULL,
            CONSTRAINT "Setor_Economico_pkey" PRIMARY KEY (setor_nome)
        );

        CREATE TABLE IF NOT EXISTS public."Trajetoria_Curso"
        (
            curso_cod integer NOT NULL,
            ano_referencia integer NOT NULL,
            num_ingressantes integer,
            num_concluintes integer,
            taxa_desistencia numeric(5, 2),
            CONSTRAINT "Trajetoria_Curso_pkey" PRIMARY KEY (curso_cod, ano_referencia)
        );

        CREATE TABLE IF NOT EXISTS public."Unidade Federativa"
        (
            uf_sigla character(2) COLLATE pg_catalog."default" NOT NULL,
            uf_nome character varying(50) COLLATE pg_catalog."default",
            CONSTRAINT "Unidade Federativa_pkey" PRIMARY KEY (uf_sigla)
        );

        ALTER TABLE IF EXISTS public."Curso"
            ADD CONSTRAINT area_cod FOREIGN KEY (area_cod)
            REFERENCES public."Area_Atuacao" (area_cod) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION;


        ALTER TABLE IF EXISTS public."Curso"
            ADD CONSTRAINT inst_cod FOREIGN KEY (inst_cod)
            REFERENCES public."Instituicao_Superior" (inst_cod) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION;


        ALTER TABLE IF EXISTS public."Emprego_Por_Setor_E_Municipio"
            ADD CONSTRAINT municipio_cod FOREIGN KEY (municipio_cod)
            REFERENCES public."Municipio" (municipio_cod) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION;


        ALTER TABLE IF EXISTS public."Emprego_Por_Setor_E_Municipio"
            ADD CONSTRAINT setor_nome FOREIGN KEY (setor_nome)
            REFERENCES public."Setor_Economico" (setor_nome) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION;


        ALTER TABLE IF EXISTS public."Instituicao_Superior"
            ADD CONSTRAINT uf_sigla FOREIGN KEY (uf_sigla)
            REFERENCES public."Unidade Federativa" (uf_sigla) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
            NOT VALID;


        ALTER TABLE IF EXISTS public."Municipio"
            ADD CONSTRAINT uf_sigla FOREIGN KEY (uf_sigla)
            REFERENCES public."Unidade Federativa" (uf_sigla) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION;


        ALTER TABLE IF EXISTS public."Relacao_Area_Setor"
            ADD CONSTRAINT area_cod FOREIGN KEY (area_cod)
            REFERENCES public."Area_Atuacao" (area_cod) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION;


        ALTER TABLE IF EXISTS public."Relacao_Area_Setor"
            ADD CONSTRAINT setor_nome FOREIGN KEY (setor_nome)
            REFERENCES public."Setor_Economico" (setor_nome) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION;


        ALTER TABLE IF EXISTS public."Remuneracao_Media_Por_UF"
            ADD CONSTRAINT uf_sigla FOREIGN KEY (uf_sigla)
            REFERENCES public."Unidade Federativa" (uf_sigla) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION;


        ALTER TABLE IF EXISTS public."Trajetoria_Curso"
            ADD CONSTRAINT curso_cod FOREIGN KEY (curso_cod)
            REFERENCES public."Curso" (curso_cod) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION;

        END;
    """

    cursor.execute(table_schema)


def main(create_bool):
    """ Main function to create the database and tables.

    Args:
        create_bool: Boolean to create the database and tables.
    """
    
    connection = psycopg2.connect(
        dbname = 'projeto_1',
        user = 'admin',
        password = 'admin123',
        host = 'postgres',
        port = '5432'
    )
    cursor = connection.cursor()

    if create_bool == "True":
        create_database(cursor)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Create database and tables.'
    )
    parser.add_argument(
        '-c',
        '--create_bool',
        default=False,
        help='Boolean to create the database and tables.'
    )
    args = parser.parse_args()
    create_bool = args.create_bool
    main(create_bool)
    
