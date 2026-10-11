import pygame
import pygame.freetype

class Player:
    #basic player characteristics
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
        self.image = pygame.image.load("Assets/playerskin02.png").convert_alpha()
        #sets the size of the sprite to 40 x 40
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        self.rotated_surface = self.image
        #draws a box around the surface and snaps it to the center of the surface
        self.rect = self.rotated_surface.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))

        #creates a mask around the player for collision handling
        self.mask = pygame.mask.from_surface(self.rotated_surface)

    def rotate_player(self, dt):
        #calculates and sets rotation angle
        self.angle = (self.angle + self.rotation_speed * dt) % 360
        #rotates the surface
        self.rotated_surface = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rotated_surface.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))
        self.mask = pygame.mask.from_surface(self.rotated_surface)

    def snap_rotation(self):
        self.angle = round(self.angle / 90) * 90 % 360
        self.rotated_surface = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rotated_surface.get_rect(center=(self.x+self.w // 2, self.y + self.h // 2))
        self.mask = pygame.mask.from_surface(self.rotated_surface)

class Spike:
    #basic spike characteristics
    def __init__(self, x, y, sw, sh):
        self.x = x
        self.y = y
        self.width = sw / 20
        self.height = sh / 10
        self.hitbox = pygame.Rect(x + self.width / 2.5, self.y + self.height / 3, self.width / 5, self.height / 2.3)

        #makes the spike hitbox into a surface
        self.surface = pygame.Surface((self.hitbox.width, self.hitbox.height), pygame.SRCALPHA)

        #makes the hitbox not transparent so a mask can be made around it
        self.surface.fill((255, 0, 0))

        #draws a mask around the surface
        self.mask = pygame.mask.from_surface(self.surface)

    def find_vertices(self):
        #calculates where the vertices should be based off x, y, w and h of the spike
        return [[self.x, self.y + self.height], [self.x + self.width / 2, self.y], [self.x + self.width, self.y + self.height]]

class Block:
    # Shared resources: create these only once.
    shared_image = None
    shared_mask = None
    shared_size = None

    def __init__(self, x, y, sw, sh):
        self.x = x
        self.y = y
        self.width = sw / 20
        self.height = sh / 10

        size = (round(self.width), round(self.height))

        # Load, scale, and mask the image only once per size.
        if Block.shared_image is None or Block.shared_size != size:
            Block.shared_image = pygame.image.load("Assets/gambledashblock.png").convert_alpha()

            Block.shared_image = pygame.transform.scale(Block.shared_image, size)

            Block.shared_mask = pygame.mask.from_surface(Block.shared_image)
            Block.shared_size = size

        # Reuse the shared image and mask.
        self.image = Block.shared_image
        self.mask = Block.shared_mask

        self.block = pygame.Rect(self.x, self.y, self.width, self.height)

        self.colliding = False

class Button:
    #takes in characteristics as arguments and makes a rect with them
    def __init__(self, x, y, w, h, color, text):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color

        #if the text argument is filled it will parse the tuple and change the font size to the specified num
        if text != 0:
            self.text, self.font_name, self.text_size, self.text_color = text
            self.font = pygame.freetype.Font(self.font_name, self.text_size)

    def render_text(self, surface):
        #gets the rectangle that bounds the text
        text_rect = self.font.get_rect(self.text)
        #sets the center to the center of the button
        text_rect.center = (self.x + self.w / 2, self.y + self.h / 2)
        #prints (renders) the text to the screen
        self.font.render_to(surface, text_rect, self.text, self.text_color)

    #draws the button
    def draw_button(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    #checks if the button is clicked
    def check_button_click(self, click_event):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and click_event.type == pygame.MOUSEBUTTONDOWN and click_event.button == 1:
            return True
        else:
            return False