import copy

from global_variables import *


class Track:
    def __init__(self, word, origin, radius):
        self.word = word
        self.origin = origin
        self.radius = radius
        self.final_point = ()
        self.final_pivot = ()

    def display(self):
        """ For this function, the "angle" will represent the angle that the vector pointing
        from the track to the pivot makes with the horizontal (flipping when letter changes) (e.x. the starting angle would be a right angle)

        This is not the same way its defined in the paper I wrote. """

        angle = m.pi/2
        active_point = self.origin
        pivot = (self.origin[0], self.origin[1]+self.radius)
        previous_letter = "R"
        filling_color = 0
        for letter in self.word:
            '''test_color = round(255 - abs((4 * angle)))  # Use to check pivot and point positions
            pygame.draw.circle(screen, (test_color, 0, 0), pivot, 10)'''''
            if letter == previous_letter:
                draw_arc(pivot, self.radius, angle, letter, filling_color)
                angle -= unit(letter)*(m.pi/4)
                active_point = (pivot[0]+(self.radius*m.cos(angle)), pivot[1]-(self.radius*m.sin(angle)))
            else:
                # Move the pivot to the other side of the active point such that the rotation goes the other way
                pivot = ((2*active_point[0])-pivot[0], (2*active_point[1])-pivot[1])
                angle = m.pi+angle
                draw_arc(pivot, self.radius, angle, letter, filling_color)
                angle -= unit(letter)*(m.pi/4)
                active_point = (pivot[0] + (self.radius * m.cos(angle)), pivot[1] - (self.radius * m.sin(angle)))
                previous_letter = letter
            if fill_type == fill_types[1]:
                print(filling_color, (filling_color + 1) % 2)
                filling_color = (filling_color + 1) % 2
        self.final_point = active_point
        self.final_pivot = pivot

    def show_points(self, end=True):
        if end:
            pygame.draw.circle(screen, "dark red", self.final_point, 10 * self.radius / 115)
        pygame.draw.circle(screen, "red", self.origin, 10 * self.radius / 115)

    def show_pdf_angle(self):
        pygame.draw.circle(screen, (0, 200, 250), self.final_point, 10*self.radius/115)
        pygame.draw.line(screen, (0, 150, 150), self.final_point, (self.final_point[0]+self.radius, self.final_point[1]), 6)
        count = 0
        for letter in self.word:
            count -= unit(letter)
        end_point = (self.final_point[0]+(self.radius*m.cos(count*m.pi/4)),
                     self.final_point[1]-(self.radius*m.sin(count*m.pi/4)))
        pygame.draw.line(screen, (0, 205, 210), self.final_point,
                         end_point, 6)
        dr = 30
        rect = pygame.Rect(self.final_point[0]-dr, self.final_point[1]-dr,
                           2*dr, 2*dr)
        count = (count+128) % 8
        if count <= 4:
            pygame.draw.arc(screen, (0, 190, 180), rect, 0, count*m.pi/4, 3)
        else:
            pygame.draw.arc(screen, (0, 190, 180), rect,  count*m.pi/4, 0, 3)

    def add_piece_random(self, wait_time=0.5):
        if wait_time != 0:
            clock.tick(1/wait_time)
        self.word += r.choice(["R", "L"])
        print(self.word)

    def set_part_d_word(self, l, u):
        new_word = "L"
        for i in range(l):
            new_word += "LR"
        new_word += "LL"
        for i in range(l):
            new_word += "LR"
        new_word += "LLL"
        for i in range(u):
            new_word += "LR"
        new_word += "LL"
        self.word = copy.deepcopy(new_word)

    def attempt_reduction(self):
        # Only checks for LR and RL omission with reductions -- some closed loops won't apply
        # This was for an earlier attempt at solving Part (b)
        LRs = []
        RLs = []
        for i in range(len(self.word)-1):
            if self.word[i] != self.word[i+1]:
                if self.word[i] == "L":
                    LRs.append(i)
                else:
                    RLs.append(i)
        for i in RLs:
            for j in RLs:
                if j != i:
                    if count(middle(self.word, i, j)) == 4:
                        # Reduce!!!
                        new_word = []
                        for k in range(len(self.word)):
                            if not (k in [i, i+1, j, j+1]):
                                new_word.append(self.word[k])
                        self.word = copy.deepcopy(string(new_word))
                        return
        for i in LRs:
            for j in LRs:
                if j != i:
                    if count(middle(self.word, i, j)) == 4:
                        # Reduce!!!
                        new_word = []
                        for k in range(len(self.word)):
                            if not (k in [i, i+1, j, j+1]):
                                new_word.append(self.word[k])
                        self.word = copy.deepcopy(string(new_word))
                        return

        if len(self.word) > 8:
            for i in range(len(self.word)):
                if self.word[0] == self.word[len(self.word)-1]:
                    new_word = self.word[0]
                    for j in range(len(self.word)-1):
                        new_word += self.word[j]
                    self.word = copy.deepcopy(new_word)
                else:
                    break
            for i in range(len(self.word)):
                if self.word[i:i+8] in ["RRRRRRRR", "LLLLLLLL"]:
                    # Reduce!!!
                    new_word = []
                    for k in range(len(self.word)):
                        if not (k in [i, i+1, i+2, i+3, i+4, i+5, i+6, i+7]):
                            new_word.append(self.word[k])
                    self.word = copy.deepcopy(string(new_word))
                    return

    def gap(self):
        if self.final_point == ():
            angle = m.pi / 2
            active_point = self.origin
            pivot = (self.origin[0], self.origin[1] + self.radius)
            previous_letter = "R"
            filling_color = 0
            for letter in self.word:
                if letter == previous_letter:
                    angle -= unit(letter) * (m.pi / 4)
                    active_point = (pivot[0] + (self.radius * m.cos(angle)), pivot[1] - (self.radius * m.sin(angle)))
                else:
                    pivot = ((2 * active_point[0]) - pivot[0], (2 * active_point[1]) - pivot[1])
                    angle = m.pi + angle
                    angle -= unit(letter) * (m.pi / 4)
                    active_point = (pivot[0] + (self.radius * m.cos(angle)), pivot[1] - (self.radius * m.sin(angle)))
                    previous_letter = letter
            self.final_point = active_point
            self.final_pivot = pivot
        return (self.origin[0]-self.final_point[0], self.origin[1]-self.final_point[1]), m.dist(self.origin, self.final_point)
