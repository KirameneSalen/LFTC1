import string
import re
import HashTable
from AF import AF

separators = [';', ',', '(', ')', '{', '}', '+', '-', '*', '/', '%', '=', '!', '<', '>']

separators_double = ['==', '!=', '||', '&&', '<=', '>=', '>>', '<<']

reserved_words = ['int', 'double', 'cin', 'cout', 'while', 'if', 'else', 'break', 'struct', 'main', 'return']

config = ["NIMIC", "ID", "CONST"] + reserved_words + separators + separators_double


class Scanner:
    __sursa = ""
    __string = ""
    __list = []
    __cod_atom = []
    __cod_ts = []
    __ts = HashTable.HashTable()
    __i = 0
    __numbersAF = AF("intregi.txt")
    __identifierAF = AF("gucci.txt")

    def __init__(self, sursa) -> None:
        super().__init__()
        self.__sursa = sursa

    """
    Citeste fisierul sursa si il salveaza intr-ul string
    """

    def read(self):
        with open(self.__sursa, 'r') as reader:
            self.__string = reader.read()

    """
    Ia urmatorul caracter din string
    """

    def get(self):
        aux = self.__string[self.__i]
        self.__i += 1
        return aux

    """
    Ia caracterul anterior
    """

    def back(self):
        self.__i -= 1

    """
    Creeaza tabelul FIP
    """

    def make_fip(self):
        self.__cod_atom = [-1] * len(self.__list)
        self.__cod_ts = [-1] * len(self.__list)
        x = 0
        for i in self.__list:
            if i in config:
                self.__cod_atom[x] = config.index(i)
                self.__cod_ts[x] = -1
            elif self.__identifierAF.wrapper_verifica(i):  # is ID
                if len(i) < 8:
                    self.__cod_atom[x] = 1
                    val = sum([ord(j) for j in i])
                    aux = self.__ts.cauta(val)
                    if not aux:
                        self.__ts.adauga(val)
                    self.__cod_ts[x] = self.__ts.index(val) + 1
            elif self.__numbersAF.wrapper_verifica(i):  # is constant
                self.__cod_atom[x] = 2
                val = sum([ord(j) for j in i])
                aux = self.__ts.cauta(val)
                if not aux:
                    self.__ts.adauga(val)
                self.__cod_ts[x] = self.__ts.index(val) + 1
            else:
                print(i)
                raise Exception("SYNTAX IS WRONG")
            x += 1

    """
    Pune tokenuri in lista
    """

    def parser(self):
        temporary_string = ""
        while True:
            try:
                aux = self.get()
                if aux in string.ascii_letters or aux in string.digits or aux in ['$', '_', '.']:
                    temporary_string += aux
                elif aux in ['+', '-']:
                    if temporary_string == "":
                        temporary_string += aux
                    else:
                        self.__list.append(temporary_string)
                        temporary_string = ""
                        aux2 = self.get()
                        if aux + aux2 in separators_double:
                            self.__list.append(aux + aux2)
                        else:
                            self.__list.append(aux)
                            self.back()
                elif aux in separators:
                    if temporary_string != '':
                        self.__list.append(temporary_string)
                    temporary_string = ""
                    aux2 = self.get()
                    if aux + aux2 in separators_double:
                        self.__list.append(aux + aux2)
                    else:
                        self.__list.append(aux)
                        self.back()
                elif aux in ['&', '|']:
                    if temporary_string != '':
                        self.__list.append(temporary_string)
                    temporary_string = ""
                    aux2 = self.get()
                    if aux + aux2 in separators_double:
                        self.__list.append(aux + aux2)
                    else:
                        raise Exception("Syntax wrong bitch")
                elif aux in string.whitespace:
                    if temporary_string != '':
                        self.__list.append(temporary_string)
                    temporary_string = ""
                else:
                    temporary_string += aux
            except IndexError:
                self.back()
                aux = self.get()
                if aux in separators:
                    self.__list.append(aux)
                return '\0'

    """
    Afiseaza lista dupa ce apeleaza celelalte functii
    """

    def run(self):
        self.read()
        self.parser()
        self.make_fip()
        output_file = "out.txt"
        with open(output_file, "w") as file:
            # file.write("-" * 25 + "\n")
            # file.write(f'{"ATOM":7} {"COD_ATOM":10} {"COD_TS":6}' + "\n")
            # file.write("-" * 25 + "\n")
            x = 0
            for i in self.__list:
                # file.write(f'{i:7} '
                #            f'{str(self.__cod_atom[x]):10} '
                #            f'{str(self.__cod_ts[x]) if self.__cod_ts[x] != -1 else "-":6}' + "\n")
                file.write(f'{i} {self.__cod_atom[x]}\n')
                x += 1
            x = 0
            # aux = self.__ts.afis()
            # file.write("-" * 25 + "\n")
            # file.write("TABELA DE SIMBOLURI" + "\n")
            # file.write("-" * 11 + "\n")
            # file.write(f'{"VALUE":5} {"INDEX":5}' + "\n")
            # file.write("-" * 11 + "\n")
            # for i in aux:
            #     file.write(f'{str(x):5} {str(i):5}' + "\n")
            #     x += 1


if __name__ == '__main__':
    Scanner('sursa.txt').run()
