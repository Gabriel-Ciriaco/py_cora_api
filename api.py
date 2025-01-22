import os
import threading
import uuid

import requests
from dotenv import load_dotenv

from bank_statement import Bank_Statement


load_dotenv()


class Cora_API():
  def __init__(self):
    self.url = "https://matls-clients.api.cora.com.br"

    self.CLIENT_ID = os.getenv('CORA_CLIENT_ID')
    self.CERTIFICATES = ('./certificates/certificate.pem', './certificates/private-key.key')

    self.get_token()


  def get_token(self):
    self.is_updating_token = True

    data = {
      'grant_type': 'client_credentials',
      'client_id': self.CLIENT_ID,
    }

    response = requests.post(self.url + '/token', data=data, cert=self.CERTIFICATES)
    response_data = response.json()

    if response.status_code == 200:
      self.auth = f"{response_data['token_type']} {response_data['access_token']}"
      self.update_token(response_data['expires_in'])
    else:
      print(response_data['error'])

    self.is_updating_token = False


  def update_token(self, time_in_seconds):
    self.token_updater = threading.Timer(time_in_seconds, self.get_token)
    self.token_updater.start()

  def close(self):
    self.token_updater.cancel()


  def GET_BANK_STATEMENT(self, start_date: str = None, end_date: str = None) -> dict:
    '''TO-DO: Usar programação asincrona aqui!'''
    if self.is_updating_token:
      return None

    req_id = str(uuid.uuid4())

    headers = {
      "Idempotency-Key": req_id,
      "Authorization": self.auth,
      "accept": "application/json"
    }

    if start_date: params['start'] = start_date
    if end_date: params['end'] = end_date

    params = {
      'perPage': 1000
    }

    response = requests.get(self.url + '/bank-statement/statement', headers=headers, params=params)
    response_data = response.json()

    if response.status_code == 200:
      return Bank_Statement(response_data)
    else:
      return None
