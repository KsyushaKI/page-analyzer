from flask import flash
import validators
from urllib.parse import urlparse
from page_analyzer.db_interaction import is_data_exist


def get_normalized_url(value):
    get_parsed_url = urlparse(value)
    normalized_url = f"{get_parsed_url.scheme}://{get_parsed_url.netloc}"

    return normalized_url


def is_validate_value(value):
    response_validate = False
    if not value:
        flash('URL обязателен', 'danger')
    elif len(value) > 255:
        flash('URL превышает 255 символов', 'danger')
    elif not validators.url(value):
        flash('Некорректный URL', 'danger')
    else:
        response_validate = True

    return response_validate


def is_data_exists_in_db(url, conn):
    response = is_data_exist(url, conn)
    if not response:
        flash('Страница успешно добавлена', 'success')
    else:
        flash('Страница уже существует', 'info')
    return response
