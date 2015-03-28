# Вступительная работа в параллель P.
# HtmlWriter.py
# Модуль, предназначенный для создания веб-страницы с таблицей статей.

import sys

# ========================================================================================
# Верхняя часть страницы
htmlPageTop = """\
<title>{pageTitle}</title>
<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type">
</head>
<body>
<table border="1" cellpadding="2" cols="3">
    <tr>
        <td bgcolor="ffffaa"><b>#</b></td>
        <td bgcolor="ffffaa" width="700"><b>Статья</b></td>
        <td bgcolor="ffffaa"><b>Количество<br>ссылок</b></td>
    </tr>\
"""
# Строка таблицы
htmlPageRow = """
    <tr>
        <td>{index:d}</td>
        <td><a href="{siteUrl}/wiki/{pageName}">{pageName}</a></td>
        <td>{extLinksCount:d}</td>
    </tr>"""
# Нижняя часть страницы
htmlPageBottom = """
</table>
</body>
"""

# ========================================================================================
# createPage - функция, создающая страницу с таблицей статей.
def createPage(config, pages) :
    # Открытие файла
    print('Создание страницы', config.outputFile, file = sys.stderr)
    try :
        htmlPage = open(config.outputFile, 'w')
    except PermissionError :
        print('Ошибка: не удалось создать файл', config.outputFile, '- отказано в доступе', file = sys.stderr)
        exit(1)
    except FileNotFoundError :
        print('Ошибка: не удалось создать файл', config.outputFile, file = sys.stderr)
        exit(1)
    except IsADirectoryError :
        print('Ошибка: не удалось создать файл', config.outputFile, '- это директория', file = sys.stderr)
        exit(1)

    # Создание таблицы
    htmlPage.write(htmlPageTop.format(pageTitle = config.pageTitle))
    for i in range(len(pages)) :
        page = pages[i]
        htmlPage.write(htmlPageRow.format(index = i + 1,
                                          siteUrl = config.siteUrl,
                                          pageName = page.name,
                                          extLinksCount = page.extLinksCount))
    htmlPage.write(htmlPageBottom)

    # Конец
    htmlPage.close()
    print('Страница успешно создана', file = sys.stderr)
