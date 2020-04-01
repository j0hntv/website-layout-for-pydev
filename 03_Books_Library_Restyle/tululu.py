import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


URL = 'http://tululu.org'
FOLDER_PATH = 'books/'
IMAGES_PATH = 'images/'
MAX_FILENAME_LENGHT = 50


def download_txt(url, filename, folder=FOLDER_PATH):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    if not response.status_code == 200:
        return

    path = os.path.join(folder, f'{sanitize_filename(filename)[:MAX_FILENAME_LENGHT]}.txt')

    with open(path, 'w') as file:
        file.write(response.text)
    return path

def download_image(url, filename, folder=IMAGES_PATH):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    if not response.status_code == 200:
        return

    path = os.path.join(folder, filename)

    with open(path, 'wb') as file:
        file.write(response.content)
    return path

def parse_book_info(url):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    if not response.status_code == 200:
        return

    soup = BeautifulSoup(response.text, 'lxml')
    title, author = map(str.strip, soup.select_one('h1').text.split('::'))
    book_txt_url = soup.select_one('.d_book a[title*="скачать книгу txt"]')
    book_image_url = soup.select_one('.d_book a img')
    comments = soup.select('.texts .black')
    genres = soup.select('span.d_book a')

    if book_txt_url:
        return {
            'title': title,
            'author': author,
            'book_txt_url': urljoin(URL, book_txt_url['href']),
            'book_image_url': urljoin(URL, book_image_url['src']),
            'book_image_name': book_image_url['src'].split('/')[-1],
            'comments': [comment.text for comment in comments],
            'genres': [genre.text for genre in genres]
        }
