import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from tululu import download_image, download_txt, parse_book_info
from time import monotonic

CATEGORY_URL = 'http://tululu.org/l55/'
FOLDER_PATH = 'books/'
IMAGES_PATH = 'images/'

def get_total_pages(url=CATEGORY_URL):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    end_page = soup.find_all('a', class_='npage')[-1].text
    return int(end_page)

def get_book_links(url=CATEGORY_URL, total_pages=1):
    if not total_pages:
        total_pages = get_total_pages()

    for page_number in range(1, total_pages + 1):
        page_url = urljoin(url, str(page_number))
        response = requests.get(page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        book_categories = soup.find_all('table', class_='d_book')
        
        for book_category in book_categories:
            div = book_category.find('div', class_='bookimage').find('a')
            yield urljoin(url, div['href'])


def main():
    os.makedirs(FOLDER_PATH, exist_ok=True)
    os.makedirs(IMAGES_PATH, exist_ok=True)

    book_links = get_book_links()

    time = monotonic()

    for book_link in book_links:
        book_info = parse_book_info(book_link)
        if not book_info:
            continue
        filename = f'{book_info["title"]}'
        imagename = book_info['book_image_name']

        txt_url = book_info['book_txt_url']
        image_url = book_info['book_image_url']

        download_txt(txt_url, filename)
        download_image(image_url, imagename)

    print(f'Done in {monotonic() - time:.2f} sec.')


if __name__ == '__main__':
    main()

