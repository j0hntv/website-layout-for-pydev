# Tululu Book Parser

Парсер книг с онлайн библиотеки [tululu.org.](http://tululu.org/)

## Установка зависимостей
```
pip3 install -r requirements.txt
```

## Запуск
```
python3 parse_tululu_category.py
```

## Параметры

 - `--start_page` - с какой страницы начинать
 - `--end_page` - на какой странице остановиться
 - `--dest_folder` - путь к каталогу с результатами парсинга: картинкам, книгами, JSON (по умолчанию - в текущую директорию)
 - `--skip_imgs` - не скачивать обложки книг
 - `--skip_txt` - не скачивать книги
 - `--json_path` - указать свой путь к *.json файлу с результатами

## Пример:
Скачаются только книги, без картинок, начиная с 700-й страницы:
```
python3 parse_tululu_category.py --start_page 700 --skip_imgs
```

## About:
Сделано в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/modules/)
