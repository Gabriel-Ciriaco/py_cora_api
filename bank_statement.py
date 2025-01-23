from datetime import datetime

def correct_money(value: int) -> float:
    return float(value) / 100

class StartEnd():
  def __init__(self, date: dict) -> None:
    self.date = self.parse_date(date['date'])
    self.balance = correct_money(date['balance'])

  def parse_date(self, iso_date: str) -> datetime:
    return datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%S")

class Aggregations():
  def __init__(self, agg: dict) -> None:
    self.creditTotal = int(agg['creditTotal'])
    self.debitTotal = int(agg['debitTotal'])

class CounterParty():
  def __init__(self, cnt_party: dict) -> None:
    self.name = str(cnt_party['name'])
    self.identity = str(cnt_party['identity'])

class Transaction():
  def __init__(self, transaction: dict) -> None:
    self.id = str(transaction['id'])
    self.type = str(transaction['type'])
    self.description = str(transaction['description'])
    self.counterParty = CounterParty(transaction['counterParty'])

class Header():
  def __init__(self, header: dict) -> None:
    self.businessName = str(header['businessName'])
    self.businessDocument = str(header['businessDocument'])

class Entry():
  def __init__(self, entry: dict) -> None:
    self.dict = entry

    self.id = str(entry['id'])
    self.type = str(entry['type'])

    self.amount = correct_money(entry['amount'])
    self.createdAt = datetime.strptime(entry['createdAt'], "%Y-%m-%dT%H:%M:%S+%f")

    self.transaction = Transaction(entry['transaction'])

  def __str__(self):
    return str(self.dict)

class Bank_Statement():
  def __init__(self, statement: dict) -> None:
    self.dict = statement

    self.start = StartEnd(statement['start'])
    self.end = StartEnd(statement['end'])

    self.entries = [Entry(entry) for entry in statement['entries']]

    self.aggregations = Aggregations(statement['aggregations'])

    self.header = Header(statement['header'])

  def __str__(self):
    return str(self.dict)