import os
import threading

import time
import uuid

import locale
from datetime import datetime


import requests
from dotenv import load_dotenv


load_dotenv()

locale.setlocale( locale.LC_ALL, '' )

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


  def GET_BANK_STATEMENT(self) -> dict:
    '''TO-DO: Usar programação asincrona aqui!'''
    if self.is_updating_token:
      return None

    req_id = str(uuid.uuid4())

    headers = {
      "Idempotency-Key": req_id,
      "Authorization": self.auth,
      "accept": "application/json"
    }

    response = requests.get(self.url + '/bank-statement/statement', headers=headers)
    response_data = response.json()

    if response.status_code == 200:
      return response_data['entries']
    else:
      return None

if __name__ == '__main__':
  test = Cora_API()
  extratos = test.GET_BANK_STATEMENT()

  for extrato in extratos:
    nome_cliente = extrato['transaction']['counterParty']['name']
    tipo_transacao = extrato['type']
    valor = locale.currency(float(extrato['amount']) / 100, grouping=True)
    data_transacao = datetime.strptime(extrato['createdAt'], "%Y-%m-%dT%H:%M:%S+%f")

    print(f'{data_transacao} {tipo_transacao} {nome_cliente} {valor}')

  test.close()