import os

import threading
import uuid

import requests

from dotenv import load_dotenv

load_dotenv()


class Response_Handler():
  def __init__(self, response: requests.Response) -> None:
    print(response)


class Request_Handler():
  def __init__(self, url: str) -> None:
    self.CLIENT_ID = os.getenv('CORA_CLIENT_ID')
    self.CERTIFICATES = ('./certificates/certificate.pem', './certificates/private-key.key')

    self.BASE_URL = url
    self.__get_token__()


  def __enter__(self):
    return self


  def __exit__(self, *args):
    if self.token_updater:
      self.token_updater.cancel()


  def get(self, endpoint: str = None, params: dict = None, data: dict = None) -> None:
    req_id = str(uuid.uuid4()) # Unique ID for Idempotency

    headers = {
      "Idempotency-Key": req_id,
      "Authorization": self.auth,
      "accept": "application/json"
    }

    return requests.get(url=self.BASE_URL + endpoint, headers=headers, params=params, data=data, cert=self.CERTIFICATES)


  def __get_token__(self) -> None:
    data = {
      'grant_type': 'client_credentials',
      'client_id': self.CLIENT_ID,
    }

    response = requests.post(self.BASE_URL + '/token', data=data, cert=self.CERTIFICATES)
    response_data = response.json()

    if response.status_code == 200:
      self.auth = f"{response_data['token_type']} {response_data['access_token']}"
      self.__update_token__(response_data['expires_in'])
    else:
      raise Exception(response_data['error'])

  def __update_token__(self, time_in_seconds: int) -> None:
    self.token_updater = threading.Timer(time_in_seconds, self.__get_token__)
    self.token_updater.start()
