import os
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


URL = 'http://tululu.org'


def download_txt(url, filename, folder='books/'):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    if response.status_code == 200:
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, f'{sanitize_filename(filename)}.txt')
        with open(path, 'w') as file:
            file.write(response.text)
        return path

def parse_book_info(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title, author = map(str.strip, soup.find('h1').text.split('::'))
    book_txt_url = soup.find('a', text='скачать txt')['href']
    print(f'Заголовок: {title}')
    print(f'Автор: {author}')
    print(f'URL: {URL}{book_txt_url}')


if __name__ == '__main__':
    parse_book_info('http://tululu.org/b1/')
