# Вступительная работа в параллель P.
# CommandLineParser.py
# Модуль, предназначенный для парсинга аргументов командной строки.

import sys

# ========================================================================================
# parse - парсит аргументы командной строки и записывает их в структуру config.
def parse(config) :
    for param in sys.argv[1:] :
        if len(param) >= 2 and param[0:2] == "--" :
            if param == "--help" :        # Показать справку
                config.showHelp = True
            elif param == "--restart" :   # Начать делать запросы заново, не с сохранённого места
                config.restart = True
            elif param == "--no-saving" : # При прерывании обработки списка прекратить работу, а не сохранять её
                config.noSaving = True
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



