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

# if self.divided:
#     if self.deapth % 2:
#         if self.x - self.w < leaf.x and self.x > leaf.x:
#             self.children[0].add(leaf)
#         else:
#             self.children[1].add(leaf)
#     else:
#         if self.y + self.h > leaf.y and self.y < leaf.y:
#             self.children[0].add(leaf)
#         else:
#             self.children[1].add(leaf)


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

class Node:
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
            temp = None
            if self.x - self.w < leaf.x and self.x > leaf.x:
                temp = self.children[0]
            else:
                temp = self.children[1]
            while temp.divided:
                if temp.deapth % 2:
                    if temp.x - temp.w < leaf.x and temp.x > leaf.x:
                        temp = temp.children[0]
                    else:
                        temp = temp.children[1]
                else:
                    if temp.y + temp.h > leaf.y and temp.y < leaf.y:
                        temp = temp.children[0]
                    else:
                        temp = temp.children[1]
            if temp.dots > 5:
                if temp.deapth % 2:
                    temp.children[0] = Node(((temp.x - temp.w) / 2, temp.y), temp.w / 2, temp.h, temp.deapth + 1)
                    temp.children[1] = Node(((temp.x + temp.w) / 2, temp.y), temp.w / 2, temp.h, temp.deapth + 1)
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
                    temp.children[0] = Node((temp.x, (temp.y + temp.h) / 2), temp.w, temp.h / 2, temp.deapth + 1)
                    temp.children[1] = Node((temp.x, (temp.y - temp.h) / 2), temp.w, temp.h / 2, temp.deapth + 1)
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
        # если количество точек больше пяти, то делим коробку на 2 части и добавляем туда точки
        elif self.dots > 5:
            if self.deapth % 2:
                self.children[0] = Node(((self.x - self.w) / 2, self.y), self.w / 2, self.h, self.deapth + 1)
                self.children[1] = Node(((self.x + self.w) / 2, self.y), self.w / 2, self.h, self.deapth + 1)
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
                self.children[0] = Node((self.x, (self.y + self.h) / 2), self.w, self.h / 2, self.deapth + 1)
                self.children[1] = Node((self.x, (self.y - self.h) / 2), self.w, self.h / 2, self.deapth + 1)
                for i in self.leafes:
                    if i.y > self.y:
                        self.children[0].leafes.append(i)
                        self.children[0].dots += 1
                    else:
                        self.children[1].leafes.append(i)
                        self.children[1].dots += 1
                if self.y + self.h > leaf.y and self.y < leaf.y:
                    self.children[0].leafes.append(leaf)
                    self.children[0].dots += 1
                else:
                    self.children[1].leafes.append(leaf)
                    self.children[1].dots += 1
            self.divided = True
            self.leafes = []
        # иначе добавить листок в текущюю ноду
        else:
            self.leafes.append(leaf)
            self.dots += 1

tree = Node((0, 0), 3500, 3500, 1)
f = open('ukraine_poi.csv')
i = 0
for line in f:
    i += 1
    info = line.split(';')
    try:
        leaf = Leaf(findXY(float(line[0]), float(line[1])), line[2], line[3], line[4], line[5])
        tree.add(leaf)
    except ValueError:
        print("Value error on", i, "line\n", line)
print(i)
f.close()
