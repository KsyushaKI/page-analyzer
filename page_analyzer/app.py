from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    get_flashed_messages,
)
import os
from dotenv import load_dotenv
import psycopg2
from urllib.parse import urlparse
import validators
from datetime import date


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

with psycopg2.connect(DATABASE_URL) as conn:
    conn.autocommit = True
    with conn.cursor() as curs:
        with open('database.sql') as f:
            curs.execute(f.read())


@app.route('/', methods=('GET', 'POST'))
def get_main_page():
    if request.method == 'POST':
        get_form_value = request.form.get("url")
        get_parsed_url = urlparse(get_form_value)
        get_main_url = f"{get_parsed_url.scheme}://{get_parsed_url.netloc}"
        validate_url = validators.url(get_main_url)

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
                        flash('Страница уже существует', 'warning')
                    curs.execute(
                        'SELECT id FROM urls WHERE name=%s',
                        (get_main_url,)
                    )
                    id = curs.fetchall()[0][0]
            return redirect(url_for('get_website_info', id=id), code=307)
        else:
            flash('Некорректный URL', 'error')
            if not get_form_value:
                flash('URL обязателен', 'error')
            messages = get_flashed_messages(
                with_categories=True,
                category_filter='error'
            )
            return render_template(
                'main/index.html',
                messages=messages,
                form_value=get_form_value,
            )

    return render_template('main/index.html')


@app.route('/urls', methods=('GET', 'POST'))
def get_websites_list():
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
    return render_template('main/websites_list.html', website_info=website_info)


@app.route('/urls/<int:id>', methods=('GET', 'POST'))
def get_website_info(id):
    messages = get_flashed_messages(with_categories=True)
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            conn.autocommit = True
            curs.execute('SELECT * FROM urls WHERE id = %s', (id,))
            website_info = curs.fetchall()[0]
            curs.execute(
                'SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC',
                (id,)
            )
            all_checked_info = curs.fetchall()
    return render_template(
        'main/website_info.html',
        id=id,
        messages=messages,
        website_info=website_info,
        all_checked_info=all_checked_info,
    )


@app.post('/urls/<int:id>/checks')
def check_website(id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            conn.autocommit = True
            curs.execute(
                'INSERT INTO url_checks (id, created_at, url_id) '
                'VALUES (DEFAULT, %s, %s)',
                (date.today(), id,)
                )
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_website_info', id=id), code=307)
