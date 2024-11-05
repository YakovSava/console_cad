import re
import ezdxf

class CADConsole:
    def __init__(self, filename="./console_cad_with_shapes.dxf"):
        # Создаем новый DXF-документ и сохраняем его
        self.doc = ezdxf.new(dxfversion="R2010")
        self.msp = self.doc.modelspace()
        self.filename = filename
        self.thickness = None  # Атрибут для хранения толщины линий

    def execute_command(self, command):
        """
        Обработка команд и вызов соответствующих методов.
        """
        # Команда для создания линии: line (x1, y1) (x2, y2)
        line_pattern = r'line\s+\(([\d\.]+),\s*([\d\.]+)\)\s+\(([\d\.]+),\s*([\d\.]+)\)'
        # Команда для создания прямоугольника: rectangle (x1, y1) (x2, y2)
        rect_pattern = r'rectangle\s+\(([\d\.]+),\s*([\d\.]+)\)\s+\(([\d\.]+),\s*([\d\.]+)\)'
        # Команда для создания круга: circle\s+\(([\d\.]+),\s*([\d\.]+)\)\s+([\d\.]+)
        circle_pattern = r'circle\s+\(([\d\.]+),\s*([\d\.]+)\)\s+([\d\.]+)'
        # Команда для создания полилинии: polyline\s+((?:\([\d\.]+,\s*[\d\.]+\)\s*)+)
        polyline_pattern = r'polyline\s+((?:\([\d\.]+,\s*[\d\.]+\)\s*)+)'
        # Новая команда для установки толщины линий: thick\s+([\d\.]+)
        thick_pattern = r'thick\s+([\d\.]+)'

        # Проверка и обработка команды для установки толщины линий
        match = re.match(thick_pattern, command, re.IGNORECASE)
        if match:
            thickness_value = float(match.group(1))
            if thickness_value > 0:
                self.thickness = thickness_value
                print(f"Thick mode activated with thickness {self.thickness}")
            else:
                self.thickness = None
                print("Thick mode deactivated.")
            return

        # Проверка и обработка команды для линии
        match = re.match(line_pattern, command, re.IGNORECASE)
        if match:
            x1, y1, x2, y2 = map(float, match.groups())
            if self.thickness:
                self.draw_thick_line((x1, y1), (x2, y2), self.thickness)
                print(f"Thick line created from ({x1}, {y1}) to ({x2}, {y2}) with thickness {self.thickness}")
            else:
                self.draw_line((x1, y1), (x2, y2))
                print(f"Line created from ({x1}, {y1}) to ({x2}, {y2})")
            return

        # Проверка и обработка команды для прямоугольника
        match = re.match(rect_pattern, command, re.IGNORECASE)
        if match:
            x1, y1, x2, y2 = map(float, match.groups())
            if self.thickness:
                self.draw_thick_rectangle((x1, y1), (x2, y2), self.thickness)
                print(f"Thick rectangle created from ({x1}, {y1}) to ({x2}, {y2}) with thickness {self.thickness}")
            else:
                self.draw_rectangle((x1, y1), (x2, y2))
                print(f"Rectangle created with corners ({x1}, {y1}) and ({x2}, {y2})")
            return

        # Проверка и обработка команды для круга
        match = re.match(circle_pattern, command, re.IGNORECASE)
        if match:
            x, y, r = map(float, match.groups())
            self.draw_circle((x, y), r)
            print(f"Circle created with center ({x}, {y}) and radius {r}")
            return

        # Проверка и обработка команды для полилинии
        match = re.match(polyline_pattern, command, re.IGNORECASE)
        if match:
            points_str = match.group(1)
            points = re.findall(r'\(([\d\.]+),\s*([\d\.]+)\)', points_str)
            points = [(float(x), float(y)) for x, y in points]
            self.draw_polyline(points)
            print(f"Polyline created with points {points}")
            return

        print("Unknown command:", command)

    def draw_line(self, start, end):
        """
        Метод для рисования линии.
        """
        self.msp.add_line(start, end)

    def draw_thick_line(self, start, end, thickness):
        """
        Метод для рисования толстой линии как прямоугольника.
        thickness: ширина линии
        """
        x1, y1 = start
        x2, y2 = end
        thick = thickness

        # Вычисляем направление линии
        dx = x2 - x1
        dy = y2 - y1
        length = (dx**2 + dy**2) ** 0.5
        if length == 0:
            print("Cannot draw thick line with zero length.")
            return

        # Нормализуем направление
        ux = dx / length
        uy = dy / length

        # Вычисляем перпендикулярное направление для толщины
        px = -uy * (thick / 2)
        py = ux * (thick / 2)

        # Определяем углы прямоугольника
        corner1 = (x1 + px, y1 + py)
        corner2 = (x1 - px, y1 - py)
        corner3 = (x2 - px, y2 - py)
        corner4 = (x2 + px, y2 + py)

        self.msp.add_lwpolyline([
            corner1,
            corner2,
            corner3,
            corner4,
            corner1
        ], close=True)

    def draw_rectangle(self, corner1, corner2):
        """
        Метод для рисования прямоугольника.
        """
        x1, y1 = corner1
        x2, y2 = corner2
        self.msp.add_lwpolyline([
            (x1, y1),
            (x2, y1),
            (x2, y2),
            (x1, y2),
            (x1, y1)
        ], close=True)

    def draw_thick_rectangle(self, corner1, corner2, thickness):
        """
        Метод для рисования толстого прямоугольника как двух прямоугольников:
        - Оригинальный прямоугольник
        - Увеличенный на thickness и сдвинутый
        """
        x1, y1 = corner1
        x2, y2 = corner2
        thick = thickness

        # Оригинальный прямоугольник
        self.msp.add_lwpolyline([
            (x1, y1),
            (x2, y1),
            (x2, y2),
            (x1, y2),
            (x1, y1)
        ], close=True)

        # Увеличенный прямоугольник с сдвигом
        shifted_corner1 = (x1 - thick, y1 - thick)
        shifted_corner2 = (x2 + thick, y2 + thick)
        self.msp.add_lwpolyline([
            shifted_corner1,
            shifted_corner2[0], y1 - thick,
            (shifted_corner2[0], shifted_corner2[1]),
            (shifted_corner1[0], shifted_corner2[1]),
            shifted_corner1
        ], close=True)

        # Альтернативный вариант: увеличиваем размеры обоих сторон
        # shifted_corner1 = (x1 - thick, y1 - thick)
        # shifted_corner2 = (x2 + thick, y2 + thick)
        # self.msp.add_lwpolyline([
        #     shifted_corner1,
        #     (shifted_corner2[0], y1 - thick),
        #     shifted_corner2,
        #     (x1 - thick, shifted_corner2[1]),
        #     shifted_corner1
        # ], close=True)

    def draw_circle(self, center, radius):
        """
        Метод для рисования круга.
        """
        self.msp.add_circle(center, radius)

    def draw_polyline(self, points):
        """
        Метод для рисования полилинии.
        """
        self.msp.add_lwpolyline(points, close=False)

    def save(self):
        """
        Метод для сохранения DXF-файла.
        """
        self.doc.saveas(self.filename)
        print(f"DXF file saved as {self.filename}")