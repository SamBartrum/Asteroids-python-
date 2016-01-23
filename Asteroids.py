import pygame as pg , random, math, time

height = 800
width = 800


pg.init()
Background = (0,0,0)
screen = pg.display.set_mode((height,width))
pg.display.set_caption("Asteroids")

shipslow = pg.image.load("images/shipslow.png")
shipfast = pg.image.load("images/shipfast.png")
planets = [pg.image.load("images/planet1.png"),pg.image.load("images/planet2.png"),pg.image.load("images/planet3.png"),pg.image.load("images/planet4.png"),pg.image.load("images/planet5.png"),pg.image.load("images/planet6.png")]
powerupimages = {"Life": pg.image.load("images/life.png"), "Rocket": pg.image.load("images/rocket.png") }

SCORE = pg.font.Font('freesansbold.ttf', 40)

fireSE = pg.mixer.Sound('fire.wav')
powerSE = pg.mixer.Sound('Power_Up.wav')
explosionSE = pg.mixer.Sound('Explosion.wav')
lifelostSE = pg.mixer.Sound('Player_death.wav')
music = pg.mixer.Sound('music.mp3')




pg.mixer.init()



gravity = (0 , 0)
drag = 0.999
elasticity = 0.9

  
PowerUps = []
no_particles = 10
my_particles = []
bullet = []
rockets = []


def random_colour():
    a = random.randint(0,255)
    b = random.randint(0,255)
    c = random.randint(0,255)
    return (a,b,c)

def add_vectors( (angle1,length1), (angle2,length2)):
    x = length1 * math.sin(angle1) + length2 * math.sin(angle2)
    y = length1 * math.cos(angle1) + length2 * math.cos(angle2)

    length =  math.hypot(x,y)
    angle = math.atan2(x,y)
    return (angle,length)


class Particle():
    def __init__(self, (x, y), size, image):
        self.x = x
        self.y = y
        self.size = size
        self.colour = random_colour()
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.image = image

    def display(self):
    
       
        temp = pg.transform.scale(self.image, (2*self.size, 2*self.size))
        screen.blit(temp,(self.x-self.size,self.y-self.size))

    def move(self):
        (self.angle, self.speed) = add_vectors((self.angle, self.speed), gravity)
        self.x -= math.sin(self.angle) * self.speed
        self.y += math.cos(self.angle) * self.speed
        self.speed *= drag

    def bounce(self):
        if self.x > width - self.size:
            self.x = (width - self.size) 
            self.angle = - self.angle
            self.speed *= elasticity

        elif self.x < self.size:
            self.x = self.size
            self.angle = - self.angle
            self.speed *= elasticity

        if self.y > height - self.size:
            self.y = (height - self.size)
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif self.y < self.size:
            self.y = self.size 
            self.angle = math.pi - self.angle
            self.speed *= elasticity
  
class Player(Particle):

    def __init__(self, (x, y), angle, image):
        self.x = x
        self.y = y
        self.size = 30
        self.thickness = 0
        self.speed = 0
        self.angle = angle
        self.colour = (0,0,0)
        self.no_rockets = 0
        self.lives = 3
        self.image = image

    def display(self):   # Rewrite using cases
        first = pg.transform.scale(self.image, (self.size,self.size))
        ship = pg.transform.rotate(first, -45)

        if self.angle == 0:
            ship1 = pg.transform.rotate(ship,180)
            screen.blit(ship1,(self.x-self.size/2,self.y-self.size/2))
        
        elif self.angle == math.pi/2 or self.angle == - 3* math.pi/2:
            ship2 = pg.transform.rotate(ship,90)  
            screen.blit(ship2,(self.x-self.size/2,self.y-self.size/2))

        elif self.angle == 3 * math.pi/2 or self.angle == - math.pi/2:

            ship3 = pg.transform.rotate(ship,270)  
            screen.blit(ship3,(self.x-self.size/2,self.y-self.size/2))

        elif self.angle == math.pi:
            ship4 = pg.transform.rotate(ship,0)  
            screen.blit(ship4,(self.x-self.size/2,self.y-self.size/2))        
            
    def bounce(self):
        if self.x > width - self.size:
            self.x = (self.size) 

        elif self.x < self.size:
            self.x = width - self.size

        if self.y > height - self.size:
            self.y = (self.size)

        elif self.y < self.size:
            self.y = height - self.size 
       
