from time import time

class Printable:
    def __repr__(self):
        return str(self.__dict__)