import math
# x, y - координаты искомой точки, х1, у1 - координаты центра круга, R - радиус
def dotInCircle(x, y, x1, y1, R):
    if ((x - x1)**2 + (y - y1)**2) <= R**2:
        return True
    return False
def findXY(latitude, longitude):
    return 6371*math.cos(latitude)*math.cos(longitude), 6371*math.cos(latitude)*math.sin(longitude)

class Leaf:
    def __init__(self, cord, type = None, subtype = None, name = None, adress = None):
        self.cord = cord
        self.x = cord[0]
        self.y = cord[1]
        self.type = type
        self.subtype = subtype
        self.name = name
        self. adress = adress
    def __str__(self):
        return 'Node: ['+str(self.x)+' '+str(self.y)+' type: '+self.type+' subtype: '+self.subtype+' name: '+self.name+' adress: '+self.adress+']'


class Node:
    def __init__(self, cord, h, w, deapth, dots):
        self.cord = cord
        self.north = (cord[0], cord[1] + h) #верх
        self.south = (cord[0], cord[1] - h) #низ
        self.west = (cord[0] - w, cord[1]) #лево
        self.east = (cord[0] + w, cord[1]) #право
        self.deapth = deapth
        self.dots = dots
        self.leafes = []
        self.h = h
        self.w = w
    def addLeaf(self, leaf):
        self.leafes.append(leaf)
        self.dots += 1

class RTree:
    def __init__(self, cord, h, w, deapth, dots):
        self.cord = cord
        self.x = cord[0]
        self.y = cord[1]
        self.north = (cord[0], cord[1] + h)  # верх
        self.south = (cord[0], cord[1] - h)  # низ
        self.west =  (cord[0] - w, cord[1])  # лево
        self.east =  (cord[0] + w, cord[1])  # право
        self.h = h
        self.w = w
        self.deapth = deapth
        self.dots = dots
        self.children = [None, None]
        self.root = Node(cord, h, w, deapth, dots)

    def add(self, leaf):
        # если нет корня, то дерево поделено уже и нужно точку добавить в одну из следующик коробок
        if self.root == None:
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
                self.children[0] = RTree(((self.x - self.w) / 2, self.y), self.w / 2, self.h, self.deapth + 1, 0)
                self.children[1] = RTree(((self.x + self.w) / 2, self.y), self.w / 2, self.h, self.deapth + 1, 0)
                for i in self.root.leafes:
                    if i.x > self.x:
                        self.children[0].add(i)
                    else:
                        self.children[1].add(i)
                if self.x - self.w < leaf.x and self.x > leaf.x:
                    self.children[0].add(leaf)
                else:
                    self.children[1].add(leaf)
            else:
                self.children[0] = RTree((self.x, (self.y + self.h) / 2), self.w, self.h / 2, self.root.deapth + 1, 0)
                self.children[1] = RTree((self.x, (self.y - self.h) / 2), self.w, self.h / 2, self.root.deapth + 1, 0)
                for i in self.root.leafes:
                    if i.y > self.y:
                        self.children[0].add(i)
                    else:
                        self.children[1].add(i)
                if self.y + self.h > leaf.y and self.y < leaf.y:
                    self.children[0].add(leaf)
                else:
                    self.children[1].add(leaf)
            self.root = None
        # иначе добавить листок в текущюю ноду
        else:
            self.root.addLeaf(leaf)
            self.dots += 1
        return



tree = RTree((0, 0), 6372, 6372, 1, 0)

f = open('ukraine_poi.csv')
for line in f:
    info = line.split(';')
    leaf = Leaf(findXY(float(line[0]), float(line[1])), line[2], line[3], line[4], line[5])
    tree.add(leaf)




f.close()