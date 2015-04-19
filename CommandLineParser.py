# Вступительная работа в параллель P.
# CommandLineParser.py
# Модуль, предназначенный для парсинга аргументов командной строки.

import sys

# ========================================================================================
# parse - парсит аргументы командной строки и записывает их в структуру config.
def parse(config) :
    i = 1
    while i < len(sys.argv) :
        param = sys.argv[i]
        if len(param) >= 2 and param[0:2] == "--" :
            if param == "--help" :         # Показать справку
                config.showHelp = True
            elif param == "--restart" :    # Начать делать запросы заново, не с сохранённого места
                config.restart = True
            elif param == "--no-saving" :  # При прерывании обработки списка прекратить работу, а не сохранять её
                config.noSaving = True
            elif param == "--saved-data" : # Имя файла для сохранённых данных
                if i == len(sys.argv) - 1 :
                    print("Ошибка: не указано имя файла для сохранённых данных")
                    exit(1)
                i += 1
                config.savedDataFile = sys.argv[i]
            elif param == "--config" : # Имя файла конфигурации
                if i == len(sys.argv) - 1 :
                    print("Ошибка: не указано имя файла конфигурации")
                    exit(1)
                i += 1
                config.configFile = sys.argv[i]
            else :
                print("Ошибка: неизвестный параметр", param, file = sys.stderr)
                exit(1)
        elif len(param) >= 2 and param[0] == "-" : # Парсинг однобуквенных ключей
            for c in param[1:] :
                if c == "h" :
                    config.showHelp = True
                elif c == "r" :
                    config.restart = True
                elif c == "n" :
                    config.noSaving = True
                else :
                    print("Ошибка: неизвестный ключ -" + c, file = sys.stderr)
                    exit(1)
        else :
            print("Ошибка: неизвестный параметр", param, file = sys.stderr)
            exit(1)
        i += 1

