

def insert_rows(rows, table_name, dbc):
    field_names = rows[0].keys()
    field_names_str = ', '.join(field_names)
    placeholder_str = ','.join('?'*len(field_names))
    insert_sql = f'INSERT INTO {table_name}({field_names_str}) VALUES ({placeholder_str})'
    saved_autocommit = dbc.autocommit
    with dbc.cursor() as cursor:
        try:
            dbc.autocommit = False
            tuples = [ tuple((row[field_name] for field_name in field_names)) for row in rows ]
            cursor.executemany(insert_sql, tuples)
            cursor.commit()
        except Exception as exc:
            cursor.rollback()
            raise exc
        finally:
            dbc.autocommit = saved_autocommit

