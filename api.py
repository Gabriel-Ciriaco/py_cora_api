import atexit

from typing import Union

from handler import Request_Handler, Request_Error
from bank_statement import Bank_Statement


class Cora_API():
  def __init__(self, stage: bool = False) -> None:
    self.url = "https://matls-clients.api.stage.cora.com.br" if stage else "https://matls-clients.api.cora.com.br"

    self.handler = Request_Handler(self.url)

    atexit.register(self.close) # Close at end of script.
    self.closed = False

    print("[CORA_API]: Started connection.")

  def __enter__(self):
    return self

  def __exit__(self, *args):
    if self.handler.token_updater:
      self.handler.token_updater.cancel()

    self.closed = True
    print("[CORA_API]: Closed Connection.")

  def close(self):
    if not self.closed:
      self.__exit__()

  def GET_BANK_STATEMENT(self, start_date: str = None, end_date: str = None) -> Union[Bank_Statement, None]:
    '''
      TO-DO: Usar programação assincrona aqui!
      Lidar com erro de páginação do request!
    '''
    params = {}

    if start_date: params['start'] = start_date
    if end_date: params['end'] = end_date

    with self.handler as request:
      try:
        response = request.get('/bank-statement/statement', params=params)

        return Bank_Statement(response)
      except Request_Error as e:
        identifier = "[GET_BANK_STATEMENT]"

        if e.message:
          print(f"{identifier}: (Error Code: {e.code}) {e.message}")

        if e.errors:
          for error in e.errors:
            print(f"{identifier}: (Error Code: {error['code']}) {error['message']}")

        return None
