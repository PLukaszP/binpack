import pandas as pd

class Glass:
    def __init__(self, width, height, thickness, construction, ref, row):
        self.szer = width
        self.wys = height
        self.grubosc = thickness
        self.budowa = construction
        self.ref = ref
        self.row = row

    def switch_size(self):
        longer_side = max(self.szer, self.wys)
        shorter_side = min(self.szer, self.wys)
        if shorter_side > 1700:
            print('za duża szyba')
        elif longer_side > 1700:
            self.szer = longer_side
            self.wys = shorter_side
        else:
            self.szer = shorter_side
            self.wys = longer_side
        return (self.szer, self.wys)

    def get_number(self):
        shorter_side = min(self.szer, self.wys)
        longer_side = max(self.szer, self.wys)
        if longer_side > 1700:
            nr = 4
        elif shorter_side > 1101:
            nr = 4
        elif shorter_side > 851:
            nr = 3
        elif shorter_side > 561:
            nr = 2
        elif shorter_side >= 350:
            nr = 1
        #very small glasses extra dimensioning
        elif shorter_side < 350 and longer_side >= 570:
            nr = 2
        else:
            nr = 1
        return nr

    def __repr__(self):
        return f"Ref {self.ref}: {self.szer}x{self.wys} {self.grubosc}  {self.budowa}  size {self.switch_size()}"

    __str__ = __repr__

def pack_into_racks(row_space, df):
    list = df['getNr']
    remain_row_space = [row_space]
    pack_solution = [[]]
    for list_index, nr in enumerate(list):
        x = df.iloc[list_index]['class_Glass_object']
        for j, free_row_space in enumerate(remain_row_space):
            if free_row_space >= nr:
                remain_row_space[j] -= nr
                pack_solution[j].append(x)
                break
        else:
            pack_solution.append([x])
            remain_row_space.append(row_space-nr)
    return pack_solution

def text_file_parser(lines, df, dfcols):
    for row in lines[3:-1]:
        construction = row[0:40].strip()
        pieces = int(row[43:49])
        width = int(row[48:57])
        height = int(row[58:64])
        thickness = int(row[74:79])
        ref = row[83:97].strip()
        for szt in range(pieces):
            glass = Glass(width, height, thickness, construction, ref, row)
            slots_numbers = glass.get_number()
            size = glass.switch_size()
            szer = int(size[0])
            wys = int(size[1])
            df = df._append(
                pd.Series([glass.ref, glass.szer, glass.wys, glass.grubosc,
                           glass.budowa, slots_numbers, szer, wys, glass],
                          index=dfcols),
                ignore_index=True
            )
    return df

