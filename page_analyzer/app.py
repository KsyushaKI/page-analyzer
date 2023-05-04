from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
)
import os
from dotenv import load_dotenv
import psycopg2
from urllib.parse import urlparse
import validators
from datetime import date
import requests
from bs4 import BeautifulSoup


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

with psycopg2.connect(DATABASE_URL) as conn:
    conn.autocommit = True
    with conn.cursor() as curs:
        with open('database.sql') as f:
            curs.execute(f.read())


@app.route('/')
def get_main_page():
    return render_template('index.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/urls', methods=('GET', 'POST'))
def get_websites_list():
    if request.method == 'POST':
        get_form_value = request.form.get("url").lower()
        get_parsed_url = urlparse(get_form_value)
        get_main_url = f"{get_parsed_url.scheme}://{get_parsed_url.netloc}"
        validate_url = validators.url(get_main_url)
        if len(get_form_value) > 255:
            flash('URL превышает 255 символов', 'danger')
            return render_template(
                'index.html',
                form_value=get_form_value,
            ), 422

        if validate_url:
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor() as curs:
                    conn.autocommit = True
                    curs.execute(
                        'SELECT EXISTS(SELECT name FROM urls WHERE name = %s)',
                        (get_main_url,)
                    )
                    data_exists = curs.fetchone()[0]
                    if not data_exists:
                        curs.execute(
                            'INSERT INTO urls VALUES (DEFAULT, %s, %s)',
                            (get_main_url, date.today())
                        )
                        flash('Страница успешно добавлена', 'success')
                    else:
                        flash('Страница уже существует', 'info')
                    curs.execute(
                        'SELECT id FROM urls WHERE name=%s',
                        (get_main_url,)
                    )
                    id = curs.fetchall()[0][0]
            return redirect(url_for('get_website_info', id=id), code=307)
        else:
            flash('Некорректный URL', 'danger')
            if not get_form_value:
                flash('URL обязателен', 'danger')
            return render_template(
                'index.html',
                form_value=get_form_value,
            ), 422

    if request.method == 'GET':
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as curs:
                conn.autocommit = True
                curs.execute(
                    'SELECT urls.id, urls.name, '
                    'MAX(url_checks.created_at), url_checks.status_code '
                    'FROM urls LEFT JOIN url_checks '
                    'ON urls.id = url_checks.url_id '
                    'GROUP BY urls.id, url_checks.status_code '
                    'ORDER BY urls.id DESC'
                )
                website_info = curs.fetchall()
    return render_template('websites_list.html', website_info=website_info)


@app.route('/urls/<int:id>', methods=('GET', 'POST'))
def get_website_info(id):
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as curs:
                conn.autocommit = True
                curs.execute('SELECT * FROM urls WHERE id = %s', (id,))
                website_info = curs.fetchall()[0]
                curs.execute(
                    'SELECT id, status_code, h1, title, description, created_at '
                    'FROM url_checks WHERE url_id = %s '
                    'ORDER BY id DESC',
                    (id,)
                )
                all_checked_info = curs.fetchall()
        return render_template(
            'website_info.html',
            id=id,
            website_info=website_info,
            all_checked_info=all_checked_info,
        )
    except IndexError:
        return render_template('page_not_found.html'), 404


@app.post('/urls/<int:id>/checks')
def check_website(id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            conn.autocommit = True
            curs.execute(
                'SELECT name FROM urls WHERE id = %s',
                (id,)
            )
            url_name = curs.fetchall()[0][0]
            code = {'code': ''}
            try:
                r = requests.get(url_name, timeout=1.0)
                code['code'] = r.status_code
            except requests.exceptions.RequestException as error:
                app.logger.warning(error)

            if code['code'] == 200:
                content = r.text
                soup = BeautifulSoup(content, 'html.parser')
                h1_tag = soup.find('h1')
                title_tag = soup.find('title')
                meta_tag = soup.find('meta', attrs={"name": "description"})
                if h1_tag:
                    h1_tag = soup.find('h1').getText()
                if title_tag:
                    title_tag = soup.find('title').getText()
                if meta_tag:
                    meta_tag = meta_tag.get("content")
                curs.execute(
                    'INSERT INTO url_checks '
                    '(id, status_code, h1, title, '
                    'description, created_at, url_id) '
                    'VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)', (
                        r.status_code,
                        h1_tag,
                        title_tag, meta_tag,
                        date.today(),
                        id
                    )
                )
                flash('Страница успешно проверена', 'success')
            else:
                flash('Произошла ошибка при проверке', 'danger')
    return redirect(url_for('get_website_info', id=id), code=307)
