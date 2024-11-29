import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time

rating_map = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
}

# Функция для сбора данных о книгах с одной страницы
def get_book_data(book_url):
    response = requests.get(book_url)
    page_book = BeautifulSoup(response.text, 'html.parser')
    block_book = page_book.find('div', class_='product_main')
    name = block_book.find('h1').text
    
    rating_tag = block_book.find('p', class_='star-rating')
    rating_class = rating_tag['class']
    if len(rating_class) > 1:
        rating_word = rating_class[1]  # Извлекаем слово рейтинга (One, Two, Three и т.д.)
        rating = rating_map.get(rating_word, 0)  # По умолчанию 0, если слово не распознано
    else:
        rating = 0  # На случай, если класса нет


    table = page_book.find('table', class_='table table-striped')

    # Словарь для данных текущей книги
    book_info = {
        'Название книги': name,
        'Оценка': rating
    }

    if table:
        rows = table.find_all('tr')  # Ищем все строки таблицы
        for row in rows:
            th = row.find('th').text.strip()  # Заголовок
            td = row.find('td').text.strip()  # Значение
            book_info[th] = td

    description_div = page_book.find('div', id='product_description')

    # Ищем следующий тег <p> после найденного <div>
    if description_div:
        description_p = description_div.find_next('p').text.strip()  # Извлекаем текст
        book_info['Описание'] = description_p
    else:
        print("Описание не найдено")
    
    return book_info


# Функция для сбора данных с всех страниц каталога
def scrape_books_data(count_page = 0):
    base_url = 'https://books.toscrape.com/catalogue/page-{}.html'
    books_data = []
    
    page_number = 1
    while True:
        url = base_url.format(page_number)
        response = requests.get(url)
        page = BeautifulSoup(response.text, 'html.parser')
        
        block_of_books = page.find('ol', class_='row')
        if not block_of_books:
            break
        
        book_links = block_of_books.find_all('h3')
        for book_link in book_links:
            book_url = 'https://books.toscrape.com/catalogue/' + book_link.find('a').get('href', '')
            print(book_url)
            book_info = get_book_data(book_url)
            books_data.append(book_info)
        
        if page_number == count_page:
            break
        page_number += 1
    
    # Преобразуем данные в DataFrame
    books_df = pd.DataFrame(books_data)
    
    # Предобработка данных
    books_df.fillna('Нет данных', inplace=True)  # Заполняем пропуски
    books_df.drop_duplicates(inplace=True)  # Удаляем дубликаты
    
    # Сохраняем данные в CSV файл
    books_df.to_csv('books_data.csv', mode='a', index=False, encoding='utf-8', header=False)
    
    # Печать первых строк для проверки
    print(books_df.head())


# Функция для запуска скрипта по расписанию
def job():
    print("Начинаю сбор данных о книгах...")
    scrape_books_data() #можно указать число чтобы не парсить все страницы
    print("Данные собраны и сохранены.")

# Автоматизация с использованием библиотеки schedule
schedule.every().day.at("19:00").do(job)


# Бесконечный цикл для ожидания времени запуска
while True:
    schedule.run_pending()
    time.sleep(60)  # Проверка каждую минуту
