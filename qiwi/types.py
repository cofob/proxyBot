class Operation:
    value = 'ALL'

    def __str__(self):
        return self.value


class IN(Operation):
    value = 'IN'


class OUT(Operation):
    value = 'OUT'


class ALL(Operation):
    value = 'ALL'


class CARD(Operation):
    value = 'QIWI_CARD'


class Source:
    value = 'QW_RUB'

    def __str__(self):
        return self.value


class RUB(Source):
    value = 'QW_RUB'


class USD(Source):
    value = 'QW_USD'


class EUR(Source):
    value = 'QW_EUR'


class SourceCard(Source):
    value = 'CARD'


class SourceMK(Source):
    value = 'MK'


class Status:
    value = 'SUCCESS'

    def __str__(self):
        return self.value


class SUCCESS(Status):
    value = 'SUCCESS'


class Transaction:
    txId = 0
    personId = 0
    date = ''
    status = SUCCESS
    type = IN
    account = ''
    total = 0
    commission = 0
    amount = 0
    comment = ''
