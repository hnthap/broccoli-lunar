from math import floor
import os
import re

from dotenv import load_dotenv
from fastapi import FastAPI
from gradio_client import Client
from uvicorn import run


app = FastAPI()
lunar_client = Client('hnthap/am-lich-viet-nam')


@app.get('/api/{tz}/{year}/{month}/{day}')
async def get_today_lunar_date(tz: str, year: int, month: int, day: int):
    tz = int(tz) if re.match(r'[\+\-]?\d+', tz) else float(tz) 
    languages = ['international', 'vi', 'zh']
    result = {
        'time_zone_hours': tz,
        'Gregorian': '{:04}-{:02}-{:02}'.format(year, month, day),
        'lunar': {},
    }
    for language in languages:
        item = lunar_client.predict(year, month, day, tz, language)
        result['lunar'][language] = item
    lunar = result['lunar']['international'][:]
    lunar = parse_lunar_date_string(lunar)
    if lunar is None:
        # TODO: Something went wrong. Fix this later. For now, just ignore it.
        return result
    result['lunar'] = dict(lunar, **result['lunar'])
    result['lunar']['emoji'] = get_lunar_phase_emoji(result['lunar']['day'])
    return result


LUNAR_PHASES = ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘']
INTERNATIONAL_LUNAR_DATE_PATTERN = \
    r'^(\d{4})\-(\d{2})(\+?)\-(\d{2}) \((29|30)\-day month\)$'
    

def get_lunar_phase_emoji(lunar_day):
    phase = (lunar_day + 1.875) / 3.75
    return LUNAR_PHASES[int(floor(phase)) % 8]


def parse_lunar_date_string(s: str):
    '''
    Parse the Lunar date string that matches the regular expression pattern 
    '^\d{4}\-\d{2}\+?\-\d{2} \((29|30)\-day month\)$'
    into a dictionary with the following keys: 
    'year': int,
    'month': int,
    'leap_month': bool,
    'day': int,
    'month_size': int.
    If the date string does not match the regular expression, return None.

    Example:
    parse_lunar_date_string('2022-01+-01 (29-day month)') 
    Output:
    {'year': 2022, 'month': 1, 'leap_month': True, 'day': 1, 'month_size': 29 }
    '''
    result = re.findall(INTERNATIONAL_LUNAR_DATE_PATTERN, s)
    if len(result) == 0:
        return None 
    year, month, is_leap, day, month_size = result[0]
    return {
        'year': int(year),
        'month': int(month),
        'day': int(day),
        'leap_month': is_leap == '+',
        'month_size': int(month_size),
    }


if __name__ == '__main__':
    load_dotenv()  # Load environment variables from .env file
    
    hostname = os.environ.get('HOSTNAME', 'localhost')
    port = int(os.environ.get('PORT', '8080'))
    run(app, host=hostname, port=port)

