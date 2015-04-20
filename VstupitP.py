#!/usr/bin/python3
# Вступительная работа в параллель P.
# VstupitP.py
# Главный файл программы.

import sys
import threading

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
    savedDataFile = "savedData.xml"
    configFile = "config.ini"

    # Параметры из файла конфигурации
    siteUrl = ""
    outputFile = ""
    pageTitle = ""
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
    ConfigParser.parse(config)

# Получение списка статей с внешними ссылками с помощью MetaWiki API
# Запуск отдельного потока; главный будет отлавливать KeyboardInterrupt
wikiGetterResult = WikiGetter.Result()
wikiGetterThread = threading.Thread(target = WikiGetter.getPagesWithExtLinks, args = (config, wikiGetterResult))
wikiGetterThread.start()
while True :
    try :
        wikiGetterThread.join()
        break
    except KeyboardInterrupt :
        WikiGetter.interrupt()

# Если всё готово или выставлен флаг --no-saving, создать страницу,
# иначе - записать в файл
if wikiGetterResult.done or config.noSaving :
    pages = WikiGetter.createList(wikiGetterResult.idToPage, config.pagesCount)
    HtmlWriter.createPage(config, pages)
    if not config.noSaving :
        SaveLoad.clearData(config)
else :
    SaveLoad.saveData(config, wikiGetterResult.idToPage, wikiGetterResult.euoffset)
