class RTree:
    children = []
    R = 0
    def __init__(self, R):
        self.R = R
    def add(self, x, y, type, subtype, name, adress):
        pass



f = open('ukraine_poi.csv')
for line in f:
    info = line.split(';')
    # print(info)


f.close()