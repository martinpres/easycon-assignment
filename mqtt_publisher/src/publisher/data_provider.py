import requests


class DataProvider:

    def __init__(self, datasource_url):
        self._datasource_url = datasource_url

    def get(self):
        response = requests.get(self._datasource_url)
        data = response.json()
        return data
