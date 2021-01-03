class AF:

    def __init__(self, filename) -> None:
        super().__init__()
        self.nr_noduri = 0
        self.nr_muchii = 0
        self.graf = {}
        self.stari_finale = []
        self.alfabetul = []
        self.stari = []
        self.stare_initiala = ""
        self.read_file(filename)

    @staticmethod
    def print_menu():
        print('-' * 32)
        print("Astazi avem in meniu:")
        print("1. Teorie")
        print("2. Verifica daca o secventa este acceptata")
        print("3. Cel mai lung prefix acceptat dintr-o secventa")
        print("4. Exit")
        print('-' * 32)

    def teorie(self):
        # print(f'Multimea starilor: {[x for x in range(nr_noduri)]}')
        print(f'Multimea starilor: {[x for x in self.stari]}')
        print(f'Alfabetul: {sorted(self.alfabetul)}')
        print(f'Tranzitiile:')
        for x in self.graf:
            for y in self.graf[x]:
                print(f'    {y[0]}')
                print(f'{x} ----> {y[1]}')
        print(f'Stari finale: {self.stari_finale}')

    def verifica(self, stare, secventa):
        if secventa == "":
            if stare in self.stari_finale:
                return True
            else:
                return False
        ok = False
        for x in self.graf[stare]:
            if x[0] == secventa[0]:
                ok = self.verifica(x[1], secventa[1:]) or ok
        return ok

    def prefix(self, stare, sec, secventa):
        if secventa == "":
            if stare in self.stari_finale:
                return secventa
            else:
                return sec
        ok = secventa
        for x in self.graf[stare]:
            if x[0] == secventa[0]:
                rez = self.prefix(x[1], sec, secventa[1:])
                ok = rez if len(rez) < len(ok) else ok
        return ok

    def wrapper_prefix(self, secventa):
        aux = self.prefix('0', secventa, secventa)
        if aux == "":
            return secventa
        return secventa[:-1 * len(aux)]

    def wrapper_verifica(self, secventa):
        return self.verifica(self.stare_initiala, secventa)

    def ui(self):
        while True:
            self.print_menu()
            comanda = input("> ")
            if comanda == "1":
                self.teorie()
            elif comanda == "2":
                # secventa acceptata
                secventa = input("Secventa: ")
                if self.wrapper_verifica(secventa):
                    print('Secventa e acceptata')
                else:
                    print('Secventa nu e acceptata')
            elif comanda == "3":
                # prefixul
                secventa = input("Secventa: ")
                print(f'Prefixul: {self.wrapper_prefix(secventa)}')
            elif comanda == "4":
                break
            else:
                print("Comanda invalida")

    def read_file(self, nume_fisier):
        with open(nume_fisier, "r") as file:
            self.nr_noduri = int(file.readline())
            self.nr_muchii = int(file.readline())
            n = self.nr_muchii
            for x in range(self.nr_noduri):
                self.graf[str(x)] = []
            for linie in file:
                linie = linie.strip()
                if n > 0:
                    n = n - 1
                    x = linie.split(",")
                    if n == self.nr_muchii - 1:
                        self.stare_initiala = x[0]
                    self.graf[x[0]].append(x[1:])
                    # citim alfabet si stari initiale
                    if x[1] not in self.alfabetul:
                        self.alfabetul.append(x[1])
                    if x[0] not in self.stari:
                        self.stari.append(x[0])
                    if x[2] not in self.stari:
                        self.stari.append(x[2])
                else:
                    self.stari_finale.append(linie)

#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     # read_file("date.txt")
#     read_file("bonus.txt")
#     # for a in graf:
#     #     print(f'{a}, {graf[a]}')
#     ui()
