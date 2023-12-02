import sqlite3
import pygame
import pygame as pg
import time
import random


class BaseConstructor:
    def __init__(self,baseName):
        self.baseName = baseName
        connection = sqlite3.connect(f'{baseName}.db')
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        nickname TEXT UNIQUE ON CONFLICT IGNORE,
        score INTEGER

        )
        ''')

        connection.commit()
        connection.close()

    def print_base(self):
        connection = sqlite3.connect(f'{self.baseName}.db')
        cursor = connection.cursor()
        cursor.execute("SELECT nickname, score FROM Users ORDER BY -score")
        users = cursor.fetchall()
        connection.close()
        return users

    def insert(self, nick):
        connection = sqlite3.connect(f'{self.baseName}.db')
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO Users (nickname, score) VALUES ('{nick}', 0)")
        connection.commit()
        connection.close()

    def update (self, nick, s):
        connection = sqlite3.connect(f'{self.baseName}.db')
        cursor = connection.cursor()
        cursor.execute(f"SELECT nickname, score FROM Users WHERE nickname = '{nick}'")
        score = cursor.fetchall()
        if s>int(score[0][1]):
            cursor.execute('UPDATE Users SET score = ? WHERE nickname = ?', (s, nick))
        connection.commit()
        connection.close()

class PlayersWindow(BaseConstructor):
    base = BaseConstructor("users")
    players = base.print_base()
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((350, 480))
        font = pygame.font.Font(None, 32)
        font2 = pygame.font.Font(None, 45)
        font3 = pygame.font.Font(None, 26)
        clock = pygame.time.Clock()
        input_box = pygame.Rect(20, 40, 142, 32)
        text_lable = font2.render("Enter Your Name Here: ", False, pygame.Color('crimson'))
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if input_box.collidepoint(event.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            self.nickname = text
                            self.base.insert(text)
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            screen.fill((30, 30, 30))
            # Render the current text.
            txt_surface = font.render(text, True, color)
            # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            # Blit the text.
            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))

            screen.blit(text_lable, (0, 0))
            y = 80
            for player in self.players:
                text_lable2 = font3.render(player[0]+" ---> "+str(player[1]), False, pygame.Color("green")) 
                screen.blit(text_lable2, (0, y))
                y+=20


            # Blit the input_box rect.
            pygame.draw.rect(screen, color, input_box, 2)

            pygame.display.flip()
            clock.tick(30)

class Game(PlayersWindow):
    def __init__(self):
        pygame.init()
        self.player= PlayersWindow()
        self.base = BaseConstructor("users")

        self.white = (255, 255, 255)
        self.yellow = (255, 255, 102)
        self.black = (0, 0, 0)
        self.red = (213, 50, 80)
        self.green = (0, 255, 0)
        self.blue = (50, 153, 213)
         
        self.dis_width = 600
        self.dis_height = 400
         
        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption('Snake Game by Pythonist')
         
        self.clock = pygame.time.Clock()
         
        self.snake_block = 10
        self.snake_speed = 8
         
        self.font_style = pygame.font.SysFont("bahnschrift", 18)
        self.score_font = pygame.font.SysFont("comicsansms", 35)

        self.gameLoop()


     
    def Your_score(self, score):
        value = self.score_font.render("Your Score: " + str(score), True, self.yellow)
        self.dis.blit(value, [0, 0])
     
     
     
    def our_snake(self,snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(self.dis, self.black, [x[0], x[1], self.snake_block, self.snake_block])
     
     
    def message(self, msg, color):
        mesg = self.font_style.render(msg, True, color)
        font3 = pygame.font.Font(None, 26)
        y = 80
        players = self.base.print_base()
        for player in players:
            text_lable2 = font3.render(player[0]+" ---> "+str(player[1]), False, pygame.Color("yellow")) 
            self.dis.blit(text_lable2, (0, y))
            y+=20
        self.dis.blit(mesg, [240, 20])

    def gameLoop(self):
        game_over = False
        game_close = False
     
        x1 = self.dis_width / 2
        y1 = self.dis_height / 2
     
        x1_change = 0
        y1_change = 0
     
        snake_List = []
        Length_of_snake = 1
     
        foodx = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0
     
        while not game_over:
     
            while game_close == True:
                self.dis.fill(self.blue)
                self.message("You Lost! Press C-Play Again or Q-Quit", self.red)
                self.Your_score(Length_of_snake - 1)
                pygame.display.update()
     
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            self.gameLoop()
     
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        x1_change = -self.snake_block
                        y1_change = 0
                    elif event.key == pygame.K_d:
                        x1_change = self.snake_block
                        y1_change = 0
                    elif event.key == pygame.K_w:
                        y1_change = -self.snake_block
                        x1_change = 0
                    elif event.key == pygame.K_s:
                        y1_change = self.snake_block
                        x1_change = 0

                    if event.key == pygame.K_LEFT:
                        x1_change = -self.snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = self.snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -self.snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = self.snake_block
                        x1_change = 0
     
            if x1 >= self.dis_width or x1 < 0 or y1 >= self.dis_height or y1 < 0:
                game_close = True
            x1 += x1_change
            y1 += y1_change
            self.dis.fill(self.blue)
            pygame.draw.rect(self.dis, self.green, [foodx, foody, self.snake_block, self.snake_block])
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]
     
            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True
     
            self.our_snake(self.snake_block, snake_List)
            self.Your_score(Length_of_snake - 1)
     
            pygame.display.update()
     
            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0
                Length_of_snake += 1
                self.base.update(self.player.nickname, Length_of_snake - 1)
     
            self.clock.tick(self.snake_speed)
        pygame.quit()
        quit()


if __name__ == "__main__":
    game = Game()

