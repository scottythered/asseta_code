import requests
import pandas as pd
import psycopg2
import datetime


def selector(cursor, command, table):
    if command == 'select_all':
        cursor.execute("SELECT * FROM {0};".format(table))
        results = cursor.fetchall()
        return results
    elif command == 'headers':
        cursor.execute("SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_NAME = '{0}';".format(table))
        results = cursor.fetchall()
        list = results
        appendable_headers = []
        for header in list:
            appendable_headers.append(header[0])
        return appendable_headers


def updated_accounts(cursor, table):
    records = selector(cursor, 'select_all', table)
    df = pd.DataFrame(records)
    headers = selector(cursor, 'headers', table)
    df.columns = headers
    df.set_index('id', inplace=True)
    df2 = df[['name', 'sfdc_id', 'last_efs_update']].dropna()
    return df2


def execute():
    try:
        conn = psycopg2.connect("dbname='xxx' user='xxx' host='xxx' port='xxx' password='xxx'")
        cur = conn.cursor()
        df = updated_accounts(cur, 'accounts')
        data_list = [{'account': row['sfdc_id'], 'name': row['name'], 'last_update': row['last_efs_update']} for index, row in df.iterrows()]
        now = datetime.date.today()
        elapsed = []
        for entry in data_list:
            delta = now - entry['last_update']
            if 89 < delta.days:
                elapsed.append(entry['name'] + ' (' + entry['account'] + ')')
            else:
                pass
        if len(elapsed) > 0:
            elapsed = '\n'.join(elapsed)
            mailgun_data = {'from': 'scotty@xxx.com', 'to': 'xxx@xxx.com', 'subject': 'EFS Accounts to Check',
                            'text': 'The following accounts haven\'t been checked in around 90 days:\n\n{0}'.format(elapsed)}
            auth = ('api', 'xxx')
            requests.post('https://api.mailgun.net/v3/mail.asseta.com/messages', data=mailgun_data, auth=auth)
        else:
            pass
    except:
        print("Unable to connect to the database")

if __name__ == "__main__":
    execute()
