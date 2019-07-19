from airtable import Airtable
from fuzzywuzzy import fuzz
from operator import itemgetter
import pickle
import os
from datetime import datetime


def matcher(x):
    table_name = 'xxx'
    base_key = 'xxx'
    airtable = Airtable(base_key, table_name, api_key='xxx')
    results = airtable.match('name', x)
    try:
        if results['fields']['type'] == 'primary':
            returner = results['fields']['name']
        elif results['fields']['type'] == 'variant':
            returner = results['fields']['use']
    except:
        returner = 'Not found'
    return returner


def searcher(y):
    ts = int(os.path.getmtime('/home/scottcarlson/api/api.pickle'))
    then = datetime.utcfromtimestamp(ts)
    now = datetime.now()
    tdelta = now - then
    if tdelta.days < 1:
        with open('/home/scottcarlson/api/api.pickle', 'rb') as f:
            results = pickle.load(f)
    else:
        table_name = 'xxx'
        base_key = 'xxx'
        airtable = Airtable(base_key, table_name, api_key='xxx')
        results = airtable.get_all()
        with open('/home/scottcarlson/api/api.pickle', 'wb') as f:
            pickle.dump(results, f)
    potential_matches = []
    for result in results:
        data = result['fields']
        fuzzy_ratio = fuzz.token_sort_ratio(y, data['name'])
        if fuzzy_ratio >= 95:
            if data['type'] == 'primary':
                potential_matches.append({'match': data['name'], 'ratio': fuzzy_ratio})
            elif data['type'] == 'variant':
                potential_matches.append({'match': data['use'], 'ratio': fuzzy_ratio})
    newlist = sorted(potential_matches, key=itemgetter('ratio'), reverse=True)
    return newlist
