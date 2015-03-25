# Вступительная работа в параллель P.
# ConfigParser.py
# Модуль, предназначенный для парсинга файла конфигурации.

import configparser
import sys

# Config - структура, возвращаемая из функции parse
class Config :
    siteUrl = ''
    outputFile = ''
    pageTitle = ''
    pagesCount = 0
    listParsingOutputPeriod = 0

# getParam - возвращает значение параметра из файла концигурации.
# Завершает программу с ошибкой при его отсутствии.
def getParam(configFile, param) :
    if param not in configFile['DEFAULT'] :
        print('Ошибка: в файле конфигурации отсутствует параметр', param, file = sys.stderr)
        exit(1)
    return configFile['DEFAULT'][param]

# parse - открывает файл fileName и считывает из него параметры.
def parse(fileName) :
    print('Парсинг файла', fileName, file = sys.stderr)
    configFile = configparser.ConfigParser()
    configFile.read(fileName)
    c = Config()

    c.siteUrl = getParam(configFile, 'siteUrl')
    c.outputFile = getParam(configFile, 'outputFile')
    c.pageTitle = getParam(configFile, 'pageTitle')
    try :
        c.pagesCount = int(getParam(configFile, 'pagesCount'))
        if c.pagesCount <= 0 :
            raise ValueError()
    except ValueError :
        print('Ошибка: некорректное значение pagesCount', file = sys.stderr)
        exit(1)
    try :
        c.listParsingOutputPeriod = int(getParam(configFile, 'listParsingOutputPeriod'))
        if c.pagesCount <= 0 :
            raise ValueError()
    except ValueError :
        print('Ошибка: некорректное значение listParsingOutputPeriod', file = sys.stderr)
        exit(1)

    return c
