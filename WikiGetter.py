# Вступительная работа в параллель P.
# WikiGetter.py
# Модуль, предназначенный для получения нужной информации из Википедии.

import urllib.request
import sys
from lxml import etree

EULIMIT = 500
LIST_PARSING_OUTPUT_PERIOD = 40

# Page - структура, содежащая  информацию о странице
class Page :
    name = ''
    extLinksCount = 0

# parseExtUrlResponse - парсинг списка внешних ссылок и добавление в словарь.
# Возвращает новый euoffset или -1, если это конец
def parseExtUrlResponse(file, idToCount, idToName) :
    try:
        responseXml = etree.parse(file)
    except etree.XMLSyntaxError as error :
        print('Ошибка: не удалось распарсить полученный XML.', error, file = sys.stderr)
        exit(1)

    # Получение нового значения euoffset
    xmlQueryContinue = responseXml.xpath('/api/query-continue/exturlusage')
    if len(xmlQueryContinue) == 0 :
        newOffset = -1
    else :
        try :
            newOffset = int(xmlQueryContinue[0].get('euoffset'))
        except ValueError :
            print('Ошибка: полученный XML имеет неверный формат', file = sys.stderr)
            exit(1)

    # Просмотр списка внешних ссылок
    xmlExtUrls = responseXml.xpath('/api/query/exturlusage/eu')
    for item in xmlExtUrls :
        try :
            pageId = int(item.get('pageid'))
            # Добавление имени стстьи в словарь имён
            if pageId not in idToName :
                idToName[pageId] = item.get('title')
        except ValueError :
            print('Ошибка: полученный XML имеет неверный формат', file = sys.stderr)
            exit(1)
        # Увеличение счётчита ссылок статьи
        if pageId not in idToCount :
            idToCount[pageId] = 1
        else :
            idToCount[pageId] += 1

    return newOffset

# createList - создаёт список статей на основе количества ссылок,
# сортирует по убыванию и оставляет pagesCount элементов
def createList(idToCount, idToName, pagesCount) :
    # Создание массива
    pages = []
    for i in idToCount :
        page = Page()
        page.name = idToName[i]
        page.extLinksCount = idToCount[i]
        pages.append(page)
    # Сортировка по количеству ссылок
    pages.sort(key = (lambda x : x.extLinksCount), reverse = True)
    # Удаление лишник статей из списка
    if len(pages) > pagesCount :
        pages = pages[:pagesCount]
    return pages

# getPagesWithExtLinks - функция, возвращающая список страниц
# с указанием количества внешних ссылок.
def getPagesWithExtLinks(config) :
    print('Получение информации с', config.siteUrl, file = sys.stderr)

    # Количество ссылок в статьях
    idToCount = {}
    # Имена снатей
    idToName = {}

    # URL запроса
    apiUrl = config.siteUrl + '/w/api.php'
    extUrlRequestUrl = apiUrl + '?'
    extUrlRequestUrl += 'action=query&'
    extUrlRequestUrl += 'list=exturlusage&'
    extUrlRequestUrl += 'format=xml&'
    extUrlRequestUrl += 'eunamespace=0&'
    extUrlRequestUrl += 'eulimit={eulimit:d}&'
    extUrlRequestUrl += 'euoffset={euoffset:d}'

    euoffset = 0
    outputPeriodLeft = LIST_PARSING_OUTPUT_PERIOD
    try :
        while True :
            # Запрос к MediaWiki API на получение данных
            try :
                response = urllib.request.urlopen(extUrlRequestUrl.format(eulimit = EULIMIT, euoffset = euoffset))
            except (urllib.error.URLError, ValueError) :
                print('Ошибка: не удалось соединиться с', config.siteUrl, file = sys.stderr)
                exit(1)

            # Парсинг xml и получение данных
            euoffset = parseExtUrlResponse(response, idToCount, idToName)
            if euoffset == -1 :
                break

            # Каждые LIST_PARSING_OUTPUT_PERIOD итераций вывод в stderr количества обработанных ссылок
            outputPeriodLeft -= 1
            if outputPeriodLeft == 0 :
                outputPeriodLeft = LIST_PARSING_OUTPUT_PERIOD
                print('Обработано', euoffset, 'ссылок...', file = sys.stderr)
    except KeyboardInterrupt :
        print('Процесс обработки списка ссылок прерван пользователем', file = sys.stderr)

    # Создание массива и сортировка
    print('Сортировка страниц по убыванию количества ссылок', file = sys.stderr)
    pages = createList(idToCount, idToName, config.pagesCount)

    return pages
