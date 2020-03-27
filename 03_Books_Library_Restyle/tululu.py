import os
import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


URL = 'http://tululu.org'
FOLDER_PATH = 'books/'
IMAGES_PATH = 'images/'


def download_txt(url, filename, folder=FOLDER_PATH):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    if not response.status_code == 200:
        return

    path = os.path.join(folder, f'{sanitize_filename(filename)}.txt')

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
    title, author = map(str.strip, soup.find('h1').text.split('::'))
    book_txt_url = soup.find('a', text='скачать txt')
    book_image_url = soup.find('div', class_='bookimage').find('img')
    comments = soup.find_all('div', class_='texts')
    genres = soup.find('span', class_='d_book').find_all('a')

    if book_txt_url:
        return {
            'title': title,
            'author': author,
            'book_txt_url': urljoin(URL, book_txt_url['href']),
            'book_image_url': urljoin(URL, book_image_url['src']),
            'book_image_name': book_image_url['src'].split('/')[-1],
            'comments': [comment.find('span', class_='black').text for comment in comments],
            'genres': [genre.text for genre in genres]
        }

def main():
    os.makedirs(FOLDER_PATH, exist_ok=True)
    os.makedirs(IMAGES_PATH, exist_ok=True)

    for i in range(9, 10):
        book_url = urljoin(URL, f'b{i}/')
        book_info = parse_book_info(book_url)
        if not book_info:
            continue
        filename = f'{i}. {book_info["title"]}'
        imagename = book_info['book_image_name']

        txt_url = book_info['book_txt_url']
        image_url = book_info['book_image_url']

        download_txt(txt_url, filename)
        download_image(image_url, imagename)
        print(filename)
        print(image_url)
        print(book_info['genres'])
        print(book_info['comments'])
    
    print('[*] Done.')


if __name__ == '__main__':
    main()