class Bullet():
    def __init__(self, (x, y), angle, colour):
        self.x = x
        self.y = y
        self.size = 5
        self.thickness = 0
        self.colour = colour
        self.speed = 30
        self.angle = angle

    def display(self):
        pg.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        (self.angle, self.speed) = add_vectors((self.angle, self.speed), gravity)
        self.x -= math.sin(self.angle) * self.speed
        self.y += math.cos(self.angle) * self.speed    


class PowerUp():
    def __init__(self, (x, y),image, kind):
        self.x = x
        self.y = y
        self.size = 15
        self.thickness = 0
        self.colour = (0,0,255)
        self.image = image
        self.kind = kind
    
    def display(self):

        temp = pg.transform.scale(self.image, (2*self.size, 2*self.size))
        screen.blit(temp,(self.x-self.size/2,self.y-self.size/2))


def delete_bullets(a):
    if a.x > width or a.x < 0 or a.y > height:
        del a

def findParticle(particles,x,y):
    for p in particles:
        if math.hypot(x - p.x, y - p.y) <= p.size:
            return p
    return None

def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    dist = math.hypot(dx, dy)
    thing = 0.5*(p1.size+p2.size -dist+1) #calculates how much they have overlapped
    
    if dist < p1.size + p2.size:
        tangent = math.atan2(dy, dx)
        angle = 0.5 * math.pi + tangent

        angle1 = 2*tangent - p1.angle
        angle2 = 2*tangent - p2.angle
        speed1 = p2.speed*elasticity
        speed2 = p1.speed*elasticity

        (p1.angle, p1.speed) = (angle1, speed1)
        (p2.angle, p2.speed) = (angle2, speed2)

        p1.x += (thing)*math.sin(angle) #Shifts the balls a bit along their new tragectory proportional to their overlap - avoids most sticking
        p1.y -= (thing)*math.cos(angle)
        p2.x -= (thing)*math.sin(angle)
        p2.y += (thing)*math.cos(angle)


def player_reset(player):
    player.x = width/2
    player.y = height/2
    player.speed = 0


def player_collide(player, p2):
    dx = player.x - p2.x
    dy = player.y - p2.y
    
    dist = math.hypot(dx, dy)
    thing = 0.5*(player.size+p2.size -dist+1) #calculates how much they have overlapped
    
    if dist < player.size/2 + p2.size:
        player.lives -= 1
        lifelostSE.play()
        player_reset(player)
        player.image = shipslow
        time.sleep(2)


           

def bullet_hit(bullets,particles):
    for missile in bullets:
        for particle in particles:
            dx = missile.x - particle.x
            dy = missile.y - particle.y

            dist = math.hypot(dx,dy)
            if dist < missile.size + particle.size:
                if particle.size == 20:
                    particles.remove(particle)
                    bullets.remove(missile)
                    explosionSE.play()
                else:
                    particle.size = 20
                    bullets.remove(missile) 
                    explosionSE.play()


def rocket_hit(rockets,particles):
    test = 0
    for rocket in rockets:
        for particle in particles:
            dx = rocket.x - particle.x
            dy = rocket.y - particle.y

            dist = math.hypot(dx,dy)
            if dist < rocket.size + particle.size:
                particles.remove(particle)
                explosionSE.play()
                
            

def power_up(player,pulist):
    for pu in pulist:
        dx = player.x - pu.x
        dy = player.y - pu.y
        dist = math.hypot(dx,dy)
        if dist < pu.size + player.size:
            pulist.remove(pu)
            powerSE.play()
            if pu.kind == "weapon":
                player.no_rockets +=2
            if pu.kind == "life":
                player.lives +=1  
        
        
