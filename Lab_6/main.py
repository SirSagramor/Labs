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
        self.type = type
        self.subtype = subtype
        self.name = name
        self. adress = adress
    def __str__(self):
        return 'Node: ['+str(self.x)+' '+str(self.y)+' type: '+self.type+' subtype: '+self.subtype+' name: '+self.name+' adress: '+self.adress+']'


class Node:
    def __init__(self, cord, h, w, height, dots):
        self.cord = cord
        self.north = (cord[0], cord[1] + h) #верх
        self.south = (cord[0], cord[1] - h) #низ
        self.west = (cord[0] - w, cord[1]) #лево
        self.east = (cord[0] + w, cord[1]) #право
        self.height = height
        self.dots = dots
        self.leafes = []
    def addLeaf(self, leaf):
        self.leafes.append(leaf)
        self.dots += 1



class RTree:
    def __init__(self, cord, h, w, height, dots):
        self.cord = cord
        self.north = (cord[0], cord[1] + h)  # верх
        self.south = (cord[0], cord[1] - h)  # низ
        self.west = (cord[0] - w, cord[1])  # лево
        self.east = (cord[0] + w, cord[1])  # право
        self.height = height
        self.dots = dots
        self.children = [None, None]

    def add(self, leaf):
        if(self.root.dots > 5):
            if self.root.height % 2:
                self.children[0] = RTree(((self.root.cord[0] + self.root.west) / 2, self.root.cord[1]), self.root.w / 2, self.root.h, self.root.height + 1)
                self.children[1] = RTree(((self.root.cord[0] + self.root.east) / 2, self.root.cord[1]), self.root.w / 2, self.root.h, self.root.height + 1)
            else:
                self.children[0] = RTree((self.root.cord[0], (self.root.cord[1] + self.root.north) / 2), self.root.w, self.root.h / 2, self.root.height + 1)
                self.children[1] = RTree((self.root.cord[0], (self.root.cord[1] - self.root.south) / 2), self.root.w, self.root.h / 2, self.root.height + 1)
            if self.root.west < leaf.cord[0] and self.root.east > leaf.cord[0] and self.root.north > leaf.cord[1] and self.root.south < leaf.cord[1]:
                self.children[0].add(leaf)
            else:
                self.children[1].add(leaf)
        else:
            self.leafes[self.dots] = leaf
            self.root.dots += 1



tree = RTree((0, 0), 6371, 6371, 1)

f = open('ukraine_poi.csv')
for line in f:
    info = line.split(';')
    leaf = Leaf(findXY(float(line[0]), float(line[1])), line[2], line[3], line[4], line[5])
    tree.add(leaf)



f.close()