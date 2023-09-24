import pygame
import random

screen_width=576
screen_height=1024
bird_position_offset=50
    
bird_img=[pygame.transform.scale2x(pygame.image.load("asset/bird1.png")),
          pygame.transform.scale2x(pygame.image.load("asset/bird2.png")),
          pygame.transform.scale2x(pygame.image.load("asset/bird3.png"))]
bg_image=pygame.transform.scale(pygame.image.load("asset/bg.png"),(screen_width,screen_height))
pipe_img=pygame.transform.scale2x(pygame.image.load("asset/pipe.png"))
base_image=pygame.transform.scale2x(pygame.image.load("asset/base.png"))
    

class Flappy_Bird:
    def __init__(self,x,y):
        self.velocity=0
        self.x=x
        self.y=y
        self.img_index=0
        self.time=0
        self.height=self.y
        self.img=bird_img[0]
    def flap(self): # make the bird jump
        self.velocity=-80    
        self.time=0
        self.y=self.height
        self.move()
        
    def move(self): # make the bird move in y direction
        
        # movement logic equations
        self.time+=0.1
        
        # equations
        s=self.velocity*self.time+15*(self.time)**2
        velocity=self.velocity+20*(self.time)
       
        self.height=self.y+s
        
        # the flapping animation
        self.img_index+=1
        if self.img_index==30:self.img_index=0
        self.img=bird_img[self.img_index//10]
        img_center=self.img.get_rect().center
        
        # tilting animation
        tilt=-0.6*velocity 
        if tilt<-90:
            tilt=-90
        rotated_img=pygame.transform.rotate(self.img, tilt )
        rotated_img.get_rect(center=img_center)
        
        
        return rotated_img,self.x,self.y+s
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    
class Pipe:
    rand_range_min=100
    rand_range_max=600
    def __init__(self):
        self.x=screen_width
        self.velocity=-5
        self.pipe_gap=200
        self.upper_pipe_height=-random.randrange(Pipe.rand_range_min,Pipe.rand_range_max)
        self.lower_pipe_height=(pipe_img.get_height())+(self.upper_pipe_height)+(self.pipe_gap)

    def move(self):
        if self.x == -pipe_img.get_width():
            self.upper_pipe_height = -random.randrange(Pipe.rand_range_min,Pipe.rand_range_max)
            self.lower_pipe_height = (pipe_img.get_height()) + (self.upper_pipe_height) + (self.pipe_gap)
            self.x = screen_width
        self.pipe_img=pipe_img
        self.inverted_pipe_img = pygame.transform.flip(pipe_img,False,True)
        self.x += self.velocity
        
        return self.pipe_img,self.inverted_pipe_img,self.x
    
    def colide(self,bird):
        bird_mask=bird.get_mask()
        top_pipe_mask=pygame.mask.from_surface(self.inverted_pipe_img)
        bottom_pipe_mask=pygame.mask.from_surface(self.pipe_img)
        top_offset=(self.x - bird.x,self.upper_pipe_height-bird.height)
        bottom_offset=(self.x - bird.x,self.lower_pipe_height-bird.height      )
        
        b_point=bird_mask.overlap(bottom_pipe_mask,bottom_offset)
        t_ponit=bird_mask.overlap(top_pipe_mask,top_offset)
        
        if b_point or t_ponit:
            return True
        return False
        
class Base:
    
    def __init__(self):
        self.x=0
        self.velocity=-5
        self.upper_height=screen_height*0.85
        
    def move(self):
        if self.x < -base_image.get_width():
            self.x=0
        self.x+=self.velocity
        
        return base_image,self.x,self.upper_height
    def colide(self,bird):
        if bird.y>(self.upper_height)-bird.img.get_height() or bird.y<0:
            return True
        
def create_window(screen,bird,pipe,base):
    screen.blit(bg_image,(0,0))
    bird_img,x_bird,y_bird=bird.move()
    pipe_img,inverted_pipe_img,x_pipe=pipe.move()
    base_img,x_base,y_base=base.move()
    screen.blit(bird_img,(x_bird,y_bird))
    screen.blit(inverted_pipe_img,(x_pipe,pipe.upper_pipe_height))
    screen.blit(pipe_img,(x_pipe,pipe.lower_pipe_height))
    screen.blit(base_img,(x_base,y_base))
    screen.blit(base_img,(x_base+base_image.get_width(),y_base))

    pygame.display.update()
        
def main():
    
    pygame.display.set_caption("Flappy Bird")
    bird=Flappy_Bird((screen_width/2)-bird_position_offset,screen_height/2)
    pipe=Pipe()
    base=Base()
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock=pygame.time.Clock()
    running=True
    
    while running:
        clock.tick(120)
        create_window(screen,bird,pipe,base)
        if pipe.colide(bird) or base.colide(bird):
            pygame.quit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()
    pygame.quit()
    quit()
    
main()