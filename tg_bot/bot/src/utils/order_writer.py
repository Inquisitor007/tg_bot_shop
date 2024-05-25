import csv
from typing import Iterable


class CSVWriter:
    def __init__(self,
                 path: str = 'data.csv',
                 mode: str = 'a'):
        self.path = path
        self.mode = mode
        if self.mode == 'w':
            self._csv_init()

    def writerow(self, order):
        with open(self.path,
                  mode=self.mode,
                  newline='',
                  encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(order)

    def _csv_init(self):
        with open(self.path,
                  mode='w',
                  newline='',
                  encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([
                'id', 'Наименование', 'URL',
                'Регулярная цена', 'Промо цена', 'Бренд'
            ])
            self.mode = 'a'
