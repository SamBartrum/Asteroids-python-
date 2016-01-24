import pygame as pg , random, math, time
from gameclasses import *


# Make the entire game a class so things are more modulates - although won't want more than one instance

images = {}  
sounds = {}
font = 'freesansbold.ttf'

height = 800
width = 800



def loadMedia():

	images['shipslow'] = pg.image.load("images/shipslow.png")
	images['shipfast'] = pg.image.load("images/shipfast.png")
	images['planets'] = [pg.image.load("images/planet1.png"),pg.image.load("images/planet2.png"),pg.image.load("images/planet3.png"),pg.image.load("images/planet4.png"),pg.image.load("images/planet5.png"),pg.image.load("images/planet6.png")]
	images['powerups'] = {"Life": pg.image.load("images/life.png"), "Rocket": pg.image.load("images/rocket.png") }  

		 
	sounds['fireSE'] = pg.mixer.Sound('sounds/fire.wav')
	sounds['powerSE'] = pg.mixer.Sound('sounds/Power_Up.wav')
	sounds['explosionSE'] = pg.mixer.Sound('sounds/Explosion.wav')
	sounds['lifelostSE'] = pg.mixer.Sound('sounds/Player_death.wav')





class Level():

	PlayerSurvived = True

	def __init__(self, no_particles):
		self.no_particles = no_particles
		Survived = True

	def makeSprites(self):

		self.player = Player((width/2, height/2),0, images['shipslow'])
		self.powerup1 = PowerUp((50, height/2), images['powerups']['Rocket'], "weapon")
		self.powerup2 = PowerUp((width-50, height/2), images['powerups']['Life'], "life")
		PowerUp.PowerUps.append(self.powerup1)
		PowerUp.PowerUps.append(self.powerup2)

		for n in range(self.no_particles):
			size = random.choice([20,40])
			x = (random.randint(size, width/3 - size),random.randint(2*width/3 , width - size) )  #Two regions where the player does not spawn
			y = (random.randint(size,height/3 - size),random.randint(2*height/3, height - size) )
			a = random.randint(0, len(images['planets'])-1)
			b = random.choice([0,1])
			c = random.choice([0,1])
			angle = random.uniform(0, math.pi * 2)
			particle = Planet((x[b],y[c]),size,angle,0, images['planets'][a])
			particle.setSpeed()
			


	def player_collide(self,player, p2):
		dx = player.x - p2.x
		dy = player.y - p2.y
		
		dist = math.hypot(dx, dy)
		thing = 0.5*(player.size+p2.size -dist+1) #calculates how much they have overlapped
		
		if dist < player.size/2 + p2.size:
			player.lives -= 1
			sounds['lifelostSE'].play()
			player.player_reset(width/2, height/2)
			player.image = images['shipslow']
			time.sleep(2)


			   

	def bullet_hit(self,bullets,particles):
		for missile in bullets:
			for particle in particles:
				dx = missile.x - particle.x
				dy = missile.y - particle.y

				dist = math.hypot(dx,dy)
				if dist < missile.size + particle.size:
					if particle.size == 20:
						particles.remove(particle)
						bullets.remove(missile)
						sounds['explosionSE'].play()
					else:
						particle.size = 20
						bullets.remove(missile) 
						sounds['explosionSE'].play()


	def rocket_hit(self,rockets,particles):
		test = 0
		for rocket in rockets:
			for particle in particles:
				dx = rocket.x - particle.x
				dy = rocket.y - particle.y

				dist = math.hypot(dx,dy)
				if dist < rocket.size + particle.size:
					particles.remove(particle)
					sounds['explosionSE'].play()
					
				

	def power_up(self,player,pulist):
		for pu in pulist:
			dx = player.x - pu.x
			dy = player.y - pu.y
			dist = math.hypot(dx,dy)
			if dist < pu.size + player.size:
				pulist.remove(pu)
				sounds['powerSE'].play()
				if pu.kind == "weapon":
					player.no_rockets +=2
				if pu.kind == "life":
					player.lives +=1  
			
			
	def game_over_screen(self):
		GO = SCORE.render("YOU HAVE DIED", True, (255,0,0))
		gameRect3 = GO.get_rect()
		gameRect3.center = (width/2,height/2)
		screen.blit(GO, gameRect3)
		pg.display.flip()
		time.sleep(1.5)


	def level_cleared(self,list):
		if len(list) == 0:
			WON = SCORE.render("LEVEL CLEARED", True, (255,255,255))
			gameRect3 = WON.get_rect()
			gameRect3.center = (width/2,height/2)
			screen.blit(WON, gameRect3)
			pg.display.flip()
			time.sleep(1.5)
			return True






	def Run(self):

		loop = True

		while loop:

			ROCKETS = SCORE.render("Rockets: " + str(self.player.no_rockets), True, (255,255,255))
			gameRect = ROCKETS.get_rect()
			gameRect.midtop = (6.5*width/8  , 10)

			HEALTH = SCORE.render("Lives: " + str(self.player.lives), True, (255,255,255))
			gameRect2 = HEALTH.get_rect()
			gameRect2.midtop = (1.5 *width /8, 10)


			for event in pg.event.get():
				if event.type == pg.QUIT:
					pygame.quit()

				elif event.type == pg.KEYDOWN:
					
					if event.key == pg.K_LEFT:
						self.player.image = images['shipslow']  
						self.player.speed = 5
						self.player.angle = math.pi/2

					if event.key == pg.K_RIGHT:
						self.player.image = images['shipslow']  
						self.player.speed = 5
						self.player.angle = - math.pi/2

					if event.key == pg.K_UP:
						self.player.image = images['shipslow']  
						self.player.speed = 5
						self.player.angle = math.pi

					if event.key == pg.K_DOWN:
						self.player.image = images['shipslow']  
						self.player.speed = 5
						self.player.angle = 0

					if event.key == pg.K_SPACE:  
						self.player.image = images['shipslow']         
						Bullet( (self.player.x+self.player.size/4, self.player.y+self.player.size/4), self.player.angle, 0)
						sounds['fireSE'].play()
					
					if event.key == pg.K_RETURN:
						self.player.image = images['shipslow']
						if self.player.no_rockets >0:
							Rocket( (self.player.x+self.player.size/4, self.player.y+self.player.size/4), self.player.angle, 0)
							self.player.no_rockets -= 1
							sounds['fireSE'].play()
						else:
							print "no"
					if event.key == pg.K_TAB:
						self.player.image = images['shipfast']
						self.player.speed = 20  


				

			screen.fill(Background) 
			screen.blit(ROCKETS, gameRect)
			screen.blit(HEALTH, gameRect2)

			# Evolve sprite, not the fastest but as number of particles is small this is not a problem.
			Bullet.BulletEvolve(screen)
			Rocket.RocketEvolve(screen)
			self.player.PlayerEvolve(screen)


			self.bullet_hit(Bullet.Bullets,Planet.Planets)
			self.rocket_hit(Rocket.Rockets, Planet.Planets)


			for pu in PowerUp.PowerUps:
				pu.display(screen)
				self.power_up(self.player, PowerUp.PowerUps)

			for planet in Planet.Planets:
				self.player_collide(self.player, planet)
				
			if self.player.lives == -1:

				Level.PlayerSurvived = False
				self.game_over_screen()
				loop = False
				      


			for i, planet in enumerate(Planet.Planets):
				planet.move()
				planet.bounce()
				for planet2 in Planet.Planets[i+1:]:
					Planet.collide(planet,planet2)

				planet.display(screen)   

			# Check if the level is cleared    
			if self.level_cleared(Planet.Planets):
				Level.PlayerSurvived = True
				loop = False
			

			pg.display.flip()



