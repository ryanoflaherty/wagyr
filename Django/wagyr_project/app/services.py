import json

API_KEY = 'ukhq6uys9ukzy4rg9p8y5ejw'

def get_dailySched(month=3, day=23):
    url = 'http://api.sportradar.us/ncaamb-t3/games/2015/REG/schedule.xml'
    params = {'api_key': API_KEY}
    response = requests.get(url, params)
    schedule = response.json()
    return schedule


