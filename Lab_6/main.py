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
    def __init__(self, cord, R):
        self.cord = cord
        self.R = R




class RTree:
    def __init__(self, maxNodes):
        self.height = 1
        self.maxNodes = maxNodes
    def add(self, x, y, type, subtype, name, adress):
        pass


# f = open('ukraine_poi.csv')
# for line in f:
#     info = line.split(';')
    # print(info)


# f.close()