from collections import OrderedDict
from utility.printable import Printable

class Transaction(Printable):
    def __init__(self, sender, receiver, amount, signature):
        self.sender = sender
        self.receiver = receiver
        self.amount  = amount
        self.signature = signature

    def to_ordered_dict(self):
        return OrderedDict([('sender',self.sender),('receiver',self.receiver),('amount',self.amount),('signature',self.signature)])