import pandas as pd

class Szyba:
    def __init__(self, szerokosc, wysokosc, grubosc, budowa, ref, linia):
        self.szer = szerokosc
        self.wys = wysokosc
        self.grubosc = grubosc
        self.budowa = budowa
        self.ref = ref
        self.linia = linia
    def switchSize(self):
        wiekszy = max(self.szer, self.wys)
        mniejszy = min(self.szer, self.wys)
        if mniejszy > 1700:
            print('za duża szyba')
        elif wiekszy > 1700:
            self.szer = wiekszy
            self.wys = mniejszy
        else:
            self.szer = mniejszy
            self.wys = wiekszy
        return (self.szer, self.wys)


    def getNr(self):
        mniejszy = min(self.szer, self.wys)
        wiekszy = max(self.szer, self.wys)
        if wiekszy > 1700:
            nr = 4
        elif mniejszy > 1101:
            nr = 4
        elif mniejszy > 851:
            nr = 3
        elif mniejszy > 561:
            nr = 2
        elif mniejszy >= 350:
            nr = 1
    #bardzo małe szyby dodatkowe wymiarowanie
        elif mniejszy < 350 and wiekszy >= 570:
            nr = 2
        else:
            nr = 1
        return nr
    def __repr__(self):
        return f"Ref {self.ref}: {self.szer}x{self.wys} {self.grubosc}  {self.budowa}  rozmiar {self.switchSize()}"
    def __str__(self):
        return self.__repr__()

def rackPack(FreeRowSpace, df):
    lista = df['getNr']
    remain = [FreeRowSpace]
    solution = [[]]
    for i, nr in enumerate(lista):
        x = df.iloc[i]['object']
        for j,free in enumerate(remain):
            if free >= nr:
                remain[j] -= nr
                solution[j].append(x)
                break
        else:
            solution.append([x])
            remain.append(FreeRowSpace-nr)
    return solution

def textFileParser(lines, df, dfcols):
    for row in lines[3:-1]:
        budowa = row[0:40].strip()
        ilosc = int(row[43:49])
        szerokosc = int(row[48:57])
        wysokosc = int(row[58:64])
        grubosc = int(row[74:79])
        ref = row[83:97].strip()
        for szt in range(ilosc):
            szyba = Szyba(szerokosc, wysokosc, grubosc, budowa, ref, row)
            slotsNr = szyba.getNr()
            size = szyba.switchSize()
            szer = int(size[0])
            wys = int(size[1])
            df = df._append(pd.Series([szyba.ref, szyba.szer, szyba.wys, szyba.grubosc, szyba.budowa, slotsNr, szer, wys, szyba],
                                  index=dfcols), ignore_index=True)
    return df


#dfcols = ['Referencja', 'Szerokosc', 'Wysokosc', 'grubosc', 'bodowa', 'getNr', 'szer', 'wys', 'object']
#df = pd.DataFrame(columns=dfcols)
#lines = open('ZBR_0706-23szyby_2.txt', 'r').readlines()
#df = textFileParser(lines, df, dfcols)
#df_sorted = df.sort_values(by=['getNr', 'wys', 'szer'], ascending=[False, False, False])
#FreeRowSpace= 4
#RowsPackDf = rackPack(FreeRowSpace, df_sorted)
