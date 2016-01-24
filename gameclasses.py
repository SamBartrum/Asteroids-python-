import math
import pygame as pg 

# The game classes live here

gravity = (0 , 0)
drag = 0.999
elasticity = 0.9

height = 800
width = 800
  



# This is the base class which the other classes will inherit from
class Particle(object):
    def __init__(self, (x, y), size, angle, speed, image):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.angle = angle
        self.image = image


    @staticmethod    
    def add_vectors( (angle1,length1), (angle2,length2)):
        x = length1 * math.sin(angle1) + length2 * math.sin(angle2)
        y = length1 * math.cos(angle1) + length2 * math.cos(angle2)

        length =  math.hypot(x,y)
        angle = math.atan2(x,y)
        return (angle,length)


    def display(self, screen):   
       
        temp = pg.transform.scale(self.image, (2*self.size, 2*self.size))
        screen.blit(temp,(self.x-self.size,self.y-self.size))

    def move(self):
        (self.angle, self.speed) = Particle.add_vectors((self.angle, self.speed), gravity)
        self.x -= math.sin(self.angle) * self.speed
        self.y += math.cos(self.angle) * self.speed
        self.speed *= drag


class Planet(Particle): 

    Planets = []

    def __init__(self, (x, y), size, angle, speed, image):
        super(Planet,self).__init__((x, y), size, angle, speed, image)
        Planet.Planets.append(self)

    def setSpeed(self):
         if self.size == 20:
            self.speed = 10
         else:
            self.speed = 5    


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

    # Takes two planet objects and sees if they have collided, updates positions appropriately        
    @staticmethod        
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

       




class Player(Particle):

    # Call the superclass constructor and extend, setting the size = 30
    def __init__(self, (x, y), angle, image):
        super(Player,self).__init__((x, y), 50, angle, 0, image)
        self.no_rockets = 0
        self.lives = 3
        self.status = 'alive'


    def display(self, screen):   # Rewrite using cases
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
          

    def boundaryconditions(self):
        if self.x > width - self.size:
            self.x = (self.size) 

        elif self.x < self.size:
            self.x = width - self.size

        if self.y > height - self.size:
            self.y = (self.size)

        elif self.y < self.size:
            self.y = height - self.size     


    def player_reset(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0        

    def PlayerEvolve(self,screen):
        self.move()
        self.boundaryconditions()
        self.display(screen)    
        
class Bullet(Particle):

    Bullets = []

    def __init__(self, (x, y), angle, image):
        super(Bullet,self).__init__( (x,y), 5, angle, 30, image)
        Bullet.Bullets.append(self)
        self.colour = (0,255,0)


    def display(self, screen):
        pg.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size)
  
    def deleteBullet(self):
        if self.x > width or self.x < 0 or self.y > height or self.y < 0:
            del self

    @staticmethod
    def BulletEvolve(screen):
        for bullet in Bullet.Bullets:
            bullet.display(screen)
            bullet.move()
            bullet.deleteBullet()



# Keep this a seperate class from Bullet to allow for future modifications
class Rocket(Particle):

    Rockets = []

    def __init__(self, (x, y), angle, image):
        super(Rocket,self).__init__( (x,y), 5, angle, 20, image)
        Rocket.Rockets.append(self)
        self.colour = (255,0,0)


    def display(self, screen):
        pg.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size)

    def deleteRocket(self):
        if self.x > width or self.x < 0 or self.y > height or self.y < 0:
            del self

    @staticmethod
    def RocketEvolve(screen):
        for rocket in Rocket.Rockets:
            rocket.display(screen)
            rocket.move()
            rocket.deleteRocket()

     




class PowerUp(Particle):

    PowerUps = []

    def __init__(self, (x, y),image, kind):
        super(PowerUp,self).__init__( (x,y), 15, 0, 30, image)
        self.kind = kind
        PowerUp.PowerUps.append(self)
    
    def display(self, screen):

        temp = pg.transform.scale(self.image, (2*self.size, 2*self.size))
        screen.blit(temp,(self.x-self.size/2,self.y-self.size/2))




# For testing
if __name__ == '__main__':

    sam = Player((0,0),0,"images/shipslow.png")
    print sam.size
    bullet = Bullet((0,0),0, "images/shipslow.png")
    print bullet.size

   











