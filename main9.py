# Парсинг в несколько потоков
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import csv
from multiprocessing import Pool # бассейн для общего объема задач, к-рые надо выполнить.
from time import sleep



# def get_html(url) :
#
#     session = requests.Session()
#     retry = Retry(connect=3, backoff_factor=0.5)
#     adapter = HTTPAdapter(max_retries=retry)
#     session.mount('http://', adapter)
#     session.mount('https://', adapter)
#
#     #r = requests.get(url)
#     r = session.get(url)
#     return r.text

def get_html(url) :
    sleep(1)
    r = requests.get(url)
    return r.text

# def get_html(url) :
#     sleep(1)
#     page = ''
#     while page == '' :
#         try :
#             page = requests.get(url)
#             break
#         except :
#             print("Connection refused by the server..")
#             print("Let me sleep for 5 seconds")
#             sleep(5)
#             continue
#     return page.text



def write_csv(data) :
    with open('websites.csv', 'a', newline='', encoding='utf-8') as f :
        order = ['name','url','description','traffic','percent','stata']
        writer = csv.DictWriter(f, fieldnames=order,delimiter='|')
        writer.writerow(data)

def get_page_data(text) :
    # взяли строку , strip()-убрали лишние пробелы \n\t,
    # split()-разбили строку в список,[1:] убрали нулевой элемент, т.к. он нам не нужен
        data = text.strip().split('\n')[1:]
    #  будем брать строки из списка data в row
        for row in data :
            # каждая строка row разделена \t на элементы
            #разобъем эту строку по спискам.
            columns = row.strip().split('\t')
            name = columns[0]
            url = columns[1]
            description = columns[2]
            traffic = columns[3]
            percent = columns[4] # процент трафика из выбранного региона
            stata = columns[5] # private - статистика закрыта, public - статистика открыта
            # пакуем в словарь.
            dicdata = {'name': name,
                    'url': url,
                    'description': description,
                    'traffic': traffic,
                    'percent': percent,
                    'stata': stata}
            # пишем в csv-файл
            write_csv(dicdata)

def make_all(url) :
    text = get_html(url)
    get_page_data(text)


def main() :
    #for i in range(0,6000) :
    #     url = 'https://www.liveinternet.ru/rating/ru//today.tsv?page={}'.format(str(i))
    #     response = get_html(url)

    # в python ф-я map на вход этой ф-и подается какая-либо функция и список
    # map(function, list)
    # ф-я map берет из списка последовательно каждый элемент и передает его
    # в функцию. внутри map есть встроенный цикл, который перебирает все элементы
    # списка и передает в качестве аргумента функции(function)
    # и теперь нам надо предоставить для map функцию для обработки и список с данными
    url = 'https://www.liveinternet.ru/rating/ru//today.tsv?page={}'
    #воспользуемся генератором списков
    urls = [url.format(str(i)) for i in range(1,8000)] # страницы на сайте нумеруются с 1

# в 20 потоков будем обрабатывать пул урлов
    with Pool(12) as p :
        # в классе Pool есть встроенный метод map
        #и в нем есть встроенный цикл, Который проходит по всем элементам списка.
        p.map(make_all, urls)



if __name__ == "__main__" :
    main()
