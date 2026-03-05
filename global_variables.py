import pygame
import math as m
import random as r
import sympy as sp
arcp = 2000  # lines per arc
arcw = 0.15  # arc width  |  ratio offset on both sides
sd = 750
screen_dimensions = (sd, sd)
fps = 60
bg = 0
bg_color = (bg, bg, bg)
title = "R26#3"

inner_color = True  # should the inner parts of the tracks be filled? Should generally set to true
fill_types = ["black fill", "multicolor"]
fill_type = fill_types[0]

fill_colors = [(184, 205, 229), (152, 193, 217)]

pygame.init()
pygame.display.set_caption(title)
clock = pygame.time.Clock()
text_stuff = pygame.font.Font(None, 50)
screen = pygame.display.set_mode(screen_dimensions)


# Used for unit value direction conversion
def unit(letter):
    if letter == "R":
        return 1
    else:
        return -1


def count(word):
    running_count = 0
    for letter in word:
        running_count += unit(letter)
    return running_count % 8


def string(list_word):
    string_word = ""
    for letter in list_word:
        string_word += letter
    return string_word


def invert_flip(word):
    new_word = ""
    for i in range(len(word)):
        if word[len(word)-i-1] == "R":
            new_word += "L"
        else:
            new_word += "R"
    return new_word


def c_replacement(word):
    new_word = ""
    for letter in word:
        if letter == "R":
            new_word += "RR"
        else:
            new_word += "LL"
    return new_word


def middle(word, i, j):
    if i < j:
        return word[i + 2:j]
    elif j < i:
        new_word = word[:j]
        for letter in word[i+2:len(word)]:
            new_word += letter
        return new_word


# Unused test function
def draw_arc_color(center, radius, start_angle, arc_color, straight_color):
    angle = start_angle
    dth = m.pi/(4*arcp)
    points = []
    points2 = []
    for i in range(arcp):
        points.append((center[0] + (radius * m.cos(angle) * (1+arcw)), center[1] - (radius * m.sin(angle) * (1+arcw))))
        points2.append((center[0] + (radius * m.cos(angle) * (1-arcw)), center[1] - (radius * m.sin(angle) * (1-arcw))))
        angle -= dth

    pygame.draw.lines(screen, arc_color, False, points, 4)
    pygame.draw.lines(screen, arc_color, False, points2, 4)

    pygame.draw.line(screen, straight_color, points[0], points2[0], 2)
    pygame.draw.line(screen, straight_color, points[arcp-1], points2[arcp-1], 2)


def draw_arc(center, radius, start_angle, direction, filling_color):
    angle = start_angle
    dth = m.pi/(4*arcp)
    points = []
    points2 = []
    pointsc = []
    for i in range(arcp):
        points.append((center[0] + (radius * m.cos(angle) * (1+arcw)), center[1] - (radius * m.sin(angle) * (1+arcw))))
        points2.append((center[0] + (radius * m.cos(angle) * (1-arcw)), center[1] - (radius * m.sin(angle) * (1-arcw))))
        pointsc.append((center[0] + (radius * m.cos(angle)), center[1] - (radius * m.sin(angle))))
        angle -= unit(direction)*dth

    if inner_color:
        if fill_type == "black fill":
            pygame.draw.lines(screen, "black", False, pointsc, round(radius * (1 + arcw) * 0.3))
        elif fill_type == "multicolor":
            pygame.draw.lines(screen, fill_colors[filling_color], False, pointsc, round(radius * (1 + arcw) * 8))

    pygame.draw.lines(screen, "white", False, points, 5)
    pygame.draw.lines(screen, "white", False, points2, 5)

    pygame.draw.line(screen, "white", points[0], points2[0], 4)
    pygame.draw.line(screen, "white", points[arcp-1], points2[arcp-1], 2)


def calc_ideal_d_answers(search_size):
    choices = []
    gaps = []
    for i in range(1, search_size):
        new_gap = abs(((2 ** 0.5) * i)-m.floor((2 ** 0.5) * i))
        if not gaps:
            choices.append(i)
            gaps.append(new_gap)
        elif abs(((2 ** 0.5) * i)-m.floor((2 ** 0.5) * i)) < gaps[len(gaps)-1]:
            choices.append(i)
            gaps.append(new_gap)
    results = []
    for i in range(len(gaps)):
        results.append((choices[i], gaps[i]))
    return results


def R(theta):
    return sp.Matrix([
        [sp.cos(theta), -sp.sin(theta)],
        [sp.sin(theta), sp.cos(theta)]
    ])


def part_d_matrix(l, u):
    return (l*R(m.pi/4)) + (l*R(3*m.pi/4)) + (u*R(6*m.pi/4))


lr_vec = sp.Matrix([
        [1.4142135623731065], [0.5857864376268935]
    ])
