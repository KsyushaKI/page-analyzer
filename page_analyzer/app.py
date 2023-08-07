from page_analyzer import validate
from page_analyzer import parser
from page_analyzer.postgresql_analyzer import urls
from page_analyzer.postgresql_analyzer import url_checks
from page_analyzer.postgresql_analyzer import db_interaction as db
from datetime import date
from dotenv import load_dotenv
from os import getenv
from flask import (
    Flask,
    flash,
    render_template,
    request,
    redirect,
    url_for,
)


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')

db.create_project_tables()


@app.errorhandler(404)
def not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/')
def get_main_page():
    return render_template('index.html')


@app.get('/urls')
def show_websites_list():
    websites_list = urls.joined_with_url_checks()

    return render_template('websites_list.html', websites_list=websites_list)


@app.post('/urls')
def make_websites_list():
    form_value = request.form.get("url").lower()
    url = validate.get_normalized_url(form_value)

    if not validate.is_validate_value(form_value):
        return render_template('index.html', form_value=form_value), 422

    else:
        if not validate.is_data_exists_in_db(url):
            urls.set_full(url, date.today())
        id = urls.get_id_by_name(url)

        return redirect(url_for('show_website_info', id=id), code=307)


@app.route('/urls/<int:id>', methods=('GET', 'POST'))
def show_website_info(id):
    website_info = urls.get_url_by_id(id)
    all_checked_info = url_checks.get_info_by_url_id(id)

    if not website_info:
        return render_template('page_not_found.html'), 404

    return render_template(
        'website_info.html',
        id=id,
        website_info=website_info,
        all_checked_info=all_checked_info,
    )


@app.post('/urls/<int:id>/checks')
def check_website(id):
    url_name = urls.get_name_by_id(id)
    status_code = parser.get_website_status_code(url_name)

    if status_code == 200:
        content = parser.get_website_content(url_name)
        h1_tag, title_tag, meta_tag = parser.get_seo_data(content)
        url_checks.set_full(
            status_code,
            h1_tag,
            title_tag,
            meta_tag,
            date.today(),
            id,
        )
        flash('Страница успешно проверена', 'success')
    else:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for('show_website_info', id=id), code=307)
