import os
import re
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


URL = 'http://tululu.org'
FOLDER = 'books/'


def download_txt(url, filename, folder=FOLDER):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    if not response.status_code == 200:
        return

    path = os.path.join(folder, f'{sanitize_filename(filename)}.txt')

    with open(path, 'w') as file:
        file.write(response.text)
    return path

def parse_book_info(url):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    if not response.status_code == 200:
        return

    soup = BeautifulSoup(response.text, 'lxml')
    title, author = map(str.strip, soup.find('h1').text.split('::'))
    book_txt_url = soup.find('a', text='скачать txt')
    # book_image_url = soup.find('img', alt=re.compile(f'.*{title}*'))

    if book_txt_url:
        return {
            'title': title,
            'author': author,
            'book_txt_url': URL + book_txt_url['href'],
            # 'book_image_url': URL + book_image_url['src']
        }


if __name__ == '__main__':
    os.makedirs(FOLDER, exist_ok=True)

    for i in range(1, 101):
        book_url = f'{URL}/b{i}/'
        book_info = parse_book_info(book_url)
        if not book_info:
            continue
        filename = f'{i}. {book_info["title"]}'
        url = book_info['book_txt_url']
        download_txt(url, filename)
        print(filename)
    
    print('[*] Done.')
