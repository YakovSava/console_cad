import re
import ezdxf

class CADConsole:
    def __init__(self, filename="./console_cad_with_shapes.dxf"):
        # Создаем новый DXF-документ и сохраняем его
        self.doc = ezdxf.new(dxfversion="R2010")
        self.msp = self.doc.modelspace()
        self.filename = filename

    def execute_command(self, command):
        """
        Обработка команд и вызов соответствующих методов.
        """
        # Команда для создания линии: line (x1, y1) (x2, y2)
        line_pattern = r'line\s+\(([\d\.]+),\s*([\d\.]+)\)\s+\(([\d\.]+),\s*([\d\.]+)\)'
        # Команда для создания прямоугольника: rectangle (x1, y1) (x2, y2)
        rect_pattern = r'rectangle\s+\(([\d\.]+),\s*([\d\.]+)\)\s+\(([\d\.]+),\s*([\d\.]+)\)'
        # Команда для создания круга: circle (x, y) r
        circle_pattern = r'circle\s+\(([\d\.]+),\s*([\d\.]+)\)\s+([\d\.]+)'
        # Команда для создания полилинии: polyline (x1, y1) (x2, y2) ... (xn, yn)
        polyline_pattern = r'polyline\s+((?:\([\d\.]+,\s*[\d\.]+\)\s*)+)'

        # Проверка и обработка команды для линии
        match = re.match(line_pattern, command, re.IGNORECASE)
        if match:
            x1, y1, x2, y2 = map(float, match.groups())
            self.draw_line((x1, y1), (x2, y2))
            print(f"Line created from ({x1}, {y1}) to ({x2}, {y2})")
            return

        # Проверка и обработка команды для прямоугольника
        match = re.match(rect_pattern, command, re.IGNORECASE)
        if match:
            x1, y1, x2, y2 = map(float, match.groups())
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
