import re

from uszipcode import ZipcodeSearchEngine

import utils


def create_digits_for_location_parsing(s):
    s = utils.wordnums_to_nums(s)
    s = re.sub(r'(\d)\s+(\d)\s+(\d)\s+(\d)\s+(\d)',r'\1\2\3\4\5', s)
    return s

def get_re_for_location_parsing():
    states_or = '|'.join(utils.states.keys())
    return r"({states_or})".format(**locals()) + r" (\d{5})"

def find_possible_locations(s):
    s = create_digits_for_location_parsing(s)
    q = get_re_for_location_parsing()
    return list(set(re.findall(q, s)))

def extract_location(s):
    states = utils.states
    z_search = ZipcodeSearchEngine()
    possible_locations = find_possible_locations(s)
    keys = ['State', 'City', 'Zipcode']
    for state, zipcode in possible_locations:
        zip_info = z_search.by_zipcode(zipcode)
        if states[state] == zip_info['State']:
            return {key: zip_info[key] for key in keys}
    return {'State': None,
            'City': None,
            'Zipcode': None}

if __name__ == "__main__":
    ss = [
        'washington nine eight one zero two',
        'massachusetts zero two one three eight',
        'texas seven five two four two', # uszipcode fails
    ]
    for s in ss:
        print('\n' + s)
        print(extract_location(s))
    
