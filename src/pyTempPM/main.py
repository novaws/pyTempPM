import requests
from bs4 import BeautifulSoup
from typing import Optional

class TempPM:
    def __init__(self):
        self.__url = 'https://temp.pm/'
        self.__headers = {
            'User-Agent': f'TempPM python library'
        }
        self.__session = requests.Session()

    def __get_csrf_token(self):
        r = self.__session.get(self.__url)
        soup = BeautifulSoup(r.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrf'}).get('value')
        return csrf_token

    def create_note(self, note: str, ttl: Optional[str] = '3', password: Optional[str] = None) -> str:
        """
        :param note: text of the note
        :param ttl: time to live of the note must be set from only specific values
        :param password: password for note
        :return: url for note
        """
        certain_values = ('15m', '30m', '45m', '1h', '6h', '12h', '1', '3', '7', '30', '60')
        if ttl not in certain_values:
            raise ValueError(f'ttl: must be one of {certain_values}')
        csrf_token = self.__get_csrf_token()
        data = {
            'note': note,
            'create': 'Create+Message',
            'ttl': ttl,
            'csrf': csrf_token,
            'cpass_create': password
        }
        r = self.__session.post(self.__url, data=data)
        soup = BeautifulSoup(r.text, 'html.parser')
        result_url = soup.find('input', {'id': 'noteurl1'}).get('value')
        return result_url
