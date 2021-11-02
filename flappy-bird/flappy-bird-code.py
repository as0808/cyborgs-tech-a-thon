import pygame, sys, random, io

def draw_floor():
    screen.blit(floor,(floor_x_pos,450))
    screen.blit(floor,(floor_x_pos+288,450))
    
def create_pipe():
    random_pipe_pos=random.choice(pipe_height)
    bottom_pipe=pipe_surface.get_rect(midtop=(300,random_pipe_pos))
    top_pipe=pipe_surface.get_rect(midbottom=(300,random_pipe_pos-125))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx-=5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom>=400:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe=pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
            
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top<=-50 or bird_rect.bottom>=450:
        return False
    return True

def rotate_bird(bird):
    new_bird=pygame.transform.rotozoom(bird,-bird_movement*3,1)
    return new_bird

def bird_animation():
    new_bird=bird_frames[bird_index]
    new_bird_rect=new_bird.get_rect(center=(50,bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state=='main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface,score_rect)
    if game_state=='game_over':
        score_surface=game_font.render(f'Score: {int(score)}' ,True,(255,255,255))
        score_rect=score_surface.get_rect(center = (144,50))
        screen.blit(score_surface,score_rect)

        high_score_surface=game_font.render(f'High score:{int(high_score)}',True,(255,255,255))
        high_score_rect=high_score_surface.get_rect(center=(144,425))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
    if score>high_score:
        high_score = score
    return high_score

def pipe_score_check():
    global score, can_score 
    if pipe_list:
        for pipe in pipe_list:
            if 95<pipe.centerx < 105 and can_score:
                score+=1
                can_score=False
            if pipe.centerx<0:
                can_score=True
                
pygame.init()
screen=pygame.display.set_mode((288,512))
clock=pygame.time.Clock()
game_font=pygame.font.Font('sprites/04B_19__.ttf',40)

gravity=0.15
bird_movement=0
game_active=True
score=0
high_score=0
can_score=True
background=pygame.image.load("sprites/background-day.png").convert()

floor=pygame.image.load("sprites/base.png").convert()
floor_x_pos=0

bird_downflap=pygame.image.load('sprites/bluebird-downflap.png').convert_alpha()
bird_midflap=pygame.image.load('sprites/bluebird-midflap.png').convert_alpha()
bird_upflap=pygame.image.load('sprites/bluebird-upflap.png').convert_alpha()
bird_frames=[bird_downflap,bird_midflap,bird_upflap]
bird_index=0
bird_surface=bird_frames[bird_index]
bird_rect=bird_surface.get_rect(center=(50,256))
BIRDFLAP=pygame.USEREVENT+1
pygame.time.set_timer(BIRDFLAP,200)

pipe_surface=pygame.image.load("sprites/pipe-green.png").convert()
pipe_list=[]
SPAWNPIPE=pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,2000)
pipe_height=[150,200,250]

game_over_surface=pygame.image.load('Desktop/sprites/message.png').convert_alpha()
game_over_rect=game_over_surface.get_rect(center=(144,256))

flap_sound=pygame.mixer.Sound('audio/wing.wav')
death_sound=pygame.mixer.Sound('audio/hit.wav')
score_sound=pygame.mixer.Sound('audio/point.wav')
score_sound_countdown=100
SCOREEVENT=pygame.USEREVENT+2
pygame.time.set_timer(SCOREEVENT,100)

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and game_active:
                bird_movement=0
                bird_movement-=4
                flap_sound.play()
            if event.key==pygame.K_SPACE and game_active==False:
                game_active=True
                pipe_list.clear()
                bird_rect.center=(50,256)
                bird_movement=0
                score=0
                
        if event.type==SPAWNPIPE:
            pipe_list.extend(create_pipe())
            print(pipe_list)
            
        if event.type==BIRDFLAP:
            if bird_index<2:
                bird_index+=1
            else:
                bird_index=0
            bird_surface,bird_rect=bird_animation()
            
    screen.blit(background,(0,0))
    
    if game_active:        
        bird_movement+=gravity
        rotated_bird=rotate_bird(bird_surface)
        bird_rect.centery+=bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active=check_collision(pipe_list)

        pipe_list=move_pipes(pipe_list)
        draw_pipes(pipe_list)
        
        score+=0.01
        score_sound_countdown-=1
        if score_sound_countdown<=0:
            score_sound.play()
            score_sound_countdown=100
        score_display('main_game')
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')
    
    floor_x_pos-=1
    draw_floor()
    if floor_x_pos<=-288:
        floor_x_pos=0
    
    pygame.display.update()
    clock.tick(80)
