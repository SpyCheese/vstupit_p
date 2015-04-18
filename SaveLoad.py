# Вступительная работа в параллель P.
# SaveLoader.py
# Модуль, предназначенный для сохранения и загрузки
# промежуточных результатов выполнения программы

import sys
import os
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
        print("Файл", fileName, "не существует или повреждён", file = sys.stderr)
        return False

    # Получение основных параметров из файла
    try :
        xmlConfig = xml.xpath('/root/config')[0]
    except IndexError :
        print("Файл", fileName, "не существует или повреждён", file = sys.stderr)
        return False

    config.siteUrl = xmlConfig.get("siteUrl")
    config.outputFile = xmlConfig.get("outputFile")
    config.pageTitle = xmlConfig.get("pageTitle")
    try :
        config.pagesCount = int(xmlConfig.get("pagesCount"))
        if config.pagesCount <= 0 :
            raise ValueError
    except ValueError :
        print("Файл", fileName, "не существует или повреждён", file = sys.stderr)
        return False

    # Значение euoffset
    try :
        config.startEUOffset = int(xml.xpath("/root/euoffset")[0].get("value"))
    except (IndexError, ValueError) :
        print("Файл", fileName, "не существует или повреждён", file = sys.stderr)
        return False

    # Страницы
    for item in xml.xpath("/root/pages/page") :
        try :
            page = Page()
            page.name = item.get("name")
            page.extLinksCount = int(item.get("extLinksCount"))
            config.startIdToPage[int(item.get("id"))] = page
        except ValueError :
            print("Файл", fileName, "не существует или повреждён", file = sys.stderr)
            return False

    print("Данные загружены", file = sys.stderr)
    return True

# ========================================================================================
# saveData - сохраняет данные в файл
def saveData(config, idToPage, euoffset) :
    print("Сохранение данных на диск", file = sys.stderr)
    # Создание корневого элемента
    xmlRoot = etree.Element("root")
    # Конфигурация
    xmlConfig = etree.SubElement(xmlRoot, "config")
    xmlConfig.set("siteUrl", config.siteUrl)
    xmlConfig.set("outputFile", config.outputFile)
    xmlConfig.set("pageTitle", config.pageTitle)
    xmlConfig.set("pagesCount", str(config.pagesCount))
    # euoffset
    xmlEUOffset = etree.SubElement(xmlRoot, "euoffset")
    xmlEUOffset.set("value", str(euoffset))
    # Страницы
    xmlPages = etree.SubElement(xmlRoot, "pages")
    for page in idToPage.items() :
        xmlPage = etree.SubElement(xmlPages, "page")
        xmlPage.set("id", str(page[0]))
        xmlPage.set("name", page[1].name)
        xmlPage.set("extLinksCount", str(page[1].extLinksCount))

   # Запись в файл
    try :
        file = open(fileName, 'wb')
    except OSError :
        print('Ошибка: не удалось создать файл', fileName, file = sys.stderr)
        exit(1)
    file.write(etree.tostring(xmlRoot))
    file.close()

# ========================================================================================
# clearData - удаляет файл с сохранёнными данными.
def clearData() :
    try :
        os.remove(fileName)
    except OSError :
        pass