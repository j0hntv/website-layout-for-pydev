# Сайт онлайн-библиотеки

- [Ссылка на сайт](https://j0hntv.github.io/Website_Layout_For_Pydev/04_Books_Library_Restyle_2/pages/index1.html)

# Установка
```
git clone https://github.com/j0hntv/Website_Layout_For_Pydev.git
cd 04_Books_Library_Restyle_2/
```
## Установка зависимостей
```
pip3 install -r requirements.txt
```
## Подготовка книг
Для начала необходимо спарсить книги с онлайн библиотеки [tululu.org:](http://tululu.org/)
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
```
python3 parse_tululu_category.py --start_page 700 --dest_folder media
```
## Запуск:
Сгенерировать html-страницы и запустить сервер, с отслеживанием изменений в шаблоне `template.html`:
```
python3 render_website.py
```
Открыть в браузере:
```
http://127.0.0.1:5500/pages/index1.html
```
Если страницы готовы - просто открыть в браузере:
```
./pages/index1.html
```


# About:
Сделано в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/modules/)
