from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/parse', methods=['POST'])
def parse():
    search_data = request.form['searchdata']
    url = f'https://www.moypolk.ru/search?s={search_data}'
    response = requests.get(url)
# Используем BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Находим все карточки
    cards = soup.find_all('div', class_='search-card__wrap')
    
    # Список для хранения информации о продуктах
    products = []
    
    # Перебираем найденные карточки и извлекаем информацию
    for card in cards:
        # Находим и выводим ФИО
        fio = card.find('a', class_='search-card__caption').text.strip()

        # Находим и выводим Звание, если есть
        rank_element = card.find('span', string=lambda x: x and 'аскердик наам' in x)
        rank = rank_element.text.split(' - ')[-1].strip() if rank_element else 'аскердик наамы жазылуу эмес'

        # Выводим ссылку
        link = card.find('a', class_='search-card__caption')['href']
        
        # Добавляем информацию о продукте в список
        products.append({"fio": fio, "rank": rank, "link": link})
    return render_template('products.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)