def rungame():
	i = 1
	while Level.PlayerSurvived == True:
		new = Level(i)
		new.makeSprites()
		new.Run()
		del new
		i+=1

# Put main in a function so that we can test this module better
def main():

	s = True

	while s:

		screen.fill((0,0,0))
		textpos = Title.get_rect()
		textpos.centerx = screen.get_rect().centerx
		screen.blit(Title, textpos)
		screen.blit(Instructions, (40,200))
		pg.display.flip()
   

		for event in pg.event.get():
			if event.type == pg.QUIT:
					s = False
			if event.type == pg.KEYDOWN:

				# We start the game loop over the levels
				if event.key == pg.K_SPACE:
					rungame()	
				  
				# We quit the game	
				if event.key == pg.K_ESCAPE:
					s = False
   

	   	Level.PlayerSurvived = True


if __name__ == "__main__":

	pg.init()
	CoverText = pg.font.Font(font, 40)
	SCORE = pg.font.Font(font, 20)
	Background = (0,0,0)
	screen = pg.display.set_mode((height,width))
	pg.display.set_caption("Asteroids")
	Instructions = CoverText.render("Press space to play or escape to quit", 10, (0,255,0))
	Title = CoverText.render("Asteroids", 1, (255, 255,255))

	loadMedia()
   
	main()
   

	   










































