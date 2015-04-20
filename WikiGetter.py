# Вступительная работа в параллель P.
# WikiGetter.py
# Модуль, предназначенный для получения нужной информации из Википедии.

import urllib.request
import sys
import heapq
from lxml import etree

EULIMIT = 500
LIST_PARSING_OUTPUT_PERIOD = 40


# ========================================================================================
# Page - структура, содежащая информацию о странице
class Page :
    name = ""
    extLinksCount = 0


# ========================================================================================
# parseExtUrlResponse - парсинг списка внешних ссылок и добавление в словарь.
# Возвращает новый euoffset (или -1, если это конец)
def parseExtUrlResponse(file, idToPage) :
    responseXml = etree.parse(file)

    # Получение нового значения euoffset
    xmlQueryContinue = responseXml.xpath("/api/query-continue/exturlusage")
    if len(xmlQueryContinue) == 0 :
        newOffset = -1
    else :
        newOffset = int(xmlQueryContinue[0].get("euoffset"))

    # Просмотр списка внешних ссылок
    xmlExtUrls = responseXml.xpath("/api/query/exturlusage/eu")
    for item in xmlExtUrls :
        pageId = int(item.get("pageid"))
        if pageId not in idToPage :
            # Создание объекта Page, если этой статьи ещё не было
            page = Page()
            page.name = item.get("title")
            page.extLinksCount = 1
            idToPage[pageId] = page
        else :
            # Увеличение счётчика ссылок статьи
            idToPage[pageId].extLinksCount += 1

    return newOffset


# ========================================================================================
# createList - создаёт список из pagesCount статей
# с наибольшим количеством внешних ссылок.
def createList(idToPage, pagesCount) :
    return heapq.nlargest(pagesCount, idToPage.values(), key = (lambda x : x.extLinksCount))

# ========================================================================================
# interrupt - функция, прерывающая выполнение getPagesWithExtLinks
# interrupted - было ли выполнение прервано
interrupted = False
def interrupt() :
    global interrupted
    interrupted = True

# ========================================================================================
# Result - в экземпляр этого класса записываются результаты выполнения функции
# getPagesWithExtLinks
class Result :
    idToPage = {}   # Страницы
    done = False    # True, если обработка списка завершена
    euoffset = 0    # Значение euoffset, если процесс не завершён

# ========================================================================================
# getPagesWithExtLinks - функция, записывающая в result список страниц
# с указанием количества внешних ссылок.
def getPagesWithExtLinks(config, result) :
    print("Получение информации с", config.siteUrl, file = sys.stderr)

    # Страницы
    idToPage = config.startIdToPage

    # URL запроса
    apiUrl = config.siteUrl + "/w/api.php"
    extUrlRequestUrl = apiUrl + "?"
    extUrlRequestUrl += "action=query&"
    extUrlRequestUrl += "list=exturlusage&"
    extUrlRequestUrl += "format=xml&"
    extUrlRequestUrl += "eunamespace=0&"
    extUrlRequestUrl += "rawcontinue&"
    extUrlRequestUrl += "eulimit={eulimit:d}&"
    extUrlRequestUrl += "euoffset={euoffset:d}"

    euoffset = config.startEUOffset
    outputPeriodLeft = LIST_PARSING_OUTPUT_PERIOD

    if euoffset != 0 :
        print("Процесс продолжается, уже обработано", euoffset, "ссылок", file = sys.stderr)

    while True :
        # Если прервано, выйти из функции
        if interrupted :
            print("\nПроцесс обработки ссылок прерван пользователем", file = sys.stderr)
            result.idToPage = idToPage
            result.done = False
            result.euoffset = euoffset
            return

        # Запрос к MediaWiki API на получение данных
        try :
            response = urllib.request.urlopen(extUrlRequestUrl.format(eulimit = EULIMIT, euoffset = euoffset))
        except (urllib.error.URLError, ValueError) :
            print("Ошибка: не удалось получить доступ к", apiUrl, file = sys.stderr)
            result.euoffset = euoffset
            result.idToPage = idToPage
            result.done = False
            return

        # Парсинг xml
        euoffset = parseExtUrlResponse(response, idToPage)
        response.close()
        if euoffset == -1 :
            break

        # Каждые LIST_PARSING_OUTPUT_PERIOD итераций вывод в stderr количества обработанных ссылок
        outputPeriodLeft -= 1
        if outputPeriodLeft == 0 :
            outputPeriodLeft = LIST_PARSING_OUTPUT_PERIOD
            print("Обработано", euoffset, "ссылок...", file = sys.stderr)

    result.idToPage = idToPage
    result.done = True
