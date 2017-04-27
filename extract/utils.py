from collections import OrderedDict

year_vals = OrderedDict()
year_vals["two thousand sixteen"] = "2016"
year_vals["two thousand seventeen"] = "2017"
year_vals["two thousand eighteen"] = "2018"
year_vals["two thousand nineteen"] = "2019"
year_vals["two thousand twenty one"] = "2021"
year_vals["two thousand twenty two"] = "2022"
year_vals["two thousand twenty three"] = "2023"
year_vals["two thousand twenty four"] = "2024"
year_vals["two thousand twenty five"] = "2025"
year_vals["two thousand twenty six"] = "2026"
year_vals["two thousand twenty seven"] = "2027"
year_vals["two thousand twenty eight"] = "2028"
year_vals["two thousand twenty nine"] = "2029"
year_vals["two thousand twenty"] = "2020"
year_vals["two thousand thirty"] = "2030"
year_vals["two thousand and sixteen"] = "2016"
year_vals["two thousand and seventeen"] = "2017"
year_vals["two thousand and eighteen"] = "2018"
year_vals["two thousand and nineteen"] = "2019"
year_vals["two thousand and twenty one"] = "2021"
year_vals["two thousand and twenty two"] = "2022"
year_vals["two thousand and twenty three"] = "2023"
year_vals["two thousand and twenty four"] = "2024"
year_vals["two thousand and twenty five"] = "2025"
year_vals["two thousand and twenty six"] = "2026"
year_vals["two thousand and twenty seven"] = "2027"
year_vals["two thousand and twenty eight"] = "2028"
year_vals["two thousand and twenty nine"] = "2029"
year_vals["two thousand and twenty"] = "2020"
year_vals["two thousand and thirty"] = "2030"

ordinals = OrderedDict()
ordinals['thirty first'] = '31st'
ordinals['thirtieth'] = '30th'
ordinals['twenty ninth'] = '29th'
ordinals['twenty eigth'] = '28th'
ordinals['twenty seventh'] = '27th'
ordinals['twenty sixth'] = '26th'
ordinals['twenty fifth'] = '25th'
ordinals['twenty fourth'] = '24th'
ordinals['twenty third'] = '23rd'
ordinals['twenty second'] = '22nd'
ordinals['twenty first'] = '21st'
ordinals['twentieth'] = '20th'
ordinals['nineteenth'] = '19th'
ordinals['eighteenth'] = '18th'
ordinals['seventeenth'] = '17th'
ordinals['sixteenth'] = '16th'
ordinals['fifteenth'] = '15th'
ordinals['fourteenth'] = '14th'
ordinals['thirteenth'] = '13th'
ordinals['twelfth'] = '12th'
ordinals['eleventh'] = '11th'
ordinals['tenth'] = '10th'
ordinals['nineth'] = '9th'
ordinals['eighth'] = '8th'
ordinals['seventh'] = '7th'
ordinals['sixth'] = '6th'
ordinals['fifth'] = '5th'
ordinals['fourth'] = '4th'
ordinals['third'] = '3rd'
ordinals['second'] = '2nd'
ordinals['first'] = '1st'

nums = OrderedDict()
nums['thirty one'] = '31'
nums['thirty'] = '30'
nums['twenty nine'] = '29'
nums['twenty eight'] = '28'
nums['twenty seven'] = '27'
nums['twenty six'] = '26'
nums['twenty five'] = '25'
nums['twenty four'] = '24'
nums['twenty three'] = '23'
nums['twenty two'] = '22'
nums['twenty one'] = '21'
nums['twenty'] = '20'
nums['nineteen'] = '19'
nums['nine teen'] = '19'
nums['eighteen'] = '18'
nums['eight teen'] = '18'
nums['seventeen'] = '17'
nums['seven teen'] = '17'
nums['sixteen'] = '16'
nums['six teen'] = '16'
nums['fifteen'] = '15'
nums['fourteen'] = '14'
nums['four teen'] = '14'
nums['thirteen'] = '13'
nums['twelve'] = '12'
nums['eleven'] = '11'
nums['ten'] = '10'
nums['nine'] = '9'
nums['eight'] = '8'
nums['seven'] = '7'
nums['six'] = '6'
nums['five'] = '5'
nums['four'] = '4'
nums['three'] = '3'
nums['two'] = '2'
nums['one'] = '1'
nums['zero'] = '0'
nums['oh'] = '0'

hours = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
         "ten", "eleven", "twelve"]
minutes = ["fifteen", "thirty", "forty five"]
d_time = {}
for hour, hr in zip(hours, range(1,13)):
    for minute, mn in zip(minutes, [15, 30, 45]):
        d_time[hour + ' '+ minute] =str(hr)+ ":"+ str(mn)

homonyms = {}
homonyms['won'] = 'one'
homonyms['too'] = 'two'
homonyms['to'] = 'two'
homonyms['tree'] = 'three'
homonyms['for'] = 'four'
homonyms['ate'] = 'eight'
homonyms['fort'] = 'fourth'
homonyms['forth'] = 'fourth'
homonyms['fit'] = 'fifth'
homonyms['tent'] = 'tenth'

state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'Washington DC': 'DC',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}
states = {}
for state in state_abbrev:
    states[state.lower()] = state_abbrev[state]


def years_to_digits(s):
    """ Examples:
    'two thousand seventeen' -> '2017'
    'two thousand and seventeen' -> '2017'

    Up to 2030
    """
    for val in year_vals.keys():
        s = s.replace(val, ', ' + year_vals[val])
    return s


def ordinals_to_ordinals(s):
    """ Example:
    'third' -> '3rd'

    Up to 31st (intended for dates)
    """
    for val in ordinals.keys():
        s = s.replace(val, ordinals[val])
    return s


def wordnums_to_nums(s):
    """ Examples:
    'four' -> '4'
    'fourteen' -> '14'
    'four teen' -> '14'

    Up to 31 (intended for dates, hours, and digits in zipcodes)
    """
    for val in nums.keys():
        s = s.replace(val, nums[val])
    return s


def hour_with_min_to_time(s):
    """ Example:
    'one forty five' -> '1:45'

    Only considers 15, 30, 45 for now
    """
    for val in d_time.keys():
        s = s.replace(val, d_time[val])
    return s


def replace_homonyms(s):
    """ Trying to catch examples where a number was transcribed as a homonym 
    of that number.

    Example:
    'for' -> 'four'
    """
    for val in homonyms.keys():
        s = s.replace(val, homonyms[val])
    return s 
