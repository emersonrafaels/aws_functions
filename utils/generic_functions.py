"""

    FUNÇÕES GENÉRICAS UTILIZANDO PYTHON.

    # Arguments

    # Returns


"""

__version__ = "1.0"
__author__ = """Emerson V. Rafael (EMERVIN)"""
__data_atualizacao__ = "27/06/2023"


from collections import OrderedDict
import datetime
from inspect import stack
from os import path, makedirs, walk, getcwd
import time
from typing import Union
from unidecode import unidecode
import re


def verify_exists(dir: str) -> bool:
    """

    FUNÇÃO PARA VERIFICAR SE UM DIRETÓRIO (PATH) EXISTE.

    # Arguments
        dir                  - Required : Diretório a ser verificado (String)

    # Returns
        validator            - Required : validator da função (Boolean)

    """

    # INICIANDO O validator DA FUNÇÃO
    validator = False

    try:
        validator = path.exists(dir)
    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {]".format(stack()[0][3], ex))

    return validator


def get_files_directory(
    directory: str, format_types_accepted: Union[tuple, list]
) -> list:
    """

    FUNÇÃO PARA OBTER OS ARQUIVOS EM UM DETERMINADO DIRETÓRIO
    FILTRANDO APENAS OS ARQUIVOS DOS FORMATOS ACEITOS POR ESSA API

    # Arguments
        directory                    - Required : Caminho/Diretório para obter os arquivos (String)
        format_types_accepted        - Required : Tipos de arquivos aceitos (List)

    # Returns
        list_archives_accepted       - Required : Caminho dos arquivos listados (List)

    """

    # INICIANDO A VARIÁVEL QUE ARMAZENARÁ O RESULTADO
    list_archives_accepted = []

    try:
        # OBTENDO A LISTA DE ARQUIVOS CONTIDOS NO DIRETÓRIO
        for root in walk(directory):
            for dir in root:
                for files in dir:
                    if path.splitext(files)[1] in format_types_accepted:
                        list_archives_accepted.append(path.join(root[0], files))

    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {]".format(stack()[0][3], ex))

    return list_archives_accepted


def create_path(dir: str) -> bool:
    """

    FUNÇÃO PARA CRIAR UM DIRETÓRIO (PATH).

    # Arguments
        dir                  - Required : Diretório a ser criado (String)

    # Returns
        validator            - Required : validator da função (Boolean)

    """

    # INICIANDO O validator DA FUNÇÃO
    validator = False

    try:
        # REALIZANDO A CRIAÇÃO DO DIRETÓRIO
        makedirs(dir)

        validator = True
    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {]".format(stack()[0][3], ex))

    return validator


def get_date_time_now(return_type: str) -> str:
    """

    OBTÉM TODOS OS POSSÍVEIS RETORNOS DE DATA E TEMPO.

    # Arguments
        return_type                    - Required : Formato de retorno. (String)

    # Returns

    """

    """%d/%m/%Y %H:%M:%S | %Y-%m-%d %H:%M:%S
    Dia: %d
    Mês: %
    Ano: %Y
    Data: %Y/%m/%d

    Hora: %H
    Minuto: %M
    Segundo: %S"""

    try:
        ts = time.time()
        stfim = datetime.datetime.fromtimestamp(ts).strftime(return_type)

        return stfim
    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))
        return datetime.datetime.now()
