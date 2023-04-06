import json

import pandas as pd
import requests

# Set the API endpoint URL
url = 'https://www.renewables.ninja/api/data/pv'

# Set the query parameters
query_params = {
    'lat': 51.5,             # latitude of the location
    'lon': -0.1,             # longitude of the location
    'date_from': '2019-01-01',  # starting date of the data
    'date_to': '2019-01-02',    # ending date of the data
    'dataset': 'merra2',     # dataset to use for the simulation
    'capacity': 1,           # capacity of the PV system in kW
    'system_loss': 0.1,       # system loss in %
    'tracking': 0,           # tracking mode, 0 = fixed, 1 = 1-axis tracking, 2 = 2-axis tracking
    'tilt': 35,              # tilt angle of the PV system in degrees
    'azim': 180,             # azimuth angle of the PV system in degrees
    'format': 'json'         # format of the data, csv or json
}

# Send the GET request and get the response
response = requests.get(url, params=query_params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON
    data = response.json()
    data_pd = pd.read_json(json.dumps(data['data']), orient='index')
    # Print the data
    print(data)
else:
    print('Error fetching data:', response.text)