def game_over_screen():
    # screen.fill((255,255,255))
    GO = SCORE.render("YOU HAVE DIED", True, (255,0,0))
    gameRect3 = GO.get_rect()
    gameRect3.center = (width/2,height/2)
    screen.blit(GO, gameRect3)
    pg.display.flip()


def level_cleared(list):
    if len(list) == 0:
        WON = SCORE.render("LEVEL CLEARED", True, (255,255,255))
        gameRect3 = WON.get_rect()
        gameRect3.center = (width/2,height/2)
        screen.blit(WON, gameRect3)
        pg.display.flip()
        return True


player = Player((width/2, height/2),0, shipslow)
powerup1 = PowerUp((50, height/2), powerupimages['Rocket'], "weapon")
powerup2 = PowerUp((width-50, height/2), powerupimages['Life'], "life")
PowerUps.append(powerup1)
PowerUps.append(powerup2)

for n in range(no_particles):
    size = random.choice([20,40])
    x = (random.randint(size, width/3 - size),random.randint(2*width/3 , width - size) )
    y = (random.randint(size,height/3 - size),random.randint(2*height/3, height - size) )
    a = random.randint(0, len(planets)-1)
    b = random.choice([0,1])
    c = random.choice([0,1])
    particle = Particle((x[b],y[c]),size, planets[a])
   
    if size == 20:
        particle.speed = 10
    else:
        particle.speed = 5

    particle.angle = random.uniform(0, math.pi * 2)


    my_particles.append(particle)   



def Level1():
    s = True
    selected_particle = None

    while s:


        ROCKETS = SCORE.render("Rockets: " + str(player.no_rockets), True, (255,255,255))
        gameRect = ROCKETS.get_rect()
        gameRect.midtop = (6.5*width/8  , 10)

        HEALTH= SCORE.render("Lives: " + str(player.lives), True, (255,255,255))
        gameRect2 = HEALTH.get_rect()
        gameRect2.midtop = (1.5 *width /8, 10)


        for event in pg.event.get():
            if event.type == pg.QUIT:
                s = False
            elif event.type == pg.KEYDOWN:
                
                if event.key == pg.K_LEFT:
                    player.image = shipslow
                    player.speed = 5
                    player.angle = math.pi/2

                if event.key == pg.K_RIGHT:
                    player.image = shipslow
                    player.speed = 5
                    player.angle = - math.pi/2

                if event.key == pg.K_UP:
                    player.image = shipslow
                    player.speed = 5
                    player.angle = math.pi

                if event.key == pg.K_DOWN:
                    player.image = shipslow
                    player.speed = 5
                    player.angle = 0

                if event.key == pg.K_SPACE:  
                    player.image = shipslow         
                    bullet.append(Bullet( (player.x+player.size/4, player.y+player.size/4), player.angle, (0,255,0)))
                    fireSE.play()
                
                if event.key == pg.K_RETURN:
                    player.image = shipslow
                    if player.no_rockets >0:
                        rockets.append(Bullet( (player.x+player.size/4, player.y+player.size/4), player.angle, (255,0,0)))
                        player.no_rockets -= 1
                        fireSE.play()
                    else:
                        print "no"
                if event.key == pg.K_TAB:
                    player.image = shipfast
                    player.speed = 20  


            

        screen.fill(Background) 
        screen.blit(ROCKETS, gameRect)
        screen.blit(HEALTH, gameRect2)


        for missile in bullet:
            missile.display()
            missile.move()
            delete_bullets(missile)

        for rocket in rockets:
            rocket.display()
            rocket.move()
            delete_bullets(rocket)


        bullet_hit(bullet,my_particles)
        rocket_hit(rockets,my_particles)


        player.move()
        player.bounce()
        player.display()

        for pu in PowerUps:
            pu.display()
            power_up(player, PowerUps)

        for particle in my_particles:
            player_collide(player, particle)
            
        if player.lives == -1:
            game_over_screen()
            time.sleep(2)
            s = False      


        for i,particle in enumerate(my_particles):
            particle.move()
            particle.bounce()
            for particle2 in my_particles[i+1:]:
                collide(particle,particle2)

            particle.display()   

        level_cleared(my_particles)
        

        pg.display.flip()





Level1()



        
