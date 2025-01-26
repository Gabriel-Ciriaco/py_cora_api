from __future__ import annotations
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

  def __enter__(self) -> Cora_API:
    return self

  def __exit__(self, *args) -> None:
    if self.handler.token_updater:
      self.handler.token_updater.cancel()

    self.closed = True
    print("[CORA_API]: Closed Connection.")

  def close(self) -> None:
    if not self.closed:
      self.__exit__()

  def handle_response(self, identifier: str, e: Request_Error) -> None:
    if e.message:
      print(f"{identifier}: (Error Code: {e.code}) {e.message}")

    if e.errors:
      for error in e.errors:
        print(f"{identifier}: (Error Code: {error['code']}) {error['message']}")


  def GET_BANK_STATEMENT(
      self,
      start_date: str = None,
      end_date: str = None,
      type: str = None,
      transaction_type: str = None,
      page: int = None,
      per_page: int = None,
      aggregation: bool = None
    ) -> Union[Bank_Statement, None]:
    '''
      TO-DO: Usar programação assincrona aqui!
      Lidar com erro de páginação do request!
    '''
    params = {
      'start': start_date,
      'end': end_date,
      'type': type,
      'transaction_type': transaction_type,
      'page': page,
      'per_page': per_page,
      'aggr': aggregation
    }

    with self.handler as request:
      try:
        response = request.get('/bank-statement/statement', params=params)

        return Bank_Statement(response)
      except Request_Error as e:
        self.handle_response("[GET_BANK_STATEMENT]", e)
        return None
