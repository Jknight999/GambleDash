#imports
import pygame
import math

#player class
class Player:
    def __init__(self, sw, sh):
        #setting char properties
        self.screen_w = sw
        self.screen_h = sh
        self.w = 40
        self.h = 40
        self.x = 100
        self.y = 100
        self.color = (255, 0, 0)
        self.y_vel = 0
        self.gravity = 120
        self.jump_strength = -2000
        self.angle = 0
        self.rotation_speed = -4
        self.is_jumping = False

        #makes a transparent surface
        self.surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        #draws the player onto the surface
        pygame.draw.rect(self.surface, self.color, (0, 0, self.w, self.h))
        #makes a copy of the surface that will be rotated from the original surface by the turn angle
        self.rotated_surface = self.surface
        #draws a box around the surface and snaps it to the center of the surface
        self.rect = self.rotated_surface.get_rect(center = (self.x + self.w//2, self.y + self.h//2))

    def rotate_player(self):
        self.angle = (self.angle + self.rotation_speed) % 360
        #rotates the surface
        self.rotated_surface = pygame.transform.rotate(self.surface, self.angle)
        self.rect = self.rotated_surface.get_rect(center = (self.x + self.w//2, self.y + self.h//2))

    #player jump function, only called when jumping = 1
    def jump(self):
        self.y_vel = self.jump_strength
        self.is_jumping = True

    #applies gravity and ground collision detection
    def apply_physics(self):
        global GROUND_Y
        self.y_vel += self.gravity
        self.y += self.y_vel * dt
        if self.y >= GROUND_Y - self.h:
            self.y = GROUND_Y - self.h
            self.y_vel = 0
            self.is_jumping = False
            #snaps the cube back to flat on the ground
            self.angle = round(self.angle / 90) * 90 % 360
            self.rotated_surface = pygame.transform.rotate(self.surface, self.angle)
        self.rect = self.rotated_surface.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))

#button class
class Button:
    #takes in characteristics as arguments and makes a rectangle with them
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color

    #draws the button
    def draw_button(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    #checks if the button is clicked and loads GambleDash
    def check_button_click(self, click_event):
        global in_game
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if click_event.type == pygame.MOUSEBUTTONDOWN and click_event.button == 1:
                in_game = True

#basic vars
SCREENWIDTH = 1000
SCREENHEIGHT = 600
GROUND_Y = math.floor(0.66*SCREENHEIGHT)
FRAMERATE = 120

#draws player to the screen
def draw_player(to_draw):
    global screen
    screen.blit(to_draw.rotated_surface, to_draw.rect)
    #pygame.draw.rect(screen, to_draw.color, (to_draw.x, to_draw.y, to_draw.w, to_draw.h))

#draws the game screen
def draw_platformer_screen(f_color):
    global GROUND_Y, SCREENHEIGHT
    screen.fill((0, 0, 102))
    pygame.draw.rect(screen, f_color, (0, GROUND_Y, SCREENWIDTH, math.ceil(0.34 * SCREENHEIGHT)))

#draws menu screen
def draw_menu_screen():
    play_button.draw_button(screen)

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), vsync = 1)
pygame.init()
clock = pygame.time.Clock()
dt = 0
floor_color = [0, 102, 255]
running = True
in_game = False

#creates the player
player = Player(SCREENWIDTH, SCREENHEIGHT)

#creates the play button
play_button = Button(SCREENWIDTH / 2 - SCREENWIDTH / 8, SCREENHEIGHT / 2 - SCREENHEIGHT / 8, SCREENWIDTH / 4, SCREENHEIGHT / 4, (255, 0, 0))

while running:
    #1. Erase Old
    screen.fill(0)

    #2. Make Changes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                in_game = not in_game
        #sends event to button to see if it's been clicked
        play_button.check_button_click(event)

    if in_game:
        #jumping if space bar is pressed, otherwise not
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not player.is_jumping:
            if player.y >= GROUND_Y - player.h:
                player.y = GROUND_Y - player.h
                player.jump()
        player.apply_physics()

        if player.y < GROUND_Y - player.h:
            player.rotate_player()
    else:
        pass

    #3. Draw New
    if in_game:
        draw_platformer_screen(floor_color)
        draw_player(player)
    else:
        draw_menu_screen()

    #4. Update and Wait
    dt = clock.tick(FRAMERATE) / 1000
    pygame.display.update()
