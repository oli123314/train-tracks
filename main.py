from track import *
from sys import exit

'''
Many functions in this project haven't been finished, are drafts, or don't work fully


Closed tracks
RRRRRLLRLLRRRRRLRRRLLRLR
RRLRRRLRRRLLLLLLLRLLLRRR

RLLRLRRRRRLRLLLRLLLLLLLRLRRLRRLRRRLR
RRRRLRRRRRRRLRLRRRRRLRRRLRLLLRLLLLLL
RRRLLLLRLRLLLRLRLLLLRRRRLLLLLRLLLLRLLLLRLLLRLRLLRRRRRRRLLRRR
RRRRLRRRRRRRLRRRRLLLLRLRLLLRLRLLLLRRRRLLLLLRLLLLRLLLLRLLLRLRLLRRRRRRRLLRRRLRRRRRLRRRLRLLLRLLLLLL
  
RRRLLLLLRRRRRRRLLRRRRRLLLRLLLLLL
RRRRRRLLLLLRRRRRRRLLRRRL  
LLLRRRRRRLLLRRRRRLLRRRRR     
'''

'''
print(calc_ideal_d_answers(1000000))
print(part_d_matrix(70, 99)*lr_vec)
track.set_part_d_word(13860, 19601)
'''

track = Track("RRRRLRRRRRRRLRRRRLLLLRLRLLLRLRLLLLRRRRLLLLLRLLLLRLLLLRLLLRLRLLRRRRRRRLLRRRLRRRRRLRRRLRLLLRLLLLLL", (sd/2.1, sd/1.1), 40)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                track.word += "L"
            if event.key == pygame.K_RIGHT:
                track.word += "R"
            if event.key == pygame.K_DOWN:
                track.word = track.word[:-1]
            print(track.word, len(track.word))
    screen.fill(bg_color)
    track.display()
    #track.show_pdf_angle()
    track.show_points()
    #track.add_piece_random(0)
    pygame.display.update()
    #track.attempt_reduction()
    #print(track.word)
    print(track.gap())
    clock.tick(fps)
