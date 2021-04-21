import qiwi.types
import qiwi.models as models
import requests
import time
import threading


class Qiwi:
    def __init__(self, token: str, phone: (str, int), rows: int = 10, update_interval: int = 5,
                 base_url: str = 'https://edge.qiwi.com',
                 operation: qiwi.types.Operation = qiwi.types.IN,
                 sources: (list, tuple) = (qiwi.types.RUB, ), callback=None):
        self.callback = callback
        self.token = token
        self.phone = phone
        self.rows = rows
        self.sources = sources
        self.operation = operation
        self.update_interval = update_interval
        self.headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer '+token
        }
        self.unprocessed = []
        self.base_url = base_url
        self.thread = None

    def generate_link(self):
        sources = '&'.join([f'sources%5B%{i}5D={self.sources[i].value}' for i in range(len(self.sources))])
        url = f'/payment-history/v2/persons/{self.phone}/payments?' \
              f'rows={self.rows}&operation={self.operation.value}&{sources}'
        return self.base_url + url

    def tx(self, tx):
        try:
            m = models.Payment(txId=tx['txnId'])
            m.save()
            transaction = qiwi.types.Transaction()
            transaction.txId = tx['txnId']
            transaction.personId = tx['personId']
            transaction.date = tx['date']
            transaction.account = tx['account']
            transaction.amount = tx['sum']['amount']
            transaction.commission = tx['commission']['amount']
            transaction.total = tx['total']['amount']
            transaction.comment = tx['comment']
            if self.callback is not None:
                self.callback(transaction)
            else:
                self.unprocessed.append(transaction)
            return tx
        except models.IntegrityError:
            return

    def loop(self):
        response = requests.get(self.generate_link(), headers=self.headers)
        response.raise_for_status()
        r = response.json()
        for tx in r['data']:
            self.tx(tx)

    def start(self):
        while True:
            self.loop()
            time.sleep(self.update_interval)

    def start_thread(self):
        self.thread = threading.Thread(target=self.start)
        self.thread.start()
