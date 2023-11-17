import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, \
    glEnable, GL_LIGHTING, GL_LIGHT0, GL_POSITION, GL_SPOT_DIRECTION, GL_DIFFUSE, GL_SPECULAR, GL_SHININESS, \
    glLoadIdentity, glTranslatef, glRotatef, glPushMatrix, glPopMatrix, glClearDepth, glDepthFunc, GL_LESS, \
    glMaterialfv, GL_FRONT_AND_BACK, GL_EMISSION, glLightfv, GL_DEPTH_TEST, glGetDoublev, GL_MODELVIEW_MATRIX
from OpenGL.GLU import gluNewQuadric, gluSphere, gluPerspective
import random

# Количество электронов
NUM_ELECTRONS = 6

# Параметры ядра
NUCLEUS_RADIUS = 0.8
NUCLEUS_COLOR = (1.0, 0.0, 0.0, 1.0)

# Параметры электрона
ELECTRON_RADIUS = 0.2
ELECTRON_SPEED = 2.0

# Цвета для диффузного отражения электронов
ELECTRON_DIFFUSE_COLORS = [(0.0, 0.0, 1.0, 1.0) for _ in range(NUM_ELECTRONS)]

# Углы поворота электронов
ELECTRON_ANGLES = [random.uniform(0, 360) for _ in range(NUM_ELECTRONS)]
# Радиусы орбит электронов
ELECTRON_ORBIT_RADII = [random.uniform(1.0, 2.5) for _ in range(NUM_ELECTRONS)]
# Углы наклона орбит электронов
ELECTRON_ORBIT_ANGLES = [random.uniform(0, 360) for _ in range(NUM_ELECTRONS)]

# Константы для размеров окна
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Границы окна
WINDOW_X_LIMIT = WINDOW_WIDTH / 2
WINDOW_Y_LIMIT = WINDOW_HEIGHT / 2


def init():
    """
    Инициализирует OpenGL, устанавливая освещение и материалы для отображения трехмерной модели атома.

    Освещение:
    - Включает освещение и источник света GL_LIGHT0.
    - Устанавливает позицию и направление света.

    Основные параметры:
    - position: Позиция светового источника в пространстве (x, y, z, w).
    - spot_direction: Направление светового пятна.

    Трансформации:
    - Устанавливает матрицу проекции, перспективу и перемещение взгляда камеры.

    Глубина:
    - Включает тест глубины и устанавливает параметры теста.

    Материалы:
    - Устанавливает диффузное отражение, зеркальность и блеск материала атома.

    :return: Нет возвращаемых значений.
    """
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_BUFFER_BIT)

    # Позиция светового источника
    position = [0.0, 0.0, 5.0, 1.0]
    # Направление светового пятна
    spot_direction = [0.0, 0.0, -1.0]

    glLoadIdentity()
    gluPerspective(45, (WINDOW_WIDTH / WINDOW_HEIGHT), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    # Настройка теста глубины
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)

    # Установка позиции и направления светового источника
    glLightfv(GL_LIGHT0, GL_POSITION, position)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, spot_direction)

    # Установка свойств материала атома
    material_diffuse = [0.8, 0.8, 0.8, 1.0]
    material_specular = [1.0, 1.0, 1.0, 1.0]
    material_shininess = [50.0]

    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, material_specular)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, material_shininess)


def draw_nucleus():
    """
    Отрисовывает ядро атома с эмиссионным свечением.

    Использует библиотеку OpenGL для создания сферы, представляющей ядро атома.
    Устанавливает цвет эмиссии для создания свечения ядра.

    :return: Нет возвращаемых значений.
    """
    # Устанавливает цвет эмиссии для свечения ядра
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, NUCLEUS_COLOR)

    # Создает квадрику для отрисовки сферы
    quadric = gluNewQuadric()

    # Рисует сферу с указанными параметрами
    gluSphere(quadric, NUCLEUS_RADIUS, 20, 20)

    # Сбрасывает цвет эмиссии после отрисовки
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])


def draw_electron(angle, orbit_radius, orbit_angle, electron_diffuse_color):
    """
    Отрисовывает электрон, представленный сферой, с учетом его орбитального положения и цвета диффузного отражения.

    :param angle: Угол поворота электрона вокруг своей оси.
    :param orbit_radius: Радиус орбиты электрона.
    :param orbit_angle: Угол наклона орбиты электрона.
    :param electron_diffuse_color: Цвет диффузного отражения для электрона.
    :return: Нет возвращаемых значений.
    """
    # Сохраняет текущую матрицу модели-вида
    glPushMatrix()

    # Поворачивает и транслирует для установки положения электрона
    glRotatef(orbit_angle, 0.0, 0.0, 1.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glTranslatef(orbit_radius, 0.0, 0.0)

    # Проверяет границы перед движением
    new_pos = glGetDoublev(GL_MODELVIEW_MATRIX)
    electron_x = new_pos[3][0]
    electron_y = new_pos[3][1]

    if abs(electron_x) > WINDOW_X_LIMIT or abs(electron_y) > WINDOW_Y_LIMIT:
        # Возвращает предыдущую матрицу, чтобы отменить движение
        glPopMatrix()
    else:
        # Устанавливает цвет диффузного отражения для электрона
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, electron_diffuse_color)

        # Создает квадрику для отрисовки сферы
        quadric = gluNewQuadric()

        # Рисует сферу с указанными параметрами
        gluSphere(quadric, ELECTRON_RADIUS, 10, 10)

    # Восстанавливает предыдущую матрицу модели-вида
    glPopMatrix()


def draw():
    """
    Осуществляет отрисовку сцены, включая ядро и электроны.

    :return: Нет возвращаемых значений.
    """
    # Очищает буферы цвета и глубины
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Устанавливает единичную матрицу проекции
    glLoadIdentity()
    gluPerspective(45, (WINDOW_WIDTH / WINDOW_HEIGHT), 0.1, 50.0)

    # Транслирует вглубь экрана
    glTranslatef(0.0, 0.0, -5)

    # Отрисовывает ядро
    draw_nucleus()

    # Отрисовывает электроны
    for i in range(NUM_ELECTRONS):
        draw_electron(
            ELECTRON_ANGLES[i],
            ELECTRON_ORBIT_RADII[i],
            ELECTRON_ORBIT_ANGLES[i],
            ELECTRON_DIFFUSE_COLORS[i]
        )
        ELECTRON_ANGLES[i] += ELECTRON_SPEED

    # Обновляет дисплей и ожидает 10 миллисекунд для контроля частоты кадров
    pygame.display.flip()
    pygame.time.wait(10)


def main():
    """
    Основная функция программы, инициализирует Pygame, устанавливает режим отображения,
    и запускает бесконечный цикл для отрисовки сцены.

    :return: Нет возвращаемых значений.
    """
    # Инициализирует Pygame
    pygame.init()

    # Устанавливает размеры окна
    display = (WINDOW_WIDTH, WINDOW_HEIGHT)

    # Устанавливает режим отображения с двойным буфером и использованием OpenGL
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Инициализирует OpenGL
    init()

    # Бесконечный цикл для отрисовки сцены
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Завершает программу при закрытии окна
                pygame.quit()
                quit()

        # Осуществляет отрисовку сцены
        draw()


if __name__ == "__main__":
    main()
