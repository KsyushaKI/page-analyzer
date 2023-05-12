import page_analyzer.postgresql_analyzer.db_interaction as db


def is_data_exist(*data):
    sql = 'SELECT EXISTS(SELECT name FROM urls WHERE name = %s)'

    return db.get_one_value(sql, data)


def set_full(*data):
    sql = 'INSERT INTO urls VALUES (DEFAULT, %s, %s)'

    return db.set_data_to_table(sql, data)


def get_url_by_id(*data):
    sql = 'SELECT * FROM urls WHERE id = %s'

    return db.get_one_row(sql, data)


def get_id_by_name(*data):
    sql = 'SELECT id FROM urls WHERE name=%s'

    return db.get_one_value(sql, data)


def get_name_by_id(*data):
    sql = 'SELECT name FROM urls WHERE id = %s'

    return db.get_one_value(sql, data)


def joined_with_url_checks():
    sql = '''SELECT DISTINCT ON (urls.id)
                urls.id,
                urls.name,
                url_checks.created_at,
                url_checks.status_code
            FROM urls LEFT JOIN url_checks
            ON urls.id = url_checks.url_id
            ORDER BY urls.id DESC, url_checks.created_at DESC'''

    return db.get_some_rows(sql, ())
