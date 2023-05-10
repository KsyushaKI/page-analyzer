from page_analyzer import validate_funk as valid
from page_analyzer import parser
from page_analyzer import db_interaction as db
from dotenv import load_dotenv
from os import getenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
)


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
db_url = getenv('DATABASE_URL')
conn = db.db_connect(db_url)
db.make_sql_file_commands('database.sql', conn)


@app.errorhandler(404)
def not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/')
def get_main_page():
    return render_template('index.html')


@app.get('/urls')
def show_websites_list():
    websites_list = db.get_websites_lists(conn)

    return render_template('websites_list.html', websites_list=websites_list)


@app.post('/urls')
def make_websites_list():
    form_value = request.form.get("url").lower()
    url = valid.get_normalized_url(form_value)

    if not valid.is_validate_value(form_value):
        return render_template('index.html', form_value=form_value), 422

    else:
        if not valid.is_data_exists_in_db(url, conn):
            db.add_full_data_to_urls(url, conn)

        id = db.get_id_by_url_from_urls(url, conn)

        return redirect(url_for('show_website_info', id=id), code=307)


@app.route('/urls/<int:id>', methods=('GET', 'POST'))
def show_website_info(id):
    website_info = db.get_website_info(id, conn)
    all_checked_info = db.get_checked_website_info(id, conn)

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
    url_name = db.get_url_by_id_from_urls(id, conn)
    status_code = parser.get_website_status_code(url_name)

    if status_code == 200:
        content = parser.get_website_content(url_name)
        h1_tag, title_tag, meta_tag = parser.get_seo_data(content)

        db.add_full_data_to_url_checks(
            status_code,
            h1_tag,
            title_tag,
            meta_tag,
            id,
            conn
        )

    return redirect(url_for('show_website_info', id=id), code=307)
