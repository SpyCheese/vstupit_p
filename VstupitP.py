#!/usr/bin/python3
# Вступительная работа в параллель P.
# VstupitP.py
# Главный файл программы.

import sys

import ConfigParser

# Парсинг файла конфигурации
configFileName = 'config.ini'
print('Парсинг файла', configFileName, file = sys.stderr)
config = ConfigParser.parse(configFileName)
