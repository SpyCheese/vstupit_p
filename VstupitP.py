#!/usr/bin/python3
# Вступительная работа в параллель P.
# VstupitP.py
# Главный файл программы.

import sys

import ConfigParser
import WikiGetter

# Парсинг файла конфигурации
configFileName = 'config.ini'
print('Парсинг файла', configFileName, file = sys.stderr)
config = ConfigParser.parse(configFileName)

# Получение списка статей с внешними ссылками с помощью MetaWiki API
pages = WikiGetter.getPagesWithExtLinks(config)
for i in pages :
    print(i.name, i.extLinksCount, file = sys.stderr)