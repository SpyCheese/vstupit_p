#!/usr/bin/python3
# Вступительная работа в параллель P.
# VstupitP.py
# Главный файл программы.

import sys

import CommandLineParser
import ConfigParser
import SaveLoad
import HelpString
import WikiGetter
import HtmlWriter

# ========================================================================================
# Config - структура, содержащая параметры запуска программы
class Config :
    # Параметры командной строки
    showHelp = False
    restart = False
    noSaving = False

    # Параметры из файла config.ini
    siteUrl = ''
    outputFile = ''
    pageTitle = ''
    pagesCount = 0

    # Данные, сохранённые ранее в файл
    startEUOffset = 0
    startIdToPage = {}
config = Config()

# ========================================================================================
# Парсинг аргументов командной строки
CommandLineParser.parse(config)

# Вывод справки, если есть ключ --help
if config.showHelp :
    print(HelpString.helpString, file = sys.stderr)
    exit(0)

# Если не выставлен флаг --restart, считать файл с сохранёнными данными
if not config.restart :
    success = SaveLoad.loadData(config)
    # Если не удалось считать данные, начать с начала
    if not success :
        config.restart = True

# Парсинг файла конфигурации, если нужно начинать процесс с начала
if config.restart :
    configFileName = 'config.ini'
    ConfigParser.parse(configFileName, config)

# Получение списка статей с внешними ссылками с помощью MetaWiki API
pages = WikiGetter.getPagesWithExtLinks(config)

# Создание html-страницы
HtmlWriter.createPage(config, pages)
