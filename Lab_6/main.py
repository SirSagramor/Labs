import math
import time
import queue
import cProfile
start_time = time.time()
# x, y - координаты искомой точки, х1, у1 - координаты центра круга, R - радиус
def dotInCircle(x, y, x1, y1, R):
    if ((x - x1) ** 2 + (y - y1) ** 2) <= R ** 2:
        return True
    return False

# x, y - центр круга, R - радиус ,х1, у1 - правый верхний угол прямоугольника, х2, y2 - левый нижний
def circleInRect(x, y, R, x1, y1, x2, y2):
    if  (x > x1 - R and x < x2 + R and y1 > y > y2) or \
        (y > y2 - R and y < y1 + R and x1 > x > x2) or \
        ((x1 - x)**2 + (y1 - y)**2 < R**2) or \
        ((x1 - x)**2 + (y2 - y)**2 < R**2) or \
        ((x2 - x)**2 + (y1 - y)**2 < R**2) or \
        ((x2 - x)**2 + (y2 - y)**2 < R**2):
        return True
    return  False

    # нахождение координат по долготе и широте

# находит координаты по долготе и широте
def findXY(latitude, longitude):
    return 6371 * math.cos(latitude) * math.cos(longitude), 6371 * math.cos(latitude) * math.sin(longitude)

def make_counter():
    i = 0
    def counter(): # counter() is a closure
        nonlocal i
        i += 2
        return i
    return counter
iterator = make_counter()

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
        return 'Node: [x: %f, y: %f, type: %s, subtype: %s, name: %s, adress: %s]' % (self.x, self.y, self.type, self.subtype, self.name, self.adress)

class Node:
    def __init__(self, cord, h, w, depth, n):
        self.x = cord[0]
        self.y = cord[1]
        self.h = h
        self.w = w
        self.depth = depth
        self.n = n
        self.dots = 0
        self.children = [None, None]
        self.divided = False
        self.leafes = []
    def add(self, leaf):
        # если нода разделеная, то находим куда нужно добавить
        if self.divided:
            temp = self
            # тут проверка на то, что нода не начальный корень
            if temp.children[0]:
                while temp.divided:
                    if temp.depth % 2:
                        if temp.x > leaf.x:
                            temp = temp.children[0]
                        else:
                            temp = temp.children[1]
                    else:
                        if temp.y < leaf.y:
                            temp = temp.children[0]
                        else:
                            temp = temp.children[1]
            # если в ноде в которую нужно добавить, больше n точек, делим ее на 2 части, добавляя в эти ноды листья
            if temp.dots == temp.n:
                if temp.depth % 2:
                    temp.leafes.sort(key=lambda x: x.x)
                    mid = (temp.leafes[temp.n // 2 - 1].x + temp.leafes[temp.n // 2].x) / 2
                    temp.children[0] = Node(((mid + temp.x - temp.w) / 2, temp.y), (mid + temp.x - temp.w) / 2 - (temp.x - temp.w), temp.h, temp.depth + 1, temp.n)
                    temp.children[1] = Node(((mid + temp.x + temp.w) / 2, temp.y), (temp.x + temp.w) - (mid + temp.x + temp.w) / 2, temp.h, temp.depth + 1, temp.n)
                    iterator()
                    temp.children[0].leafes = temp.leafes[:temp.n // 2]
                    temp.children[1].leafes = temp.leafes[temp.n // 2:]
                    temp.children[0].dots += temp.n // 2
                    temp.children[1].dots += temp.n // 2
                    if mid > leaf.x:
                        temp.children[0].leafes.append(leaf)
                        temp.children[0].dots += 1
                    else:
                        temp.children[1].leafes.append(leaf)
                        temp.children[1].dots += 1
                else:
                    temp.leafes.sort(key=lambda y: y.y)
                    mid = (temp.leafes[temp.n // 2 - 1].y + temp.leafes[temp.n // 2].y) / 2
                    temp.children[0] = Node((temp.x, (mid + temp.y + temp.h) / 2), temp.w, (temp.y + temp.h) - (mid + temp.y + temp.h) / 2, temp.depth + 1, temp.n)
                    temp.children[1] = Node((temp.x, (mid + temp.y - temp.h) / 2), temp.w, (mid + temp.y - temp.h) / 2 - (temp.y - temp.h), temp.depth + 1, temp.n)
                    iterator()
                    temp.children[0].leafes = temp.leafes[temp.n // 2:]
                    temp.children[1].leafes = temp.leafes[:temp.n // 2]
                    temp.children[0].dots += temp.n // 2
                    temp.children[1].dots += temp.n // 2
                    if mid < leaf.y:
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
        #если в корне меньше n - 1 точек, то просто их добавляем
        elif self.dots < self.n - 1:
            self.leafes.append(leaf)
            self.dots += 1
        # иначе ставим корень деленным и добавляем листок
        else:
            self.leafes.append(leaf)
            self.dots += 1
            self.divided = True

    def findCord(self, cord, R, type):
        x = cord[0]
        y = cord[1]
        out = []
        q = queue.Queue()
        q.put(self)
        while not q.empty():
            temp = q.get()
            if temp.divided:
                if circleInRect(x, y, R, temp.children[0].x + temp.children[0].w, temp.children[0].y + temp.children[0].h,
                                temp.children[0].x - temp.children[0].w, temp.children[0].y - temp.children[0].h):
                    q.put(temp.children[0])
                if circleInRect(x, y, R, temp.children[1].x + temp.children[1].w, temp.children[1].y + temp.children[1].h,
                                temp.children[1].x - temp.children[1].w, temp.children[1].y - temp.children[1].h):
                    q.put(temp.children[1])
            else:
                out += [el for el in temp.leafes if dotInCircle(x, y, el.x, el.y, R) and el.type == type]
        return out

tree = Node((0, -5109), 6372, 1300, 1, 200)
f = open('ukraine_poi.csv')
i = 0
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


out = tree.findCord(findXY(49.94257, 36.31512), 20, "shop")
out.sort(key=lambda x: x.x)
for el in out:
    print(el)

# (50.45130913, 30.45735345)

# Node: (49.94257, 36.31512)[x: 1122.067109, y: -5936.606923, type: shop, subtype: convenience, name: , adress:]
# cProfile.run("tree.add(leaf)")

print("\nКоличество нод:", iterator())
print("Строк всего:", i)
print("Время работы: %s секунд" % (round(time.time() - start_time, 2)))
f.close()
