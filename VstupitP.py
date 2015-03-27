#!/usr/bin/python3
# Вступительная работа в параллель P.
# VstupitP.py
# Главный файл программы.

import ConfigParser
import WikiGetter
import HtmlWriter


# ========================================================================================
# Парсинг файла конфигурации
configFileName = 'config.ini'
config = ConfigParser.parse(configFileName)

# Получение списка статей с внешними ссылками с помощью MetaWiki API
pages = WikiGetter.getPagesWithExtLinks(config)

# Создание html-страницы
HtmlWriter.createPage(config, pages)
