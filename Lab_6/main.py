import math

# x, y - координаты искомой точки, х1, у1 - координаты центра круга, R - радиус
def dotInCircle(x, y, x1, y1, R):
    if ((x - x1) ** 2 + (y - y1) ** 2) <= R ** 2:
        return True
    return False

# нахождение координат по долготе и широте
def findXY(latitude, longitude):
    return 6371 * math.cos(latitude) * math.cos(longitude), 6371 * math.cos(latitude) * math.sin(longitude)

# листок с координатами и информацией
class Leaf:
    def __init__(self, cord, type, subtype, name, adress):
        self.x = cord[0]
        self.y = cord[1]
        self.type = type
        self.subtype = subtype
        self.name = name
        self.adress = adress
    def __str__(self):
        return 'Node: [x: %f, y: %f, type: %s, subtype: %s, name: %s, adress: %s' % (self.x, self.y, self.type, self.subtype, self.name, self.adress)

class Node:
    def __init__(self, cord, h, w, depth):
        self.x = cord[0]
        self.y = cord[1]
        self.h = h
        self.w = w
        self.depth = depth
        self.dots = 0
        self.children = [None, None]
        self.divided = False
        self.leafes = []

    def add(self, leaf):
        # если нода разделеная, то находим куда нужно добавить
        if self.divided:
            temp = self
            # тут проверка на то, что нода не начальный корень
            if self.children[0] != None:
                if self.x - self.w < leaf.x and self.x > leaf.x:
                    temp = self.children[0]
                else:
                    temp = self.children[1]
                #находим место куда добавить
                while temp.divided:
                    if temp.depth % 2:
                        if temp.x - temp.w < leaf.x and temp.x > leaf.x:
                            temp = temp.children[0]
                        else:
                            temp = temp.children[1]
                    else:
                        if temp.y + temp.h > leaf.y and temp.y < leaf.y:
                            temp = temp.children[0]
                        else:
                            temp = temp.children[1]
            # если в ноде в которую нужно добавить, больше 100 точек, делим ее на 2 части, добавляя в эти ноды листья
            if temp.dots > 100:
                if temp.depth % 2:
                    temp.children[0] = Node(((temp.x - temp.w) / 2, temp.y), temp.w / 2, temp.h, temp.depth + 1)
                    temp.children[1] = Node(((temp.x + temp.w) / 2, temp.y), temp.w / 2, temp.h, temp.depth + 1)
                    for i in temp.leafes:
                        if i.x > temp.x:
                            temp.children[0].leafes.append(i)
                            temp.children[0].dots += 1
                        else:
                            temp.children[1].leafes.append(i)
                            temp.children[1].dots += 1
                    if temp.x - temp.w < leaf.x and temp.x > leaf.x:
                        temp.children[0].leafes.append(leaf)
                        temp.children[0].dots += 1
                    else:
                        temp.children[1].leafes.append(leaf)
                        temp.children[1].dots += 1
                else:
                    temp.children[0] = Node((temp.x, (temp.y + temp.h) / 2), temp.w, temp.h / 2, temp.depth + 1)
                    temp.children[1] = Node((temp.x, (temp.y - temp.h) / 2), temp.w, temp.h / 2, temp.depth + 1)
                    for i in temp.leafes:
                        if i.y > temp.y:
                            temp.children[0].leafes.append(i)
                            temp.children[0].dots += 1
                        else:
                            temp.children[1].leafes.append(i)
                            temp.children[1].dots += 1
                    if temp.y + temp.h > leaf.y and temp.y < leaf.y:
                        temp.children[0].leafes.append(leaf)
                        temp.children[0].dots += 1
                    else:
                        temp.children[1].leafes.append(leaf)
                        temp.children[1].dots += 1
                temp.divided = True
                temp.leafes = []
            else:
                temp.leafes.append(leaf)
                temp.dots += 1
        #если в корне меньше 100 точек, то просто их добавляем
        elif self.dots <= 100:
            self.leafes.append(leaf)
            self.dots += 1
        # иначе ставим корень деленным и добавляем листок
        else:
            self.leafes.append(leaf)
            self.divided = True


    #тут нужно написать код..(
    def findCord(self, cord, R, out):
        x = cord[0]
        y = cord[1]
        if self.depth % 2:
            if self.x - self.w < x and self.x > x:
                pass
            else:
                pass
        else:
            if self.y + self.h > y and self.y < y:
                pass
            else:
                pass





tree = Node((0, -5109), 6372, 1300, 1)
f = open('ukraine_poi.csv')
i, out = 0, []
for line in f:
    i += 1
    info = line.split(';')
    info[0] = info[0].replace(',', '.')
    info[1] = info[1].replace(',', '.')
    try:
        leaf = Leaf(findXY(float(info[0]), float(info[1])), info[2], info[3], info[4], info[5])
        tree.add(leaf)
    except ValueError:
        print("Value error on line:", i)
    print(i)
print("Строк всего:", i)
f.close()
