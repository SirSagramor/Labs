import math
import time
import queue
import cProfile
start_time = time.time()
# x, y - координаты искомой точки, х1, у1 - координаты центра круга, R - радиус
def dotInCircle(cord, x1, y1, R):
    x, y = cord[0], cord[1]
    if ((x - x1) ** 2 + (y - y1) ** 2) <= R ** 2:
        return True
    return False

# x, y - центр круга, R - радиус ,х1, у1 - правый верхний угол прямоугольника, х2, y2 - левый нижний
def circleInRect(cordCircle, R, topRight, botLeft):
    x, y = cordCircle[0], cordCircle[1]
    x1, y1 = topRight[0], topRight[1]
    x2, y2 = botLeft[0], botLeft[1]
    if  (x1 - R <= x <= x2 + R and y1 >= y >= y2) or \
        (y2 - R <= y <= y1 + R and x1 >= x >= x2) or \
        ((x1 - x)**2 + (y1 - y)**2 <= R**2) or \
        ((x1 - x)**2 + (y2 - y)**2 <= R**2) or \
        ((x2 - x)**2 + (y1 - y)**2 <= R**2) or \
        ((x2 - x)**2 + (y2 - y)**2 <= R**2):
        return True
    return False


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
                    x0 = (mid + temp.x - temp.w) / 2
                    x1 = (mid + temp.x + temp.w) / 2
                    temp.children[0] = Node((x0, temp.y), temp.h, x0 - (temp.x - temp.w), temp.depth + 1, temp.n)
                    temp.children[1] = Node((x1, temp.y), temp.h, (temp.x + temp.w) - x1, temp.depth + 1, temp.n)
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
                    y0 = (mid + temp.y + temp.h) / 2
                    y1 = (mid + temp.y - temp.h) / 2
                    temp.children[0] = Node((temp.x, y0), (temp.y + temp.h) - y0, temp.w, temp.depth + 1, temp.n)
                    temp.children[1] = Node((temp.x, y1), y1 - (temp.y - temp.h), temp.w, temp.depth + 1, temp.n)
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
        out = []
        q = queue.Queue()
        q.put(self)
        while not q.empty():
            temp = q.get()
            if temp.divided:
                # topRightRect0 = (temp.children[0].x + temp.children[0].w, temp.children[0].y + temp.children[0].h)
                # botLeftRect0 = (temp.children[0].x - temp.children[0].w, temp.children[0].y - temp.children[0].h)
                # topRightRect1 = (temp.children[1].x + temp.children[1].w, temp.children[1].y + temp.children[1].h)
                # botLeftRect1 = (temp.children[1].x - temp.children[1].w, temp.children[1].y - temp.children[1].h)
                # if circleInRect(cord, R, topRightRect0, botLeftRect0):
                #     q.put(temp.children[0])
                #     print(topRightRect0, botLeftRect0)
                # if circleInRect(cord, R, topRightRect1, botLeftRect1):
                #     q.put(temp.children[1])
                #     print(topRightRect1, botLeftRect1)
                topRightRect = (temp.x + temp.w, temp.y + temp.h)
                botLeftRect = (temp.x - temp.w, temp.y - temp.h)
                # if circleInRect(cord, R, topRightRect, botLeftRect):
                print(topRightRect, botLeftRect)
                q.put(temp.children[0])
                q.put(temp.children[1])
            else:
                out += [el for el in temp.leafes if dotInCircle(cord, el.x, el.y, R) and el.type == type]
        return out

tree = Node((0, 0), 10000, 10000, 1, 100)
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
        # print(leaf)
    except ValueError:
        print("Value error on line:", i)
    # if i > 200:
    #     break

out = tree.findCord(findXY(50.45130913, 30.45735345), 50, "shop")
out.sort(key=lambda x: x.x)
print("find elements:")
for el in out:
    print(el)

# (50.45130913, 30.45735345)

# Node: (49.94257, 36.31512)[x: 1122.067109, y: -5936.606923, type: shop, subtype: convenience, name: , adress:]
# cProfile.run("tree.add(leaf)") Node: [x: 3435.666632, y: -4923.759551, type: shop, subtype: car, name: Авто Масло, adress: ]

print("\nКоличество нод:", iterator())
print("Строк всего:", i)
print("Время работы: %s секунд" % (round(time.time() - start_time, 2)))
f.close()

