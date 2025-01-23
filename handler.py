import os

import threading
import uuid

from typing import Union

import requests

from dotenv import load_dotenv

load_dotenv()

class Request_Error(Exception):
  def __init__(self, error_details: dict) -> None:
    self.code = error_details['code']

    self.message = self.message_handler(error_details)

    self.errors = error_details['errors'] if 'errors' in error_details else None

    message = f"(Error Code: {self.code}) {self.message}"

    super().__init__(message)


  def message_handler(self, error_details: dict) -> object:
    if 'message' in error_details:
      return error_details['message']
    elif 'error_description' in error_details:
      return error_details['error_description']
    else:
      return None


def response_handler(res: requests.Response) -> Union[requests.Response, None]:
  code = res.status_code // 100

  if code == 2:
    return res.json()
  elif code == 4 or code == 5:
    res_data = res.json()
    if 'code 'not in res_data:
      res_data['code'] = res.status_code

    raise Request_Error(res_data)


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

    try:
      return response_handler(
        requests.get(
          url=self.BASE_URL + endpoint,
          headers=headers,
          params=params,
          data=data,
          cert=self.CERTIFICATES)
      )
    except Request_Error as e:
      raise e

  def post(self, endpoint: str = None, params: dict = None, data: dict = None):
    try:
      return response_handler(
        requests.post(
          url=self.BASE_URL + endpoint,
          params=params,
          data=data,
          cert=self.CERTIFICATES
        )
      )
    except Request_Error as e:
      raise e

  def __get_token__(self) -> None:
    try:
      data = {
        'grant_type': 'client_credentials',
        'client_id': self.CLIENT_ID,
        }

      response = self.post('/token', data=data)
      self.auth = f"{response['token_type']} {response['access_token']}"
      self.__update_token__(response['expires_in'])
    except Request_Error as e:
      raise Exception(e.message)

  def __update_token__(self, time_in_seconds: int) -> None:
    self.token_updater = threading.Timer(time_in_seconds, self.__get_token__)
    self.token_updater.start()
