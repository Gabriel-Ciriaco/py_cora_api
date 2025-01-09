import os

import pandas as pd
from pandas.core.frame import DataFrame

from docling.document_converter import DocumentConverter
from docling_core.types.doc import TableItem


FILE_NAME = "Nome do Extrato sem .PDF"
DIR_PATH = os.path.abspath(f"PATH do Extrato")


def pdf_to_xlsx(file_name: str, dir_path: str) -> None:
  source= f"{dir_path}\{file_name}.pdf"
  output = f"{dir_path}\{file_name}.xlsx"

  converter = DocumentConverter()
  result = converter.convert(source)

  for item, level in result.document.iterate_items():
    if isinstance(item, TableItem):
      table_df = item.export_to_dataframe()
      treat_dataframe(table_df).to_excel(output)

'''
    TO DO:

    Função responsável por tratar corretamente os dados coletados.
'''
def treat_dataframe(df: DataFrame) -> DataFrame:
  pass

if __name__ == '__main__':
  pdf_to_xlsx(FILE_NAME, DIR_PATH)