# Node: [x: 3573.150127, y: -5148.059406, type: shop, subtype: supermarket, name: Фора, adress: ]
# Node: [x: 3574.227755, y: -5140.278885, type: shop, subtype: supermarket, name: Продукти, adress: ]
# Node: [x: 3579.298595, y: -5139.453265, type: shop, subtype: computer, name: Company, adress: ]
# Node: [x: 3586.101148, y: -5154.274972, type: shop, subtype: convenience, name: , adress: ]
# Node: [x: 3594.112863, y: -5150.394708, type: shop, subtype: hardware, name: AllTels, adress: ]
# Node: [x: 3599.678326, y: -5149.038511, type: shop, subtype: supermarket, name: Сільпо, adress: ]
# Node: [x: 3601.934597, y: -5147.770109, type: shop, subtype: shoes, name: EVA, adress: ]

# Node: [x: 3550.646356, y: -5137.212583, type: shop, subtype: car_repair, name: , adress: ]
# Node: [x: 3552.710863, y: -5110.315536, type: shop, subtype: convenience, name: Канцелярські товари, adress: ]
# Node: [x: 3554.398509, y: -5106.094614, type: shop, subtype: convenience, name: Кумушка, adress: ]
# Node: [x: 3558.222868, y: -5148.835040, type: shop, subtype: travel_agency, name: , adress: ]
# Node: [x: 3558.263484, y: -5148.893812, type: shop, subtype: bicycle, name: Вело Стріт, adress: ]
# Node: [x: 3559.696397, y: -5152.950176, type: shop, subtype: kiosk, name: Кіоск з водою, adress: ]
# Node: [x: 3560.485537, y: -5132.113219, type: shop, subtype: travel_agency, name: "Поехали с нами", adress: Дегтярівська вулиця,50]
# Node: [x: 3560.622807, y: -5153.189203, type: shop, subtype: convenience, name: Подвальчик, adress: ]
# Node: [x: 3561.688080, y: -5148.343551, type: shop, subtype: copyshop, name: Широкоформатний друк, adress: ]
# Node: [x: 3562.719644, y: -5157.106012, type: shop, subtype: bicycle, name: Ель-Капітан, adress: ]
# Node: [x: 3562.885419, y: -5103.144092, type: shop, subtype: bicycle, name: Giant Велоцентр, adress: ]
# Node: [x: 3563.648936, y: -5115.454951, type: shop, subtype: tyres, name: Твоя шина, adress: ]
# Node: [x: 3566.633117, y: -5096.667320, type: shop, subtype: supermarket, name: , adress: ]
# Node: [x: 3566.641969, y: -5113.752353, type: shop, subtype: car_repair, name: АвтоДоктор, adress: ]
# Node: [x: 3567.222797, y: -5113.059383, type: shop, subtype: car_repair, name: , adress: ]
# Node: [x: 3567.350906, y: -5130.717321, type: shop, subtype: convenience, name: Будьмо разом, adress: ]
# Node: [x: 3567.748879, y: -5096.959581, type: shop, subtype: convenience, name: ларёк, adress: ]
# Node: [x: 3570.423320, y: -5148.745913, type: shop, subtype: laundry, name: Clean'OK, adress: ]
# Node: [x: 3570.869095, y: -5162.055813, type: shop, subtype: supermarket, name: АТБ, adress: ]
# Node: [x: 3571.020947, y: -5164.261898, type: shop, subtype: electronics, name: 9В: Радіодеталі, adress: Ушинського вулиця]
# Node: [x: 3571.899731, y: -5110.065256, type: shop, subtype: sports, name: Інтер атлетика, adress: ]
# Node: [x: 3572.184730, y: -5160.427422, type: shop, subtype: kiosk, name: ОККО №02, adress: Чоколівський бульвар,42]
# Node: [x: 3572.634380, y: -5148.305448, type: shop, subtype: photo, name: Принт-центр, adress: ]
# Node: [x: 3572.949825, y: -5148.100522, type: shop, subtype: clothes, name: , adress: ]
# Node: [x: 3573.150127, y: -5148.059406, type: shop, subtype: supermarket, name: Фора, adress: ]
# Node: [x: 3573.209293, y: -5163.010696, type: shop, subtype: mobile_phone, name: Аксессуары к мобильным телефонам, adress: ]
# Node: [x: 3573.582138, y: -5140.885762, type: shop, subtype: mobile_phone, name: Бiлка, adress: ]
# Node: [x: 3573.652736, y: -5148.673629, type: shop, subtype: hairdresser, name: Пора подстричься, adress: ]
# Node: [x: 3574.086381, y: -5166.706727, type: shop, subtype: chemist, name: Динь-Динь, adress: Авіаконструктора Антонова вулиця,43]
# Node: [x: 3574.106759, y: -5126.421523, type: shop, subtype: car_repair, name: Автосервіс Аполлон, adress: Дегтярівська вулиця,27A]
# Node: [x: 3574.227755, y: -5140.278885, type: shop, subtype: supermarket, name: Продукти, adress: ]
# Node: [x: 3574.319155, y: -5162.517947, type: shop, subtype: pawnbroker, name: Скарбниця, adress: ]
# Node: [x: 3574.567507, y: -5162.214818, type: shop, subtype: electronics, name: Експерт, adress: Ушинського вулиця,3]
# Node: [x: 3574.976801, y: -5161.813253, type: shop, subtype: mobile_phone, name: Vodafone, adress: ]
# Node: [x: 3575.264345, y: -5161.456488, type: shop, subtype: electronics, name: Міленіум, adress: ]
# Node: [x: 3575.411648, y: -5161.117828, type: shop, subtype: convenience, name: Колосок, adress: ]
# Node: [x: 3575.886942, y: -5160.591142, type: shop, subtype: mobile_phone, name: Мир мобильних аксесуарів, adress: ]
# Node: [x: 3575.897070, y: -5165.569556, type: shop, subtype: convenience, name: Продуктовый магазин, adress: Авіаконструктора Антонова вулиця,43]
# Node: [x: 3575.963198, y: -5160.590956, type: shop, subtype: mobile_phone, name: , adress: ]
# Node: [x: 3576.219616, y: -5160.189388, type: shop, subtype: electronics, name: Радиомаг, adress: ]
# Node: [x: 3576.493414, y: -5106.082148, type: shop, subtype: sports, name: Все для хоккея, adress: ]
# Node: [x: 3576.643424, y: -5145.619041, type: shop, subtype: florist, name: , adress: Борщагівська вулиця]
# Node: [x: 3577.385757, y: -5146.247768, type: shop, subtype: computer, name: б/в ком'ютори, adress: ]
# Node: [x: 3578.051432, y: -5145.338796, type: shop, subtype: bakery, name: Киевхлеб, adress: ]
# Node: [x: 3578.721390, y: -5162.916970, type: shop, subtype: stationery, name: Петрик П'яточкин, adress: ]
# Node: [x: 3578.821608, y: -5135.263582, type: shop, subtype: florist, name: , adress: ]
# Node: [x: 3579.298595, y: -5139.453265, type: shop, subtype: computer, name: Company, adress: ]
# Node: [x: 3579.930988, y: -5145.187148, type: shop, subtype: convenience, name: Олександіївський, adress: ]
# Node: [x: 3580.753018, y: -5139.349596, type: shop, subtype: hairdresser, name: , adress: ]
# Node: [x: 3582.697922, y: -5155.099424, type: shop, subtype: car_parts, name: База автозвука, adress: ]
# Node: [x: 3584.593992, y: -5153.317804, type: shop, subtype: florist, name: , adress: ]
# Node: [x: 3584.970103, y: -5151.660283, type: shop, subtype: stationery, name: Папірус, adress: ]
# Node: [x: 3585.105747, y: -5130.269127, type: shop, subtype: convenience, name: AMIC, adress: ]
# Node: [x: 3585.302801, y: -5140.288630, type: shop, subtype: copyshop, name: , adress: ]
# Node: [x: 3585.313631, y: -5151.714402, type: shop, subtype: hairdresser, name: Anti barber, adress: ]
# Node: [x: 3585.469322, y: -5166.359884, type: shop, subtype: clothes, name: ЭкономЪка, adress: ]
# Node: [x: 3585.765412, y: -5139.965932, type: shop, subtype: florist, name: , adress: ]
# Node: [x: 3586.101148, y: -5154.274972, type: shop, subtype: convenience, name: , adress: ]
# Node: [x: 3586.339607, y: -5143.419189, type: shop, subtype: car_repair, name: Автомийка, adress: ]
# Node: [x: 3586.997384, y: -5153.913923, type: shop, subtype: pawnbroker, name: , adress: ]
# Node: [x: 3587.068091, y: -5104.975131, type: shop, subtype: computer, name: Інтернет-магазин "Репка.юа", adress: ]
# Node: [x: 3587.544727, y: -5168.467577, type: shop, subtype: hardware, name: , adress: ]
# Node: [x: 3587.558979, y: -5160.331907, type: shop, subtype: convenience, name: , adress: Мартиросяна вулиця,19]
# Node: [x: 3588.467803, y: -5153.937844, type: shop, subtype: hairdresser, name: , adress: ]
# Node: [x: 3588.694858, y: -5153.714416, type: shop, subtype: convenience, name: , adress: ]
# Node: [x: 3590.564764, y: -5165.316638, type: shop, subtype: supermarket, name: ЛотОК, adress: ]
# Node: [x: 3591.495354, y: -5160.046583, type: shop, subtype: car_parts, name: Лангис, adress: ]
# Node: [x: 3592.775735, y: -5160.895470, type: shop, subtype: electronics, name: MUK Express, adress: ]
# Node: [x: 3593.264001, y: -5135.159724, type: shop, subtype: electronics, name: Сет Украина, adress: Борщагівська вулиця,99]
# Node: [x: 3593.325363, y: -5169.287983, type: shop, subtype: supermarket, name: Фуршет, adress: ]
# Node: [x: 3593.790838, y: -5152.348216, type: shop, subtype: supermarket, name: АТБ, adress: ]
# Node: [x: 3594.112863, y: -5150.394708, type: shop, subtype: hardware, name: AllTels, adress: ]
# Node: [x: 3594.675822, y: -5152.738436, type: shop, subtype: hairdresser, name: , adress: Чоколівський бульвар,5]
# Node: [x: 3596.244800, y: -5130.785940, type: shop, subtype: books, name: Технічна книга, adress: ]
# Node: [x: 3596.586219, y: -5158.664318, type: shop, subtype: newsagent, name: Союздрук, adress: ]
# Node: [x: 3597.232977, y: -5153.987223, type: shop, subtype: supermarket, name: Fiducia Африканский магазин, adress: Мартиросяна вулиця,16/14]
# Node: [x: 3597.294434, y: -5152.208813, type: shop, subtype: electronics, name: Фокстрот, adress: ]
# Node: [x: 3597.541759, y: -5149.600324, type: shop, subtype: electronics, name: VOLIA, adress: Чоколівський бульвар,30]
# Node: [x: 3598.272383, y: -5149.439533, type: shop, subtype: clothes, name: , adress: ]
# Node: [x: 3598.448730, y: -5142.788219, type: shop, subtype: supermarket, name: Лоток, adress: ]
# Node: [x: 3599.678326, y: -5149.038511, type: shop, subtype: supermarket, name: Сільпо, adress: ]
# Node: [x: 3600.796402, y: -5149.979781, type: shop, subtype: florist, name: , adress: ]
# Node: [x: 3601.592607, y: -5150.241128, type: shop, subtype: chemist, name: , adress: Київ, Чоколівський бульвар, 19]
# Node: [x: 3601.934597, y: -5147.770109, type: shop, subtype: shoes, name: EVA, adress: ]
# Node: [x: 3603.687443, y: -5154.004894, type: shop, subtype: supermarket, name: ЛотОК, adress: ]
# Node: [x: 3603.690905, y: -5151.486431, type: shop, subtype: convenience, name: , adress: ]
# Node: [x: 3603.751078, y: -5147.078227, type: shop, subtype: pet, name: Зоомаркет, adress: ]
# Node: [x: 3604.241692, y: -5146.464384, type: shop, subtype: bakery, name: Грузинський хліб, adress: ]
# Node: [x: 3604.430169, y: -5172.340181, type: shop, subtype: car_repair, name: СТО "IBSERVICE", adress: Народного Ополчення вулиця,18Б]
# Node: [x: 3604.611473, y: -5090.559069, type: shop, subtype: supermarket, name: Сильпо, adress: ]
# Node: [x: 3605.198893, y: -5157.813862, type: shop, subtype: supermarket, name: Billa, adress: ]
# Node: [x: 3605.930715, y: -5145.152226, type: shop, subtype: erotic, name: "Насолода", adress: ]
# Node: [x: 3606.334931, y: -5146.166951, type: shop, subtype: hairdresser, name: , adress: ]
# Node: [x: 3606.603535, y: -5136.925777, type: shop, subtype: copyshop, name: , adress: ]
# Node: [x: 3607.326648, y: -5136.644894, type: shop, subtype: convenience, name: Маленька кишенька, adress: ]
# Node: [x: 3608.159764, y: -5149.099626, type: shop, subtype: doityourself, name: , adress: Мартиросяна вулиця,6]
# Node: [x: 3608.338303, y: -5087.727174, type: shop, subtype: supermarket, name: Сільпо, adress: ]
# Node: [x: 3608.380302, y: -5156.762539, type: shop, subtype: supermarket, name: Лоток, adress: ]
# Node: [x: 3608.525248, y: -5148.416072, type: shop, subtype: hairdresser, name: Валерія, adress: Мартиросяна вулиця,8]
# Node: [x: 3609.249111, y: -5144.302891, type: shop, subtype: photo, name: Ірина, adress: ]
# Node: [x: 3609.404447, y: -5154.713818, type: shop, subtype: hardware, name: Добрий господар, adress: ]
# Node: [x: 3610.355215, y: -5103.105610, type: shop, subtype: car, name: , adress: ]
# Node: [x: 3610.916747, y: -5137.604899, type: shop, subtype: supermarket, name: Лоток, adress: ]
# Node: [x: 3611.439713, y: -5136.710983, type: shop, subtype: hairdresser, name: , adress: ]
# Node: [x: 3611.709597, y: -5142.011290, type: shop, subtype: convenience, name: Bud, adress: ]
# Node: [x: 3612.088966, y: -5145.614021, type: shop, subtype: yes, name: Двері Білорусії, adress: ]
# Node: [x: 3612.203748, y: -5102.038369, type: shop, subtype: car, name: АиС, adress: ]
# Node: [x: 3612.245196, y: -5135.564132, type: shop, subtype: convenience, name: Еко-лавка, adress: ]
# Node: [x: 3614.252510, y: -5128.276137, type: shop, subtype: kiosk, name: , adress: ]
# Node: [x: 3615.815309, y: -5139.984394, type: shop, subtype: hairdresser, name: Fleur, adress: ]
# Node: [x: 3616.293548, y: -5143.942790, type: shop, subtype: florist, name: , adress: ]
# Node: [x: 3616.404813, y: -5133.401086, type: shop, subtype: greengrocer, name: , adress: ]
# Node: [x: 3616.618056, y: -5133.158630, type: shop, subtype: greengrocer, name: , adress: ]
# Node: [x: 3616.622656, y: -5153.277857, type: shop, subtype: beauty, name: Jazz, adress: ]
# Node: [x: 3616.820504, y: -5132.791854, type: shop, subtype: greengrocer, name: , adress: ]
# Node: [x: 3617.078761, y: -5132.504307, type: shop, subtype: florist, name: , adress: ]
# Node: [x: 3617.162765, y: -5132.405508, type: shop, subtype: greengrocer, name: , adress: ]
# Node: [x: 3617.270832, y: -5143.255602, type: shop, subtype: florist, name: , adress: ]
# Node: [x: 3618.072484, y: -5131.407512, type: shop, subtype: newsagent, name: , adress: ]
# Node: [x: 3618.549685, y: -5130.885804, type: shop, subtype: coffee, name: , adress: ]
# Node: [x: 3618.691025, y: -5142.870069, type: shop, subtype: confectionery, name: Roshen, adress: Чоколівський бульвар,3]
# Node: [x: 3618.707931, y: -5145.627009, type: shop, subtype: beauty, name: Brilace.kiev.ua, adress: ]
# Node: [x: 3619.152821, y: -5145.166089, type: shop, subtype: bakery, name: Чудо пекар, adress: ]
# Node: [x: 3619.154376, y: -5145.386981, type: shop, subtype: florist, name: , adress: ]
# Node: [x: 3619.175783, y: -5130.139563, type: shop, subtype: tobacco, name: , adress: ]
# Node: [x: 3619.582025, y: -5130.170828, type: shop, subtype: supermarket, name: Еко-маркет, adress: ]
# Node: [x: 3619.899357, y: -5089.022577, type: shop, subtype: beauty, name: Кабинет депиляции, adress: Сім’ї Хохлових вулиця,8]
# Node: [x: 3619.932188, y: -5136.225976, type: shop, subtype: bakery, name: Батоша, adress: ]
# Node: [x: 3621.417959, y: -5140.298770, type: shop, subtype: supermarket, name: Сільпо, adress: Чоколівський бульвар,6]
# Node: [x: 3621.613067, y: -5142.432256, type: shop, subtype: chemist, name: Космо, adress: ]
# Node: [x: 3622.128245, y: -5095.283792, type: shop, subtype: tailor, name: , adress: Зоологічна вулиця,4]
# Node: [x: 3622.128785, y: -5135.306531, type: shop, subtype: bicycle, name: MOTOstyle.ua, adress: ]
# Node: [x: 3623.034707, y: -5126.897259, type: shop, subtype: clothes, name: Модный карапуз, adress: ]
# Node: [x: 3623.210289, y: -5093.245898, type: shop, subtype: convenience, name: Крамниця, adress: Зоологічна вулиця]
# Node: [x: 3623.866097, y: -5092.658199, type: shop, subtype: car_parts, name: Формула 1, adress: Зоологічна вулиця]
# Node: [x: 3624.306463, y: -5133.923735, type: shop, subtype: hairdresser, name: , adress: ]
# Node: [x: 3626.101059, y: -5142.029885, type: shop, subtype: yes, name: Сонька, adress: ]
# Node: [x: 3626.272892, y: -5090.004080, type: shop, subtype: convenience, name: Укрмаркет, adress: ]
# Node: [x: 3626.302377, y: -5135.442903, type: shop, subtype: doityourself, name: SkloBanka, adress: Левка Мацієвича вулиця,3]
# Node: [x: 3627.806022, y: -5138.226577, type: shop, subtype: copyshop, name: Фото, adress: ]
# Node: [x: 3628.341122, y: -5136.803696, type: shop, subtype: pawnbroker, name: Єв.ро.фінанс, adress: ]
# Node: [x: 3629.891202, y: -5130.936662, type: shop, subtype: supermarket, name: Фора, adress: ]
# Node: [x: 3630.279110, y: -5147.298846, type: shop, subtype: supermarket, name: АТБ маркет, adress: Федора Ернста вулиця,4]
# Node: [x: 3630.354413, y: -5147.514906, type: shop, subtype: bakery, name: , adress: ]
# Node: [x: 3630.803132, y: -5134.839062, type: shop, subtype: e-cigarette, name: Vape Shop Vapingman, adress: Повітрофлотський проспект,46]
# Node: [x: 3631.298928, y: -5134.450971, type: shop, subtype: convenience, name: Еко-Лавка, adress: ]
# Node: [x: 3631.773454, y: -5146.139133, type: shop, subtype: hairdresser, name: , adress: ]
# Node: [x: 3632.688811, y: -5145.797547, type: shop, subtype: sports, name: Спортивний клуб "Жаклін", adress: ]
# Node: [x: 3632.693430, y: -5133.264376, type: shop, subtype: cosmetics, name: Watsons, adress: Повітрофлотський проспект,44]
# Node: [x: 3633.757691, y: -5118.034726, type: shop, subtype: supermarket, name: Дінь Дінь, adress: Єреванська вулиця,30]
# Node: [x: 3634.178283, y: -5131.987904, type: shop, subtype: hairdresser, name: Салон красоты Лакмусс, adress: Повітрофлотський проспект,42]
# Node: [x: 3634.438530, y: -5132.028963, type: shop, subtype: florist, name: , adress: ]
# Node: [x: 3634.796475, y: -5144.414310, type: shop, subtype: florist, name: , adress: ]
# Node: [x: 3634.839261, y: -5127.048813, type: shop, subtype: convenience, name: Харчі, adress: ]
# Node: [x: 3636.795448, y: -5152.489539, type: shop, subtype: kiosk, name: , adress: ]
# Node: [x: 3637.594956, y: -5096.400048, type: shop, subtype: bakery, name: Crepier, adress: ]
# Node: [x: 3637.849192, y: -5100.206937, type: shop, subtype: supermarket, name: АТБ, adress: ]
# Node: [x: 3638.220170, y: -5095.982650, type: shop, subtype: coffee, name: Coffee nerds, adress: ]
# Node: [x: 3639.049154, y: -5095.419615, type: shop, subtype: bakery, name: Farmajo, adress: ]
# Node: [x: 3642.571366, y: -5141.550487, type: shop, subtype: car_repair, name: , adress: ]
# Node: [x: 3644.319384, y: -5121.618261, type: shop, subtype: doityourself, name: Флора-Техно, adress: Авіаконструктора Антонова вулиця,5а]
# Node: [x: 3645.707385, y: -5123.351997, type: shop, subtype: pawnbroker, name: Сейф, adress: ]
# Node: [x: 3646.934607, y: -5125.944665, type: shop, subtype: convenience, name: , adress: ]
# Node: [x: 3647.743520, y: -5121.550001, type: shop, subtype: books, name: Книгарня «Є», adress: ]
# Node: [x: 3648.039374, y: -5120.556518, type: shop, subtype: houseware, name: Посуд de Luxe, adress: ]