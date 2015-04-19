# Вступительная работа в параллель P.
# ConfigParser.py
# Модуль, предназначенный для парсинга файла конфигурации.

import configparser
import sys


# ========================================================================================
# getParamStr - возвращает значение параметра из файла конфигурации.
# Завершает программу с ошибкой при его отсутствии.
def getParamStr(configFile, param) :
    if param not in configFile['DEFAULT'] :
        print('Ошибка: в файле конфигурации отсутствует параметр', param, file = sys.stderr)
        exit(1)
    return configFile['DEFAULT'][param]


# ========================================================================================
# getParamInt - возвращает значение параметра из файла конфигурации, преобразованное к числовому типу.
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
def parse(config) :
    print('Парсинг файла', config.configFile, file = sys.stderr)
    configFile = configparser.ConfigParser()
    configFile.read(config.configFile)

    config.siteUrl = getParamStr(configFile, 'siteUrl')
    config.outputFile = getParamStr(configFile, 'outputFile')
    config.pageTitle = getParamStr(configFile, 'pageTitle')
    config.pagesCount = getParamInt(configFile, 'pagesCount')

    config.startEUOffset = 0
    config.startIdToPage = {}
