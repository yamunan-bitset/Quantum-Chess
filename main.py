import os
import pygame

pygame.init()

import analysis_board
import computer
from Widgets import Button, Label

logo = pygame.image.load(os.path.join("texture", "black", "knight.png"))
pygame.display.set_icon(logo)
pygame.display.set_caption("Chess Client")
screen = pygame.display.set_mode((1000, 800))
screen.fill((36, 34, 30))

font = pygame.font.SysFont(None, 30)

welcome = Label(screen, font, "Welcome!", (183, 183, 183), 200, 50, 600, 50)
analysis = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), font, "Analysis", (183, 183, 183), 200, 200, 600, 50)
comp = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), font, "Play against computer", (183, 183, 183), 200, 300, 600, 50)
online = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), font, "Play online", (183, 183, 183), 200, 400, 600, 50)

connection_refused = Label(screen, font, "Error: Connection Refused. Try again later.", (150, 10, 10), 200, 450, 600, 50)
error = False

while True:
    event = pygame.event.wait()
    pos = pygame.mouse.get_pos()

    if event.type == pygame.QUIT:
        break

    if analysis.handle_event(event, pos):
        analysis_board.main()
        error = False
    if online.handle_event(event, pos):
        try:
            import client
        except ConnectionRefusedError:
            error = True
        else:
            error = False
    if comp.handle_event(event, pos):
        computer.main()

    screen.fill((36, 34, 30))
    welcome.render()
    analysis.render()
    comp.render()
    online.render()

    if error:
        connection_refused.render()

    pygame.display.update()

pygame.quit()
