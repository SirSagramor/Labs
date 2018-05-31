import math

# x, y - координаты искомой точки, х1, у1 - координаты центра круга, R - радиус
def dotInCircle(x, y, x1, y1, R):
    if ((x - x1) ** 2 + (y - y1) ** 2) <= R ** 2:
        return True
    return False

# нахождение координат по долготе и широте
def findXY(latitude, longitude):
    return 6371 * math.cos(latitude) * math.cos(longitude), 6371 * math.cos(latitude) * math.sin(longitude)

# self.north = (x, y + h)  # верх
# self.south = (x, y - h)  # низ
# self.west = (x - w, y)  # лево
# self.east = (x + w, y)  # право

class Leaf:
    def __init__(self, cord, type=None, subtype=None, name=None, adress=None):
        self.x = cord[0]
        self.y = cord[1]
        self.type = type
        self.subtype = subtype
        self.name = name
        self.adress = adress
    def __str__(self):
        return 'Node: [' + str(self.x) + ' ' + str(
            self.y) + ' type: ' + self.type + ' subtype: ' + self.subtype + ' name: ' + self.name + ' adress: ' + self.adress + ']'

class RTree:
    def __init__(self, cord, h, w, deapth):
        self.x = cord[0]
        self.y = cord[1]
        self.h = h
        self.w = w
        self.deapth = deapth
        self.dots = 0
        self.children = [None, None]
        self.divided = False
        self.leafes = []

    def add(self, leaf):
        # если дерево поделено уже то нужно точку добавить в одну из следующик коробок
        if self.divided:
            if self.deapth % 2:
                if self.x - self.w < leaf.x and self.x > leaf.x:
                    self.children[0].add(leaf)
                else:
                    self.children[1].add(leaf)
            else:
                if self.y + self.h > leaf.y and self.y < leaf.y:
                    self.children[0].add(leaf)
                else:
                    self.children[1].add(leaf)
        # если количество точек больше пяти, то делим коробку на 2 части и добавляем туда точки
        elif self.dots > 5:
            if self.deapth % 2:
                self.children[0] = RTree(((self.x - self.w) / 2, self.y), self.w / 2, self.h, self.deapth + 1)
                self.children[1] = RTree(((self.x + self.w) / 2, self.y), self.w / 2, self.h, self.deapth + 1)
                for i in self.leafes:
                    if i.x > self.x:
                        self.children[0].leafes.append(i)
                        self.children[0].dots += 1
                    else:
                        self.children[1].leafes.append(i)
                        self.children[1].dots += 1
                if self.x - self.w < leaf.x and self.x > leaf.x:
                    self.children[0].leafes.append(leaf)
                    self.children[0].dots += 1
                else:
                    self.children[1].leafes.append(leaf)
                    self.children[1].dots += 1
            else:
                self.children[0] = RTree((self.x, (self.y + self.h) / 2), self.w, self.h / 2, self.deapth + 1)
                self.children[1] = RTree((self.x, (self.y - self.h) / 2), self.w, self.h / 2, self.deapth + 1)
                for i in self.leafes:
                    if i.y > self.y:
                        self.children[0].add(i)
                    else:
                        self.children[1].add(i)
                if self.y + self.h > leaf.y and self.y < leaf.y:
                    self.children[0].add(leaf)
                else:
                    self.children[1].add(leaf)
            self.divided = True
        # иначе добавить листок в текущюю ноду
        else:
            self.leafes.append(leaf)
            self.dots += 1

tree = RTree((0, 0), 6372, 6372, 1)
f = open('ukraine_poi.csv')
for line in f:
    info = line.split(';')
    leaf = Leaf(findXY(float(line[0]), float(line[1])), line[2], line[3], line[4], line[5])
    tree.add(leaf)

f.close()
