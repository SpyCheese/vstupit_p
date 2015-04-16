#!/usr/bin/python3
# Вступительная работа в параллель P.
# VstupitP.py
# Главный файл программы.

import sys

import CommandLineParser
import ConfigParser
import HelpString
import WikiGetter
import HtmlWriter

# ========================================================================================
# Config - структура, содержащая параметры запуска программы
class Config :
    showHelp = False
    restart = False
    noSaving = False

    siteUrl = ''
    outputFile = ''
    pageTitle = ''
    pagesCount = 0
config = Config()

# ========================================================================================
# Парсинг аргументов командной строки
CommandLineParser.parse(config)

# Вывод справки, если есть ключ --help
if config.showHelp :
    print(HelpString.helpString, file = sys.stderr)
    exit(0)

# Парсинг файла конфигурации
configFileName = 'config.ini'
ConfigParser.parse(configFileName, config)

# Получение списка статей с внешними ссылками с помощью MetaWiki API
pages = WikiGetter.getPagesWithExtLinks(config)

# Создание html-страницы
HtmlWriter.createPage(config, pages)
