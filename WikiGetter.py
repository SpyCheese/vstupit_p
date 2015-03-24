# Вступительная работа в параллель P.
# WikiGetter.py
# Модуль, предназначенный для получения нужной информации из Википедии.

import urllib.request
import sys
from lxml import etree

eulimit = 500

# Page - структура, содежащая  информацию о странице
class Page :
    name = ''
    url = ''
    id = 0
    extLinksCount = 0

# parseExtUrlResponse - парсинг списка внешних ссылок и добавление в словарь.
# Возвращает новый euoffset или -1, если это конец
def parseExtUrlResponse(file, idToCount) :
    try:
        xml = etree.parse(file)
    except lxml.etree.XMLSyntaxError as error :
        print('Ошибка: не удалось распарсить полученный XML.', error, file = sys.stderr)
        exit(1)

    # Получение нового значения euoffset
    xmlQueryContinue = xml.xpath('/api/query-continue/exturlusage')
    if len(xmlQueryContinue) == 0 :
        newOffset = -1
    else :
        try :
            newOffset = int(xmlQueryContinue[0].get('euoffset'))
        except ValueError :
            print('Ошибка: полученный XML имеет неверный формат', file = sys.stderr)
            exit(1)

    # Просмотр списка внешних ссылок
    xmlExtUrls = xml.xpath('/api/query/exturlusage/eu')
    for item in xmlExtUrls :
        try :
            pageId = int(item.get('pageid'))
        except ValueError :
            print('Ошибка: полученный XML имеет неверный формат', file = sys.stderr)
            exit(1)
        if pageId not in idToCount :
            idToCount[pageId] = 1
        else :
            idToCount[pageId] += 1


    return newOffset

# createList - создаёт список статей на основе количества ссылок,
# сортирует по убыванию и оставляет pagesCount элементов
def createList(idToCount, pagesCount) :
    pages = []
    for i in idToCount :
        page = Page()
        page.id = i
        page.extLinksCount = idToCount[i]
        pages.append(page)
    pages.sort(key = (lambda x : -x.extLinksCount))
    if len(pages) > pagesCount :
        pages = pages[:pagesCount]
    return pages

# getPagesWithExtLinks - функция, возвращающая список страниц
# с указанием количества внешних ссылок.
def getPagesWithExtLinks(site, pagesCount) :
    print('Получение информации с', site, file = sys.stderr)

    # Количество ссылок в статьях
    idToCount = {}

    # URL запроса
    apiUrl = site + '/w/api.php'
    extUrlRequestUrl = apiUrl + '?'
    extUrlRequestUrl += 'action=query&'
    extUrlRequestUrl += 'list=exturlusage&'
    extUrlRequestUrl += 'format=xml&'
    extUrlRequestUrl += 'eulimit=' + str(eulimit) + '&'
    extUrlRequestUrl += 'euoffset='
    euoffset = 0
    while euoffset != -1 :
        # Запрос к MediaWiki API на получение данных
        try :
            response = urllib.request.urlopen(extUrlRequestUrl + str(euoffset))
        except (urllib.error.URLError, ValueError) :
            print('Ошибка: не удалось соединиться с', site, file = sys.stderr)
            exit(1)

        # Парсинг xml и получение данных
        euoffset = parseExtUrlResponse(response, idToCount)

    # Создание массива и сортировка
    print('Сортировка страниц по убыванию количества ссылок', file = sys.stderr)
    pages = createList(idToCount, pagesCount)
    for i in pages :
        print(i.id, i.extLinksCount, file = sys.stderr)

    # Получение информации о страницах (название, адрес)
