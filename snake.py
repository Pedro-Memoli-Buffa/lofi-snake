import pygame
import random
import os

os.chdir('.\\snakeFiles')

pygame.init()
pygame.font.init()


width = 960
height = 640


black = (0,0,0)
white = (255,255,255)


gameDisplay = pygame.display.set_mode((width, height))


clock = pygame.time.Clock()


mainMenuBg = pygame.image.load('mainMenu.png')
gameBG = pygame.image.load('gameBG.png')


snakeSkin1 = pygame.image.load('snakeSkin1.png')

foodSkin1 = pygame.image.load('foodSkin1.png')

pixelFont = pygame.font.Font('Peepo.ttf', 30, bold = True)


saveData = {
    'bestScore' : 0
}


gameRunning = True


pygame.mixer.music.load('snake ST 1.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)



#Funcion drawText que funciona en todas las clases
def drawText(fontObject, text, location):
    textSurface = fontObject.render(text, False, (0, 0, 0))
    gameDisplay.blit(textSurface, location)





class Snake:
    def __init__(self, startingPosition, skin):
        self.headPosition = startingPosition

        self.skin = skin

        secondPart = (self.headPosition[0] - 1, self.headPosition[1])
        thirdPart = (self.headPosition[0] - 2, self.headPosition[1])
        self.previousFragmentation = [thirdPart, secondPart, self.headPosition]
        self.fragmentation = [thirdPart, secondPart, self.headPosition]


        self.originalFragmentation = [thirdPart, secondPart, self.headPosition]


    #Position es una funcion vectorial que a partir de un (x, y) te da la posicion de ese valor en el juego
    def position(self, x, y):
        return (212 + 30 * x, 25 + 30 * y)



    def move(self, direction, eating):
        if direction == 'right':
            newHead = (self.headPosition[0] + 1, self.headPosition[1])


        if direction == 'left':
            newHead = (self.headPosition[0] - 1, self.headPosition[1])      


        if direction == 'up':
            newHead = (self.headPosition[0], self.headPosition[1] - 1)


        if direction == 'down':
            newHead = (self.headPosition[0], self.headPosition[1] + 1) 



        self.previousFragmentation = [] + self.fragmentation

        self.fragmentation.append(newHead)
        self.headPosition = newHead

        #Si come que no elimine la cola
        if eating == False:
           self.fragmentation.pop(0)


    #Dibuja cada cuadrado con las posiciones dadas pos self.fragmentation()
    def draw(self):
        for boxPosition in self.fragmentation:
            boxCoordinates = self.position(boxPosition[0], boxPosition[1])
            gameDisplay.blit(self.skin, boxCoordinates)



    #Detecta si ocurrio una colision
    def detectColition(self):
        #Verifica si se excedio el limite del mapa
        for position in self.fragmentation:
            if position[0] < 0 or position[0] > 17 or position[1] < 0 or position[1] > 17:
                return True



        #Compara la cantidad de elementos de la lista como "conjunto" (sin elementos repetidos) con la lista original. Si son dif -> hay colision.
        if len(set(self.fragmentation)) != len(self.fragmentation):
            return True

        else:
            return False



    def restart(self, gameSpeed):
        self.fragmentation = [] + self.originalFragmentation
        self.headPosition = self.originalFragmentation[-1]



        #Timer de 2 segundos hasta reiniciar
        n = 0

        while True:
            #Para cada evento del juego
            for event in pygame.event.get():

                #Para poder quitear
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


            for boxPosition in self.previousFragmentation:
                boxCoordinates = self.position(boxPosition[0], boxPosition[1])
                gameDisplay.blit(self.skin, boxCoordinates)


            if n > 12:
                break

            n += 1

            pygame.display.update()

            clock.tick(gameSpeed)                  






class Food:
    def __init__(self, skin, unavailablePositions):
        self.skin = skin

        #Itera por un numero mayor a la cantidad de posiciones posibles (es simbolico solo no puede hacerlo en 3)
        for i in range(324):
            possibleFoodPosition = (random.randint(1, 17), random.randint(1, 17))

            if possibleFoodPosition not in unavailablePositions:
                self.foodPosition = possibleFoodPosition
                break



    def position(self, x, y):
        return (212 + 30 * x, 25 + 30 * y)



    def draw(self):
        boxCoordinates = self.position(self.foodPosition[0], self.foodPosition[1])
        gameDisplay.blit(self.skin, boxCoordinates)


    def newFood(self, unavailablePositions):
        #Itera por un numero mayor a la cantidad de posiciones posibles
        for i in range(324):
            possibleFoodPosition = (random.randint(1, 17), random.randint(1, 17))

            if possibleFoodPosition not in unavailablePositions:
                self.foodPosition = possibleFoodPosition
                break







class Score:
    def __init__(self):
        self.bestScore = saveData['bestScore']
        self.score = 0


    def draw(self):
        #Draw score
        drawText(pixelFont, str(self.score), (250, 600))

        #Draw best score
        drawText(pixelFont, str(self.bestScore), (860, 600))


    def increaseScore(self):
        self.score += 1


    def modifyBestScore(self, newScore):
        saveData['bestScore'] = newScore
        self.bestScore = newScore


    def restartScore(self):
        self.score = 0







class MainMenu:
    def __init__(self):
        pass


    def run(self):
        menuRunning = True
        

        while menuRunning:
            #Para cada evento del juego
            for event in pygame.event.get():
                leftClick = pygame.mouse.get_pressed()[0]
                mousePosition = pygame.mouse.get_pos() 

                #Para poder quitear
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


                #Si se hizo click
                if leftClick == 1:

                    #Se hizo click en Game
                    if mousePosition[0] in range(630, 850) and mousePosition[1] in range(180, 275):
                        return "game"



            gameDisplay.blit(mainMenuBg, (0,0))


            pygame.display.update()


            clock.tick(60)          





class Game:
    def __init__(self):
        pass


    def run(self):
        snake = Snake((9,9), snakeSkin1)
        food = Food(foodSkin1, snake.fragmentation)
        score = Score()

        gameRunning = True

        direction = 'right'

        gameSpeed = 5

        startCounter = 0
        finishCounter = 0

        colition = False
        

        while gameRunning:
            #Para cada evento del juego
            for event in pygame.event.get():

                #Para poder quitear
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


                if event.type == pygame.KEYDOWN:

                    if direction != 'left' and event.key == pygame.K_d:
                        direction = 'right'

                    elif direction != 'right' and event.key == pygame.K_a:
                        direction = 'left'                      

                    elif direction != 'down' and event.key == pygame.K_w:
                        direction = 'up'

                    elif direction != 'up' and event.key == pygame.K_s:
                        direction = 'down'

                    #Utilizo break para que no tome en cuenta 2 eventos de KEYDOWN y haya bug.
                    break


            #Dibuja el fondo
            gameDisplay.blit(gameBG, (0,0))


            #Cadena logica a partir de haber agarrado comida.
            if food.foodPosition == snake.headPosition:
                eating = True
                food.newFood(snake.fragmentation)
                score.increaseScore()
                if score.score > score.bestScore:
                    score.modifyBestScore(score.score)

                pygame.display.update()

            else:
                eating = False


            food.draw()
            score.draw()
 

            #Espera 2 segundos para empezar a moverse.
            if startCounter < gameSpeed * 3:
                startCounter += 1
            else:
                snake.move(direction, eating)
            
            
            #Detectar colision
            if snake.detectColition() == True:
                snake.restart(gameSpeed)
                score.restartScore()
                direction = 'right'
                colition = True


            #Dibuja la serpiente
            if colition != True:
                snake.draw() 


            pygame.display.update()



            clock.tick(gameSpeed)

            colition = False 
            




class App:
    def __init__(self, state):
        self.state = state
        self.mainMenu = MainMenu()
        self.game = Game()


    def run(self):
        if self.state == 'mainMenu':

            while gameRunning:
                ramification = self.mainMenu.run()

                if ramification == 'game':
                    self.game.run()


        #Estas 2 opciones son para testeo
        elif self.state == 'game':

            self.game.run()





app = App('mainMenu')
app.run()

pygame.quit()
exit()