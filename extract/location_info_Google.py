import re

from uszipcode import SearchEngine as ZipcodeSearchEngine

from extract.utils import state_abbrev as states


def get_re_for_location_parsing():
    states_or = '|'.join(states.keys())
    return r"({states_or})".format(**locals()) + r" (\d{5})"

def find_possible_locations(s):
    q = get_re_for_location_parsing()
    return list(set(re.findall(q, s)))

def extract_location(s):
    z_search = ZipcodeSearchEngine()
    possible_locations = find_possible_locations(s)
    keys = ['State', 'City', 'Zipcode']
    for state, zipcode in possible_locations:
        zip_info = z_search.by_zipcode(zipcode)
        if states[state] == zip_info.state:
            d = {key: getattr(zip_info, key.lower()) for key in keys}
            d["Confidence_location"] = "high"
            return d
    if possible_locations != []:
        return {'State': possible_locations[0][0],
                'City': None,
                'Zipcode': possible_locations[0][1],
                'Confidence_location': "low"}
    else:
#        return {'State': None,
#                'City': None,
#                'Zipcode': None,
#                'Confidence_location': None}
        return None

if __name__ == "__main__":
    ss = [
        'washington 98102',
        'massachusetts 02138',
        'texas 10983', # uszipcode fails as zip does not match state
    ]
    for s in ss:
        print('\n' + s)
        print(extract_location(s))
