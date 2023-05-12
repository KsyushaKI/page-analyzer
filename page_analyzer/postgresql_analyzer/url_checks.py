import page_analyzer.postgresql_analyzer.db_interaction as db


def set_full(*data):
    sql = '''INSERT INTO url_checks (
                id,
                status_code,
                h1, title,
                description,
                created_at,
                url_id
            )
            VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)'''

    return db.set_data_to_table(sql, data)


def get_info_by_url_id(*data):
    sql = '''SELECT
                id,
                status_code,
                h1,
                title,
                description,
                created_at
            FROM url_checks WHERE url_id = %s
            ORDER BY id DESC'''

    return db.get_some_rows(sql, data)
