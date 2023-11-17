import sys
import os
import random
import unittest
import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import glTranslatef
from OpenGL.GLU import gluPerspective
# Получаем путь к текущему каталогу скрипта
current_dir = os.path.dirname(os.path.abspath(__file__))
# Добавляем путь к родительскому каталогу
sys.path.append(os.path.join(current_dir, '..'))
from main import draw_electron, draw_nucleus


class TestDrawFunctions(unittest.TestCase):
    """
    Тестирование функций отрисовки электрона и ядра.
    """

    def setUp(self):
        """
        Настройка окружения для тестов.
        """
        pygame.init()
        self.display = (1200, 800)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)

    def tearDown(self):
        """
        Очистка окружения после тестов.
        """
        pygame.quit()

    def test_draw_electron(self):
        """
        Тестирование функции отрисовки электрона.
        """
        electron_angles = random.uniform(0, 360)
        electron_orbit_radii = random.uniform(1.0, 2.5)
        electron_orbit_angles = random.uniform(0, 360)
        electron_diffuse_colors = (0.0, 0.0, 1.0, 1.0)
        self.assertIsNone(draw_electron(electron_angles,
                                        electron_orbit_radii,
                                        electron_orbit_angles,
                                        electron_diffuse_colors))

    def test_draw_nucleus(self):
        """
        Тестирование функции отрисовки ядра.
        """
        self.assertIsNone(draw_nucleus())
