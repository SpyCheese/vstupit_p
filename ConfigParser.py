# Вступительная работа в параллель P.
# ConfigParser.py
# Модуль, предназначенный для парсинга файла конфигурации.

import configparser
import sys


# ========================================================================================
# Config - структура, возвращаемая из функции parse
class Config :
    siteUrl = ''
    outputFile = ''
    pageTitle = ''
    pagesCount = 0


# ========================================================================================
# getParamStr - возвращает значение параметра из файла концигурации.
# Завершает программу с ошибкой при его отсутствии.
def getParamStr(configFile, param) :
    if param not in configFile['DEFAULT'] :
        print('Ошибка: в файле конфигурации отсутствует параметр', param, file = sys.stderr)
        exit(1)
    return configFile['DEFAULT'][param]


# ========================================================================================
# getParamInt - возвращает значение параметра из файла концигурации, преобразованное к числовому типу.
# Завершает программу с ошибкой при его отсутствии или неверном формате.
def getParamInt(configFile, param) :
    try :
        a = int(getParamStr(configFile, param))
        if a <= 0 :
            raise ValueError
        return a
    except ValueError :
        print('Ошибка: некорректное значение', param, file = sys.stderr)
        exit(1)


# ========================================================================================
# parse - открывает файл fileName и считывает из него параметры.
def parse(fileName) :
    print('Парсинг файла', fileName, file = sys.stderr)
    configFile = configparser.ConfigParser()
    configFile.read(fileName)
    c = Config()

    c.siteUrl = getParamStr(configFile, 'siteUrl')
    c.outputFile = getParamStr(configFile, 'outputFile')
    c.pageTitle = getParamStr(configFile, 'pageTitle')
    c.pagesCount = getParamInt(configFile, 'pagesCount')

    return c
