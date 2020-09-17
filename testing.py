import pygame,random
    
def draw_floor(floor, floor_pos):
    screen.blit(floor, (floor_pos, 400))
    screen.blit(floor, (floor_pos + 288, 400))

def create_pipe():
    pipe_pos=random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (400,pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (400,pipe_pos-130))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 412:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe=pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
    
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 400:
        return False
    return True

def rotate_bird(bird):
    angled_bird=pygame.transform.rotozoom(bird,-bird_movement*4, 1)
    return angled_bird

def bird_animation(bird_list,index):
    new_bird=bird_list[index]
    new_rect=new_bird.get_rect(center = (50, bird_rect.centery))
    return new_bird,new_rect

pygame.init()
screen=pygame.display.set_mode((288, 512))
clock=pygame.time.Clock()

#Game variables 
gravity=0.12
bird_movement=0
game_active = False 
start_flag=0
score=0
high_score=0

#surfaces
bg_surface=pygame.image.load('assets/sprites/background-day.png').convert()

floor=pygame.image.load('assets/sprites/base.png').convert()
floor_pos=0

gameover_surface=pygame.image.load('assets/sprites/gameover.png').convert_alpha()
initial_surface=pygame.image.load('assets/sprites/message.png').convert_alpha()

bird_downflap=pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()
bird_upflap=pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()
bird_midflap=pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha()
bird_list=[bird_upflap,bird_midflap,bird_downflap]
bird_index=0
bird_surface=bird_list[bird_index]
bird_rect=bird_surface.get_rect(center = (50,180))

BIRDFLAP=pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,100)

pipe_surface=pygame.image.load('assets/sprites/pipe-red.png').convert()
pipe_list=[]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height= [160,246,330]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 4.8 
            if event.key == pygame.K_SPACE and game_active == False:
                game_active=True
                pipe_list.clear()
                bird_movement=0
                bird_rect.center = (50,180)
                start_flag=1

        if event.type  == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            bird_index+=1
            if bird_index > 2:
                bird_index %= 3
            bird_surface,bird_rect = bird_animation(bird_list,bird_index)

    #background image
    screen.blit(bg_surface, (0, 0))
    
    if game_active:
        #bird movement
        bird_movement+=gravity
        rotated_bird=rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active=check_collision(pipe_list)
        #pipes    
        pipe_list=move_pipes(pipe_list)
        draw_pipes(pipe_list)
    elif game_active == False and start_flag == 0:
        screen.blit(initial_surface,(52,120))
    else:
        screen.blit(gameover_surface,(52,150))
    
    # floor
    if floor_pos <= -288:
        floor_pos = 0
    draw_floor(floor, floor_pos)
    floor_pos -= 1   
        
    pygame.display.update()
    clock.tick(120)