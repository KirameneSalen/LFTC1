"""
Tabela de dispersie cu adresare deschisa
"""


class HashTable:

    def __init__(self, m=10):
        super().__init__()
        self.__m = m
        self.__ch = [None] * self.__m

    def __dprim(self, x):
        return x % self.__m

    def __d(self, x, i):
        return (self.__dprim(x) + i) % self.__m

    def adauga(self, val):
        i = 0  # nr verificare
        gasit = False
        while True:
            j = self.__d(val, i)  # locatia de verificat
            if self.__ch[j] is None:
                self.__ch[j] = val  # memorez cheia
                gasit = True  # am gasit
            else:
                i += 1  # mai departe
            if i == self.__m or gasit:
                break
            if i == self.__m:
                return  # tabela e plina

    def __aux_search(self, val):
        i = 0
        gasit = False
        while True:
            j = self.__d(val, i)
            if self.__ch[j] == val:
                gasit = True
            else:
                i += 1
            if self.__ch[j] is None or gasit:
                break
        return [j, gasit]

    def cauta(self, val):
        return self.__aux_search(val)[1]

    def index(self, val):
        aux = self.__aux_search(val)
        return aux[0] if aux[1] else -1

    def afis(self):
        return self.__ch
