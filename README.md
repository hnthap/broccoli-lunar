# Broccoli: The Lunar Calendar API

Convert a date in Gregorian calendar to Lunar calendar.

## What is this

This repo does not do any calculations regarding the calendars. Instead it just tells the HuggingFace Space [`hnthap/am-lich-viet-nam`](https://huggingface.co/spaces/hnthap/am-lich-viet-nam) to calculate the calendar conversion and send it back via Gradio Client.

I created this repo to demonstrate how to create a backend for any HuggingFace Spaces.

## Setup the server

Create a file named `.env` in the repository's root directory with the following contents:

```txt
# Replace the values with your desired host name and port

HOSTNAME=localhost
PORT=8080
```

Create a Python virtual enviroment:

```sh
python -m venv env
./env/Scripts/activate # Or: source ./env/bin/activate
```

Activate the virtual environment, then run:

```sh
pip install -r requirements.txt
```

To start the server, run:

```sh
python app.py
```

## Usage

```sh
GET /api/{tz}/{year}/{month}/{day}
```

where

- `tz` is the time zone offset from UTC in hours
- `year` is the year (Gregorian calendar)
- `month` is the month (Gregorian calendar) with January is 1, February is 2, and so on.
- `day` is the day of month (Gregorian calendar) that starts from 1.

For example:

```sh
GET /api/7/2024/10/1
```

yields the following result:

```json
{
  "time_zone_hours": 7,
  "Gregorian": "2024-10-01",
  "lunar": {
    "year": 2024,
    "month": 8,
    "day": 29,
    "leap_month": false,
    "month_size": 30,
    "international": "2024-08-29 (30-day month)",
    "vi": "ngày 29 tháng Tám (đủ) năm Giáp Thìn",
    "zh": "甲辰年八月（大）廿九日",
    "emoji": "🌑"
  }
}
```
