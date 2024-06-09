import pygame
import math
import ctypes
import win32gui
import win32con
from ducky import ducky

#init
pygame.init()
pygame.mixer.init()

#Create Fullscreen Window
pygame.display.set_caption("Desktop Ducky")
WINDOW = pygame.display.set_mode((0, 0), pygame.NOFRAME)

#Make window layered
hwnd = pygame.display.get_wm_info()["window"]
ctypes.windll.user32.SetWindowLongW(hwnd, -20, ctypes.windll.user32.GetWindowLongW(hwnd, -20) | 0x80000)

# Make the entire window transparent
transparency_color = (0, 0, 0)
color_key = (transparency_color[2] << 16) | (transparency_color[1] << 8) | transparency_color[0]
ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, color_key, 0, 0x00000001)

#set framerate
clock = pygame.time.Clock()
FPS = 60

#Load all Ducky Idle Sprites
DUCKY_IDLE_01 = pygame.transform.scale(pygame.image.load("Assets\Sprites\idle\idle01.png"), (100, 100))
DUCKY_IDLE_02 = pygame.transform.scale(pygame.image.load("Assets\Sprites\idle\idle02.png"), (100, 100))
DUCKY_IDLE_ARRAY = [DUCKY_IDLE_01, DUCKY_IDLE_02]

#Load all Ducky walk Sprites
DUCKY_WALK_01 = pygame.transform.scale(pygame.image.load("Assets\Sprites\walk\walk01.png"), (100, 100))
DUCKY_WALK_02 = pygame.transform.scale(pygame.image.load("Assets\Sprites\walk\walk02.png"), (100, 100))
DUCKY_WALK_03 = pygame.transform.scale(pygame.image.load("Assets\Sprites\walk\walk03.png"), (100, 100))
DUCKY_WALK_04 = pygame.transform.scale(pygame.image.load("Assets\Sprites\walk\walk04.png"), (100, 100))
DUCKY_WALK_05 = pygame.transform.scale(pygame.image.load("Assets\Sprites\walk\walk05.png"), (100, 100))
DUCKY_WALK_06 = pygame.transform.scale(pygame.image.load("Assets\Sprites\walk\walk06.png"), (100, 100))
DUCKY_WALK_ARRAY = [DUCKY_WALK_01, DUCKY_WALK_02, DUCKY_WALK_03, DUCKY_WALK_04, DUCKY_WALK_05, DUCKY_WALK_06]

#Load Quack Image and Sound
QUACK_IMAGE = pygame.transform.scale(pygame.image.load("Assets\Sprites\quack\quack01.png"), (100, 100))
QUACK_SOUND = pygame.mixer.Sound("Assets\Sounds\quack_sound.mp3")

#Create a Ducky instance
ducky_instantce = ducky(WINDOW, DUCKY_IDLE_01, (900, 400), QUACK_IMAGE)
move = True
amim = DUCKY_WALK_ARRAY
anim_speed = 0.15
quack_audio = None
quack_particle = None

#Game Loop with 60 FPS
run = True
transparent_surface = pygame.Surface(WINDOW.get_size())
transparent_surface.fill((0, 0, 0))

while run:
    clock.tick(FPS)

    #Keep Window on Top
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE)

    #Draw TransparentCircle Surface Behind the Ducky
    WINDOW.blit(transparent_surface, ducky_instantce.position, ducky_instantce.image.get_rect())
    
    #Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            move = False
            amim = DUCKY_IDLE_ARRAY
            anim_speed = 0.07
            quack_audio = QUACK_SOUND
            quack_particle = QUACK_IMAGE
        elif event.type == pygame.MOUSEBUTTONUP:
            move = True
            amim = DUCKY_WALK_ARRAY
            anim_speed = 0.15
            quack_audio = None
            quack_particle = None
            WINDOW.fill((0, 0 ,0))
  
    #Move to Random Locations, set animations, play sound
    ducky_instantce.move_to_next_location(move)
    ducky_instantce.play_animation(amim, anim_speed)
    ducky_instantce.play_quack_sound(quack_audio)
    ducky_instantce.quack_is_angry(quack_particle)
    
    pygame.display.update()

pygame.quit()
