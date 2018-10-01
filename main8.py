# как парсить сайты, которые используют AJAX
# асинхронный JavaScript и XML
# вся работа с AJAX сводится обычно к парсингу ответа сервера
# а перед этим надо узнать куда слать запрос (ссылка)
# какой слать запрос GET , PUT или что-то еще
# а также параметры запроса.
# в случае с www.liveinternet.ru JavaScript обрабатывать не придется.
import requests
import csv


def get_html(url) :
    r = requests.get(url)
    return r.text

def write_csv(data) :
    with open('websites.csv', 'a', newline='', encoding='utf-8') as f :
        order = ['name','url','description','traffic','percent','stata']
        writer = csv.DictWriter(f, fieldnames=order,delimiter='|')
        writer.writerow(data)


def main() :
    for i in range(0,6000) :
        url = 'https://www.liveinternet.ru/rating/ru//today.tsv?page={}'.format(str(i))
        response = get_html(url)
    # взяли строку response, strip()-убрали лишние пробелы \n\t,
    # split()-разбили строку в список,[1:] убрали нулевой элемент, т.к. он нам не нужен
        data = response.strip().split('\n')[1:]
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



if __name__ == "__main__" :
    main()
