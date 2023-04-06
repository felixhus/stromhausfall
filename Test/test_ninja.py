import time

import requests

token = '9d539337969f016d51d3c637ddba49bbc9fe6e71'
s = requests.session()
s.headers = {'Authorization': 'Token ' + token}

url = 'https://www.renewables.ninja/api/data/pv?lat=51.9223851680104&lon=8.37306698136307&date_from=2015-01-05&date_to=2015-01-06&dataset=sarah&capacity=1&system_loss=0.1&tracking=0&tilt=35&azim=0&format=json'
counter = 0

while True:
    response = s.get(url)
    if response.status_code == 200:  # Check if the request was successful
        counter += 1
        print(counter)
    else:
        print(f"Number of successful requests: {counter}")
        print(response.content)
        break
    time.sleep(1.5)

