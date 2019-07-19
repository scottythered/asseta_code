from airtable import Airtable
import pickle


def splitter(thesaurus_object):
    api_json = []
    for entry in thesaurus_object:
        api_json.append(entry['fields'])
    for entry in api_json:
        try:
            if '; ' in entry['variant_name_form']:
                entry['variant_name_form'] = entry['variant_name_form'].split('; ')
        except KeyError:
            pass
    return api_json


def grabber():
    table_name = 'xxx'
    base_key = 'xxx'
    airtable = Airtable(base_key, table_name, api_key='xxx')
    thesaurus = airtable.get_all(sort='primary_name_form')
    split_thesaurus = splitter(thesaurus)
    api_format_thes = []
    for item in split_thesaurus:
        api_format_thes.append({'name': item['primary_name_form'],
                                'type': 'primary'})
        try:
            if item['variant_name_form'] != '':
                if isinstance(item['variant_name_form'], (list,)):
                    for thing in item['variant_name_form']:
                        api_format_thes.append({'name': thing,
                                                'type': 'variant',
                                                'use': item['primary_name_form']})
                else:
                    api_format_thes.append({'name': item['variant_name_form'],
                                            'type': 'variant',
                                            'use': item['primary_name_form']})
            else:
                pass
        except:
            pass
    with open('make_api.pickle', 'rb') as f:
        pickled_data = pickle.load(f)
    parsed_pickle = []
    for thing in pickled_data:
        parsed_pickle.append(thing['fields'])
    difference = [x for x in api_format_thes if x not in parsed_pickle]
    if len(difference) > 0:
        print(f"{len(difference)} records need to be added")
        return difference
    else:
        print('No update needed')


def diagnostics(list_to_check):
    primaries = []
    for item in list_to_check:
        primaries.append(item['primary_name_form'])
    for name_form in primaries:
        for entry in list_to_check:
            try:
                if isinstance(entry['variant_name_form'], (list,)):
                    for subentry in entry['variant_name_form']:
                        if subentry != '':
                            if name_form == subentry:
                                print(f"{name_form} is found in the variantforms of {entry['primary_name_form']}")
                else:
                    if name_form == entry['variant_name_form']:
                        print(f"{name_form} is the variantform of {entry['primary_name_form']}")
            except:
                pass
    for entry in list_to_check:
        try:
            if isinstance(entry['variant_name_form'], (list,)):
                for subentry in entry['variant_name_form']:
                    if subentry == entry['primary_name_form']:
                        print(f"{subentry} is found in the variantforms of {entry['primary_name_form']}")
            else:
                if entry['primary_name_form'] == entry['variant_name_form']:
                    print(f"{entry['variant_name_form']} the variantform of {entry['primary_name_form']}")
        except:
            pass


def puncher(y):
    table_name = 'xxx'
    base_key = 'xxx'
    airtable = Airtable(base_key, table_name, api_key='xxx')
    results = airtable.batch_insert(y)
    new_thesaurus = airtable.get_all()
    with open('make_api.pickle', 'wb') as f:
        pickle.dump(new_thesaurus, f)
    return results
