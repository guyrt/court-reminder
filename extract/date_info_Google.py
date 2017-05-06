
import calendar
from collections import OrderedDict
import dateutil.parser as dparser
from datetime import datetime
import re

from extract.utils import years_to_digits, ordinals_to_ordinals, hour_with_min_to_time, wordnums_to_nums, replace_homonyms


#not used by Google
def create_digits_for_date_parsing(s):
    """ Examples:
    'april thirteenth two thousand sixteen at two thirty PM'
    -> 'april 13th, 2016 at 2:30 PM'

    'april thirteen two thousand sixteen at two thirty PM'
    -> 'april 13, 2016, at 2:30 PM'

    'april thirteenth two thousand and sixteen at two thirty PM'
    -> 'april 13th, 2016 at 2:30 PM'

    'april thirteenth two thousand sixteen at two PM'
    -> 'april 13th, 2016, at 2 PM'

    'april two thousand sixteen at two thirty PM'
    -> 'april, 2016 at 2:30 PM'
    """
    # order important
    s = years_to_digits(s)
    s = ordinals_to_ordinals(s)
    s = hour_with_min_to_time(s)
    s = wordnums_to_nums(s)
    return s


def get_re_for_date_parsing():
    """ 
    Basically matches strings beginning with a month, and ending in AM or PM
    In between the month and AM/PM, matching is non-greedy.
    Uses lookahead with grouping to find overlapping matches.
    Example:
    s = '31 may st new york new york on april 3rd, 2017 at 1:30 p.m.'
    The re will catch both:
        'may st new york new york on april 3rd, 2017 at 1:30 p.m.'
    and
        'april 3rd, 2017 at 1:30 p.m.'
    """
    months = list(map(lambda x: x.lower(), list(calendar.month_name)[1:])) # py 3
    months_or = '|'.join(months)
    return r"(?=((?:{months_or}) .*? (?:a\.m\.|p\.m\.)))".format(**locals())


def find_possible_date_times(s, words_to_nums):
    """ Example:
    s = 'blah blah thirty one may st new york new york on april third, 
         two thousand seventeen at one thirty PM blah blah'
    returns
    list('april 3rd, 2017 at 1:30 p.m.',
         'may st new york new york on april 3rd, 2017 at 1:30 PM')

    The returned list is ordered by length.
    Duplicates are removed.
    """
    if words_to_nums:
        s = create_digits_for_date_parsing(s)
    s = s.lower()
    q = get_re_for_date_parsing()
    ret = list(set(re.findall(q, s)))
    ret.sort(key=len)
    return ret


def extract_date_time_base(s, words_to_nums=False):
    """ Example:
    s = 'blah blah thirty one may st new york new york on april third, 
         two thousand seventeen at one thirty PM blah blah'
    returns
    dict('year': 2017,
         'month': 4,
         'day': 3,
         'hour': 13,
         'minute': 30)
    
    minute default to 0 if none found.
    All other keys default to None.

    Loops through possible dates, returns as soon as dparser succeeds in 
    parsing date.
    """
    possible_dates = find_possible_date_times(s, words_to_nums)
    default_1 = datetime(1900, 1, 1, 0, 0)
    default_2 = datetime(1999, 12, 25, 23, 0)
    fields = ['year', 'month', 'day', 'hour', 'minute']
    d = OrderedDict()
    for field in fields:
        d[field] = None
    for date in possible_dates:
        try:
            dt_1 = dparser.parse(date, default=default_1)
            dt_2 = dparser.parse(date, default=default_2)
            #populate dictionary with date info
            different = 0 #flags if dt_1 different than dt_2
            for key in d:
                if dt_1.__getattribute__(key) == dt_2.__getattribute__(key):
                    d[key] = dt_1.__getattribute__(key)
                else:
                	different = 1
            d["minute"] = dt_1.minute

            if not different: #  if dt_1 == dt_2, create datetime column
            	d["datetime"] = dt_1
            return d
        except:
            pass
    return None


def extract_date_time(s):
    """ If extract_date_time_base doesn't succeed, try again having replaced
    homonyms.
    """
#    return (extract_date_time_base(s) or
#            extract_date_time_base(replace_homonyms(s), words_to_nums=True) or
#            {'year': None, 'month': None, 'day': None,
#             'hour': None, 'minute': None})
    return (extract_date_time_base(s) or
            extract_date_time_base(replace_homonyms(s), words_to_nums=True) or
            None)
    

if __name__ == "__main__":
    ss = [
        'your next Master hearing date January 19th 2018 at 3 p.m. for Gymboree',
        'twenty third street january seventh at ate a.m.',
        'march avenue february two thousand and twenty at nine a.m.',
        ('judge may smith at address involving march and 23rd st '
         'on May 10th 2018 at 3 p.m.'),
    ]
    for s in ss:
        print('\n' + s)
        print(extract_date_time(s))
