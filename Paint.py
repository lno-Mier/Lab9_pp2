import pygame
import math

pygame.init()

W, H = 800, 800
sc = pygame.display.set_mode((W, H))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
ORANGE= (252, 154, 8)
YELLOW= (252, 248, 3)
PINK  = (252, 3, 252)
PURPLE= (169, 3, 252)
GRAY  = (206, 204, 207)

colors = {
    'white': WHITE, 'black': BLACK, 'red': RED, 'green': GREEN,
    'blue': BLUE, 'orange': ORANGE, 'yellow': YELLOW,
    'pink': PINK, 'purple': PURPLE, 'gray': GRAY
}

eraser = pygame.image.load('C:\\Users\\mierc\\OneDrive\\Рабочий стол\\PP2\\lab_8_pp2\\PygameTutorial_3_0\\Eraser.png').convert_alpha()
eraser = pygame.transform.scale(eraser, (eraser.get_width()//15, eraser.get_height()//15))
eraser_rect = eraser.get_rect(center=(700, 70))
eraser2 = pygame.transform.scale(eraser, (eraser.get_width()//1.5, eraser.get_height()//1.5))

def draw_isosceles_triangle(screen, start_pos, end_pos, current_color):
    x2, y2 = max(start_pos[0], end_pos[0]), max(start_pos[1], end_pos[1])
    x1, y1 = min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1])
    
    base_mid_x = (x1 + x2) / 2
    top_vertex = (base_mid_x, y1)
    base_left = (x1, y2)
    base_right = (x2, y2)
    
    pygame.draw.polygon(screen, current_color, [top_vertex, base_left, base_right])
    
def is_point_in_triangle(px, py, A, B, C):
    def triangle_area(X, Y, Z):
        return abs((X[0] * (Y[1] - Z[1]) + Y[0] * (Z[1] - X[1]) + Z[0] * (X[1] - Y[1])) / 2.0)

    S_ABC = triangle_area(A, B, C)
    S_PBC = triangle_area((px, py), B, C)
    S_PCA = triangle_area((px, py), C, A)
    S_PAB = triangle_area((px, py), A, B)

    return abs(S_PBC + S_PCA + S_PAB - S_ABC) < 1e-5

def draw_parallelogram(screen, start_pos, end_pos, current_color):
    x1, y1 = start_pos
    x2, y2 = end_pos
    
    shift = (x2 - x1) // 3
    top_left = (x1, y1)
    top_right = (x2, y1)
    bottom_left = (x1 + shift, y2)
    bottom_right = (x2 + shift, y2)

    pygame.draw.polygon(screen, current_color, [top_left, top_right, bottom_right, bottom_left])
    
def is_point_in_parallelogram(px, py, A, B, C, D):
    def triangle_area(X, Y, Z):
        return abs((X[0] * (Y[1] - Z[1]) + Y[0] * (Z[1] - X[1]) + Z[0] * (X[1] - Y[1])) / 2.0)

    S_ABCD = triangle_area(A, B, C) + triangle_area(A, C, D)
    S_PAB = triangle_area((px, py), A, B)
    S_PBC = triangle_area((px, py), B, C)
    S_PCD = triangle_area((px, py), C, D)
    S_PAD = triangle_area((px, py), A, D)

    return abs(S_PAB + S_PBC + S_PCD + S_PAD - S_ABCD) < 1e-5

current_color = RED
mode = "brush"

drawed = []

sc.fill(WHITE)

x, y = 0, 0
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 15)

is_erase = False
is_visible = True
start_pos = None
preview_shape = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if color_yellow.collidepoint(event.pos):
                current_color = YELLOW
            elif color_green.collidepoint(event.pos):
                current_color = GREEN
            elif color_red.collidepoint(event.pos):
                current_color = RED
            elif color_blue.collidepoint(event.pos):
                current_color = BLUE
            elif color_orange.collidepoint(event.pos):
                current_color = ORANGE
            elif color_pink.collidepoint(event.pos):
                current_color = PINK
            elif color_purple.collidepoint(event.pos):
                current_color = PURPLE
            elif color_black.collidepoint(event.pos):
                current_color = BLACK

            elif eraser_rect.collidepoint(event.pos):
                is_visible = not is_visible
                is_erase = not is_erase

            elif square_button.collidepoint(event.pos):
                mode = "rect"
            elif circle_button.collidepoint(event.pos):
                mode = "circle"
            elif triangle_button.collidepoint(event.pos):
                mode = "triangle"
            elif parallelogram_button.collidepoint(event.pos):
                mode = "parallelogram"
            elif brush_button.collidepoint(event.pos):
                mode = "brush"
            

            elif event.pos[1] >= 183 and not is_erase:
                if mode in ("rect", "circle", "triangle", "parallelogram"):
                    start_pos = event.pos
                elif mode == "brush":
                    drawed.append(("dot", event.pos, current_color))

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and start_pos:
            end_pos = event.pos
            preview_shape = None
            drawed.append((mode, start_pos, end_pos, current_color))
            start_pos = None

        elif event.type == pygame.MOUSEMOTION:
            if start_pos and pygame.mouse.get_pressed()[0] and not is_erase:
                preview_shape = (mode, start_pos, event.pos, current_color)
            elif pygame.mouse.get_pressed()[0] and mode == "brush" and not is_erase and pygame.mouse.get_pos()[1] >= 183:
                drawed.append(("dot", pygame.mouse.get_pos(), current_color))

    sc.fill(WHITE)

    for item in drawed:
        if item[0] == "dot":
            _, pos, color = item
            pygame.draw.circle(sc, color, pos, 5)
        else:
            fig_type, sp, ep, color = item
            x1, y1 = sp
            x2, y2 = ep
            rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
            rect.normalize()
            if fig_type == "rect":
                pygame.draw.rect(sc, color, rect)
            elif fig_type == "circle":
                center = rect.center
                radius = int(min(rect.width, rect.height) / 2)
                pygame.draw.circle(sc, color, center, radius)
            elif fig_type == "triangle":
                draw_isosceles_triangle(sc, sp, ep, color)
            elif fig_type == "parallelogram":
                draw_parallelogram(sc, sp, ep, color)

    if preview_shape:
        fig_type, sp, ep, color = preview_shape
        rect = pygame.Rect(*sp, ep[0] - sp[0], ep[1] - sp[1])
        rect.normalize()
        if fig_type == "rect":
            pygame.draw.rect(sc, color, rect, 2)
        elif fig_type == "circle":
            center = rect.center
            radius = int(min(rect.width, rect.height) / 2)
            pygame.draw.circle(sc, color, center, radius, 2)
        elif fig_type == "triangle":
            draw_isosceles_triangle(sc, sp, ep, color)
        elif fig_type == "parallelogram":
            draw_parallelogram(sc, sp, ep, color)

    pygame.mouse.set_visible(is_visible)
    if is_erase:
        sc.blit(eraser2, pygame.mouse.get_pos())
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            new_drawed = []
            for item in drawed:
                if item[0] == "dot":
                    pos, color = item[1], item[2]
                    dx = pos[0] - mx
                    dy = pos[1] - my
                    if (dx**2 + dy**2)**0.5 > 10:
                        new_drawed.append(item)
                else:
                    fig_type, sp, ep, color = item
                    rect = pygame.Rect(*sp, ep[0] - sp[0], ep[1] - sp[1])
                    rect.normalize()
                    if fig_type == "rect":
                        if not rect.collidepoint(mx, my):
                            new_drawed.append(item)
                    elif fig_type == "circle":
                        center = rect.center
                        radius = int(min(rect.width, rect.height) / 2)
                        dx = mx - center[0]
                        dy = my - center[1]
                        if dx**2 + dy**2 > radius**2:
                            new_drawed.append(item)
                    elif fig_type == "triangle":
                        top_vertex = sp
                        base_left = (sp[0], ep[1])
                        base_right = ep
                        if not is_point_in_triangle(mx, my, top_vertex, base_left, base_right):
                            new_drawed.append(item)
                    elif fig_type == "parallelogram":
                        top_left = sp
                        top_right = (ep[0], sp[1])
                        bottom_left = (sp[0] + (ep[0] - sp[0]) // 3, ep[1])
                        bottom_right = (ep[0] + (ep[0] - sp[0]) // 3, ep[1])
                        if not is_point_in_parallelogram(mx, my, top_left, top_right, bottom_right, bottom_left):
                            new_drawed.append(item)
                            
            drawed = new_drawed

    pygame.draw.rect(sc, GRAY, (50, 30, 130, 130), 5)
    pygame.draw.rect(sc, current_color, (55, 35, 120, 120))

    color_red = pygame.draw.rect(sc, RED, (300, 30, 50, 50))
    color_yellow = pygame.draw.rect(sc, YELLOW, (380, 30, 50, 50))
    color_green = pygame.draw.rect(sc, GREEN, (460, 30, 50, 50))
    color_blue = pygame.draw.rect(sc, BLUE, (540, 30, 50, 50))
    color_orange = pygame.draw.rect(sc, ORANGE, (300, 110, 50, 50))
    color_pink = pygame.draw.rect(sc, PINK, (380, 110, 50, 50))
    color_purple = pygame.draw.rect(sc, PURPLE, (460, 110, 50, 50))
    color_black = pygame.draw.rect(sc, BLACK, (540, 110, 50, 50))

    brush_button = pygame.draw.rect(sc, GRAY, (660, 30, 60, 60), 5)

    square_button = pygame.draw.rect(sc, GRAY, (660, 110, 60, 60), 5)
    pygame.draw.rect(sc, current_color, (665, 115, 50, 50))

    circle_button = pygame.draw.rect(sc, GRAY, (735, 110, 60, 60), 5)
    pygame.draw.circle(sc, current_color, (765, 140), 25)
    
    triangle_button = pygame.draw.rect(sc, GRAY, (660, 180, 60, 60), 5)
    pygame.draw.polygon(sc, current_color, [(690, 185), (665, 235), (715, 235)])
    
    parallelogram_button = pygame.draw.rect(sc, GRAY, (735, 180, 60, 60), 5)
    pygame.draw.polygon(sc, current_color, [(755, 185), (735, 235), (775, 235), (795, 185)])

    pygame.draw.line(sc, BLACK, (0, 180), (800, 180), 3)
    pygame.draw.line(sc, BLACK, (270, 180), (270, 0), 3)
    pygame.draw.line(sc, BLACK, (630, 180), (630, 0), 3)

    write_color = font.render("Colors", True, BLACK)
    write_current = font.render("Now using", True, BLACK)
    write_tools = font.render("Tools", True, BLACK)

    sc.blit(write_current, (60, 10))
    sc.blit(write_color, (420, 10))
    sc.blit(write_tools, (660, 10))

    sc.blit(eraser, eraser_rect)

    pygame.display.update()
    clock.tick(60)