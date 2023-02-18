
def truncate_table(table_ref, dbc):
    try:
        with dbc.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {table_ref}')
            cursor.commit()
    except Exception as err:
        dbc.rollback()
        raise err
