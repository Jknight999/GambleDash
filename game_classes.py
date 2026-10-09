import pygame
import random

class Player:
    #player characteristics
    def __init__(self, sw, sh, floor_y):
        self.SCREENWIDTH = sw
        self.SCREENHEIGHT = sh
        self.w = self.SCREENWIDTH / 20
        self.h = self.SCREENHEIGHT / 10
        self.x = (self.SCREENWIDTH - self.w) / 4
        self.y = (floor_y - self.h)
        self.color = (14, 237, 70)
        self.y_vel = 0
        self.gravity = 1800000 / self.SCREENHEIGHT
        self.jump_strength = -900
        self.angle = 0
        self.rotation_speed = -(self.gravity / 10)

        #makes a sprite of the cube asset
        self.image = pygame.image.load("Assets/playerskin0" + str(random.randint(1,6)) + ".png").convert_alpha()
        #sets the size to 40 x 40
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        self.rotated_surface = self.image
        # draws a box around the surface and snaps it to the center of the surface
        self.rect = self.rotated_surface.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))

        # creates mask for collision handling
        self.mask = pygame.mask.from_surface(self.image)

    def rotate_player(self, dt):
        #calculates and sets rotation angle
        self.angle = (self.angle + self.rotation_speed * dt) % 360
        # rotates the surface
        self.rotated_surface = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rotated_surface.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))

class Spike:
    #spike characteristics
    def __init__(self, x, y, sw, sh):
        self.x = x
        self.y = y
        self.width = sw / 20
        self.height = sh / 10
        self.speed = 550
        self.hitbox = pygame.Rect(x + self.width / 2.5, self.y + self.height / 3, self.width / 5, self.height / 2.3)

        # makes the hitbox into a surface
        self.surface = pygame.Surface((self.hitbox.width, self.hitbox.height), pygame.SRCALPHA)
        self.surface.fill((255, 0, 0))

        # draws a mask around the surface
        self.mask = pygame.mask.from_surface(self.surface)

    def find_vertices(self):
        #calculates where the vertices should be based off x, y, w and h of the spike
        #needed because triangles drawn through draw.polygon()
        # These vertices should not be used for hitboxes, spike hitboxes are rectangular
        return [[self.x, self.y + self.height], [self.x + self.width / 2, self.y], [self.x + self.width, self.y + self.height]]

class Block:
    # spike characteristics
    def __init__(self, x, y, sw, sh):
        self.x = x
        self.y = y
        self.width = sw / 20
        self.height = sh / 10
        self.speed = 550
        self.block = pygame.Rect(self.x, self.y, self.width, self.height)

        #makes the block a sprite
        self.image = pygame.image.load("Assets/gambledashblock.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        #draws a mask around the image for collisions
        self.mask = pygame.mask.from_surface(self.image)

        self.colliding = False