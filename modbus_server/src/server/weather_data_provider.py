import requests


class DataProvider:

    def __init__(self, datasource_url):
        self._datasource_url = datasource_url

    def get(self):
        response = requests.get(self._datasource_url)
        data = response.json()
        current = data.get('current', {})
        return [
            current.get('temperature_2m', -1),
            current.get('relative_humidity_2m', -1),
            current.get('wind_speed_10m', -1)
        ]
