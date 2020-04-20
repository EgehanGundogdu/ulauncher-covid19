import requests


def remove_unnecessary_info(country):
    keys = ["Province", "City", "CityCode", "Lat", "Lon", "Slug", "Date", "CountryCode"]
    for i in keys:
        if i in country:
            country.pop(i)
    return country


def get_summary():
    return requests.get("https://api.covid19api.com/summary").json()


def generate_icon_path(key, flag_code=None):

    if flag_code:
        return f"images/flags/{flag_code}.png"
    return f"images/emoji/{key}.png"


def beautify_stats(stat):
    if type(stat) == int:
        return "{:,}".format(stat).replace(",", ".")
    return stat
