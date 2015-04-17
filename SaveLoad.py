# Вступительная работа в параллель P.
# SaveLoader.py
# Модуль, предназначенный для сохранения и загрузки
# промежуточных результатов выполнения программы

import sys
from lxml import etree
from WikiGetter import Page

# ========================================================================================
fileName = "savedData.xml"

# ========================================================================================
# loadData - загрузить данные и записать их в config.as
# Возвращает True в случае успеха
def loadData(config) :
    print("Попытка загрузить ранее сохранённые данные", file = sys.stderr)
    try :
        xml = etree.parse(fileName)
    except (OSError, etree.XMLSyntaxError) :
        print("Файл", fileName, "не существует или повреждён.", file = sys.stderr)
        return False

    # Получение основных параметров из файла
    try :
        xmlConfig = xml.xpath('/config')[0]
    except IndexError :
        print("Файл", fileName, "не существует или повреждён.", file = sys.stderr)
        return False

    config.siteUrl = xmlConfig.get("siteUrl")
    config.outputFile = xmlConfig.get("oututFile")
    config.pageTitle = xmlConfig.get("pageTitle")
    try :
        config.pagesCount = int(xmlConfig.get("pagesCount"))
    except ValueError :
        print("Файл", fileName, "не существует или повреждён.", file = sys.stderr)
        return False

    # Значение euoffset
    try :
        config.startEUOffset = int(xml.xpath("/euoffset")[0].get("value"))
    except (IndexError, ValueError) :
        print("Файл", fileName, "не существует или повреждён.", file = sys.stderr)
        return False

    # Страницы
    for item in xml.xpath("/page") :
        try :
            page = Page()
            page.name = item.get("name")
            page.extLinksCount = int(item.get("extLinksCount"))
            config.startIdToPage[int(item.get("id"))] = page
        except ValueError :
            print("Файл", fileName, "не существует или повреждён.", file = sys.stderr)
            return False

    print("Данные загружены", file = sys.stderr)
    return True
