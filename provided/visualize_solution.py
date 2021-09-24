# Author: Okorie Rehoboth
# Sept 23 2021
import math
import cs1lib
from provided import SearchSolution
from provided.FoxProblem import FoxProblem
from provided.uninformed_search import bfs_search


def draw_animal(coord, r=5):
    cs1lib.draw_circle(coord[0], coord[1], r)


def calculate_animal_coords(animal_list: list, x_extreme: int, y_extreme: int, lines: int, animals: int):
    for y in range(1, lines + 1):
        for x in range(1, min(12, animals) + 1):
            xc = x * 15 + x_extreme if x_extreme > 0 else -x_extreme - x * 15
            yc = y * 15 + y_extreme if y_extreme > 0 else -y_extreme - y * 15
            animal_list.append((xc, yc))
            animals -= 1


def solution_visualizer(solution: SearchSolution):
    path = solution.path
    foxes_total_number = path[0][0]
    chicken_total_number = path[0][1]

    def draw_animals(fx, ch):
        cs1lib.set_fill_color(1, 0, 0)
        for f in fx:
            draw_animal(f)

        cs1lib.set_fill_color(.5, .5, .2)
        for c in ch:
            draw_animal(c)

    def draw_setting():
        cs1lib.set_fill_color(0, 1, 0)
        cs1lib.draw_rectangle(100, 200, 200, 400)
        cs1lib.set_fill_color(.1, .2, 1)
        cs1lib.draw_rectangle(300, 200, 200, 400)
        cs1lib.set_fill_color(0, 1, 0)
        cs1lib.draw_rectangle(500, 200, 200, 400)

    state_count = 0

    def draw():
        nonlocal state_count
        state = solution.path[state_count]
        cs1lib.clear()
        draw_setting()
        foxes, chickens = list(), list()
        fb1, fb2 = state[0], foxes_total_number - state[0]
        cb1, cb2 = state[1], chicken_total_number - state[1]
        fox_lines = math.ceil(fb1 / 12)
        chicken_lines = math.ceil(cb1 / 12)
        calculate_animal_coords(foxes, 100, 200, fox_lines, fb1)
        calculate_animal_coords(chickens, 100, -600, chicken_lines, cb1)
        draw_animals(foxes, chickens)
        fox_lines = math.ceil(fb2 / 12)
        chicken_lines = math.ceil(cb2 / 12)
        foxes, chickens = list(), list()
        calculate_animal_coords(foxes, 500, 200, fox_lines, fb2)
        calculate_animal_coords(chickens, 500, -600, chicken_lines, cb2)
        draw_animals(foxes, chickens)
        state_count += 1
        if state_count > len(solution.path):
            cs1lib.cs1_quit()
    cs1lib.start_graphics(draw, width=800, height=800, framerate=1)


problem331 = FoxProblem((3, 3, 1), boat_capacity=2)
sol = bfs_search(problem331)
print(sol)
solution_visualizer(sol)
