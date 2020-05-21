import json
import os
from glob import glob
from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked
from livereload import Server
from urllib.parse import quote


def get_books_description():
    with open('media/description.json') as file:
        books_description = json.load(file)
    return books_description


def remove_old_pages():
    pages = glob('pages/*.html')
    for page in pages:
        os.remove(page)


def render_pages():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    books_description = get_books_description()
    chunked_books_description = chunked(books_description, 2)
    chunked_pages = list(chunked(chunked_books_description, 10))
    total_pages = len(chunked_pages)

    for index, chunked_page in enumerate(chunked_pages, start=1):
        rendered_page = template.render(
            books_description=chunked_page,
            quote=quote,
            total_pages=total_pages,
            current_page=index
        )
        with open(f'pages/index{index}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    os.makedirs('pages', exist_ok=True)
    remove_old_pages()
    server = Server()
    render_pages()
    server.watch('template.html', render_pages)
    server.serve(root='.')


if __name__ == "__main__":
    main()
