import pandas as pd


def selector(cursor, command, table):
    if command == 'select_all':
        cursor.execute("SELECT * FROM {0};".format(table))
        results = cursor.fetchall()
        return results
    elif command == 'headers':
        cursor.execute("SELECT COLUMN_NAME FROM information_schema.COLUMNS ",
                       "WHERE TABLE_NAME = '{0}';".format(table))
        results = cursor.fetchall()
        list = results
        appendable_headers = [header[0] for header in list]
        return appendable_headers


def get_all_data(cursor, table):
    records = selector(cursor, 'select_all', table)
    df = pd.DataFrame(records)
    headers = selector(cursor, 'headers', table)
    df.columns = headers
    df.set_index('id', inplace=True)
    return df


def active_listings(cursor, account):
    if account != 'all':
        cursor.execute("SELECT * FROM equipment_listings where account_id ",
                       "= {0} and quantity > 0;".format(account))
        records = cursor.fetchall()
        df = pd.DataFrame(records)
        try:
            headers = selector(cursor, 'headers', 'equipment_listings')
            df.columns = headers
            print(len(df))
            return df
        except ValueError:
            print('No records')
    else:
        cursor.execute("SELECT * FROM equipment_listings where quantity > 0;")
        records = cursor.fetchall()
        df = pd.DataFrame(records)
        try:
            headers = selector(cursor, 'headers', 'equipment_listings')
            df.columns = headers
            print(len(df))
            return df
        except ValueError:
            print('No records')
