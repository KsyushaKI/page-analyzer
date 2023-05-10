from psycopg2 import connect
from datetime import date


def db_connect(db_url):
    with connect(db_url) as conn:
        conn.autocommit = True

        return conn


def make_sql_file_commands(file_path, conn):
    with conn.cursor() as curs:
        with open(file_path) as f:
            curs.execute(f.read())


def is_data_exist(data, conn):
    sql = 'SELECT EXISTS(SELECT name FROM urls WHERE name = %s)'
    with conn.cursor() as curs:
        curs.execute(sql, (data,))
        data_exists = curs.fetchone()[0]

        return data_exists


def add_full_data_to_urls(data, conn):
    sql = 'INSERT INTO urls VALUES (DEFAULT, %s, %s)'
    with conn.cursor() as curs:
        curs.execute(sql, (data, date.today()))


def get_id_by_url_from_urls(url, conn):
    sql = 'SELECT id FROM urls WHERE name=%s'
    with conn.cursor() as curs:
        curs.execute(sql, (url,))
        id = curs.fetchone()[0]

        return id


def get_websites_lists(conn):
    sql = '''
            SELECT DISTINCT ON (urls.id)
                urls.id,
                urls.name,
                url_checks.created_at,
                url_checks.status_code
            FROM urls LEFT JOIN url_checks
            ON urls.id = url_checks.url_id
            ORDER BY urls.id DESC, url_checks.created_at DESC
        '''
    with conn.cursor() as curs:
        curs.execute(sql)
        websites_list = curs.fetchall()

        return websites_list


def get_website_info(id, conn):
    sql = 'SELECT * FROM urls WHERE id = %s'
    with conn.cursor() as curs:
        curs.execute(sql, (id,))
        website_info = curs.fetchone()

        return website_info


def get_checked_website_info(id, conn):
    sql = '''
        SELECT
            id,
            status_code,
            h1,
            title,
            description,
            created_at
        FROM url_checks WHERE url_id = %s
        ORDER BY id DESC
        '''
    with conn.cursor() as curs:
        curs.execute(sql, (id,))
        checked_website_info = curs.fetchall()

        return checked_website_info


def get_url_by_id_from_urls(id, conn):
    sql = 'SELECT name FROM urls WHERE id = %s'
    with conn.cursor() as curs:
        conn.autocommit = True
        curs.execute(sql, (id,))
        url_name = curs.fetchone()[0]

        return url_name


def add_full_data_to_url_checks(
        status_code,
        h1_tag,
        title_tag,
        meta_tag,
        id,
        conn,
        ):

    sql = '''
        INSERT INTO url_checks (
            id,
            status_code,
            h1, title,
            description,
            created_at,
            url_id
            )
        VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)
        '''
    values = status_code, h1_tag, title_tag, meta_tag, date.today(), id

    with conn.cursor() as curs:
        curs.execute(sql, (values))
