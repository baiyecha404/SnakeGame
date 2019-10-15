import sys
import time
from random import randint
import pygame

pygame.init()
pygame.display.set_caption("Snake")
screen = pygame.display.set_mode((750, 750), 0, 32)  # pygame.FULLSCREEN
pygame.mouse.set_visible(0)

# Background
background = pygame.Surface(screen.get_size())
print(screen.get_size())
background = background.convert()
background_color = (100, 100, 255)
background.fill(background_color)


class Board:
    def __init__(self, size):
        self.size = size
        self.content = [[0 for _ in range(size[0])] for _ in range(size[1])]
        self.content[size[0] // 2][size[1] // 2] = 1

    def print_board(self):
        for line in self.content:
            print(line)
        print()

    def generate_food(self):
        tmp = []
        for row in range(self.size[0]):
            for column in range(self.size[1]):
                if self.content[row][column] == 0:
                    tmp.append((row, column))
        choice = randint(0, len(tmp) - 1)
        print(tmp)
        self.content[tmp[choice][0]][tmp[choice][1]] = 2

    def draw(self, screen, snake):
        for row in range(self.size[0]):
            for column in range(self.size[1]):
                # print(self.content, "row:", row, "column:", column)
                if self.content[row][column] == 1:
                    if row == snake[0][0] and column == snake[0][1]:
                        pygame.draw.rect(screen, (180, 80, 100),
                                         [column * 70, row * 70, 50, 50])
                    else:
                        pygame.draw.rect(screen, (200, 100, 100),
                                         [column * 70, row * 70, 50, 50])
                elif self.content[row][column] == 2:
                    pygame.draw.rect(screen, (100, 200, 100),
                                     [column * 70, row * 70, 50, 50])
        if len(snake) > 1:
            for i in range(len(snake) - 1):
                if snake[i][0] == snake[i + 1][0]:
                    pygame.draw.rect(
                        screen, (190, 90, 100),
                        [(snake[i][1] + snake[i + 1][1]) // 2 * 70 + 50,
                         (snake[i][0] + snake[i + 1][0]) // 2 * 70, 20, 50])
                else:
                    pygame.draw.rect(screen, (190, 90, 100), [
                        (snake[i][1] + snake[i + 1][1]) // 2 * 70,
                        (snake[i][0] + snake[i + 1][0]) // 2 * 70 + 50, 50, 20
                    ])

    def snake_move(self, snake, press):
        x = snake[0][0]
        y = snake[0][1]
        dx = [0, -1, 1, 0, 0]
        dy = [0, 0, 0, -1, 1]
        # print(snake)
        for i in range(1, 5):
            if press == i:
                # 判断越界
                if 0 <= x + dx[i] < self.size[
                        0] and 0 <= y + dy[i] < self.size[1]:
                    # 判断撞身体
                    if self.content[x + dx[i]][y + dy[i]] != 1:
                        flag = 1
                        if self.content[x + dx[i]][y + dy[i]] == 0:
                            self.content[snake[-1][0]][snake[-1][1]] = 0
                            del snake[-1]
                            flag = 0
                        snake.insert(0, (x + dx[i], y + dy[i]))
                        self.content[x + dx[i]][y + dy[i]] = 1
                        if flag:
                            return 1
                    else:
                        return 2
                else:
                    return 2
        print("snake", snake)
        # 0: 没吃 1: 吃了 2: 结束


class Space_menu:

    # Define the initalize self options
    def __init__(self, *options):
        self.options = options
        self.x = 0
        self.y = 0
        self.font = pygame.font.Font(None, 32)
        self.option = 0
        self.width = 1
        self.color = [0, 0, 0]
        self.hcolor = [0, 0, 0]
        self.height = len(options) * self.font.get_height()
        for o in options:
            text = o[0]
            ren = self.font.render(text, 1, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()

    # Draw the menu
    def draw(self, surface):
        i = 0
        for o in self.options:
            if i == self.option:
                clr = self.hcolor
            else:
                clr = self.color
            text = o[0]
            ren = self.font.render(text, 1, clr)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            surface.blit(ren, (self.x, self.y + i * self.font.get_height()))
            i += 1

    # Handle events
    def update(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    self.option -= 1
                elif e.key == pygame.K_DOWN:
                    self.option += 1
                elif e.key == pygame.K_RETURN:
                    self.options[self.option][1]()
            if self.option > len(self.options) - 1:
                self.option = 0
            elif self.option < 0:
                self.option = len(self.options) - 1

    # Position of menu
    def set_pos(self, x, y):
        self.x = x
        self.y = y

    # Font Style
    def set_font(self, font):
        self.font = font
        for o in self.options:
            text = o[0]
            ren = self.font.render(text, 1, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()

    # Highlight Color
    def set_highlight_color(self, color):
        self.hcolor = color

    # Font Color
    def set_normal_color(self, color):
        self.color = color

    # Font position
    def center_at(self, x, y):
        self.x = x - (self.width / 2)
        self.y = y - (self.height / 2)


def pause():
    pygame.event.wait()
    while True:
        event = pygame.event.wait()
        if event.key == pygame.K_ESCAPE:
            break
        if event.key == pygame.K_q:
            quit()


def quit():
    pygame.quit()
    sys.exit()


def receive_keyboard():
    keypad_dict = {
        pygame.K_UP: 1,
        pygame.K_DOWN: 2,
        pygame.K_LEFT: 3,
        pygame.K_RIGHT: 4,
        pygame.K_z: 5,
    }
    press = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # print(event.key)
            if event.key == pygame.K_ESCAPE:
                pause()
            if event.key == pygame.K_q:
                exit()
            if event.key in keypad_dict:
                press = keypad_dict[event.key]
            # 0:UP 1:DOWN 2:LEFT 3:RIGHT 4:LSHIFT 5:z
    if press != None:
        return press


def about_menu():
    # About Menu Text
    # Title for Option Menu
    menuTitle = Space_menu(["Snake"])

    info = Space_menu(["Use arrow key to move your snake."], [""], [""], [""],
                      [""], [""], [""], [""],
                      ["       PRESS ESC TO RETURN          "],
                      ["       PRESS ESCAPE TO PAUSE        "],
                      ["       PRESS Q TO QUIT          "])

    # About Title Font color, aligment, and font type
    menuTitle.set_font(pygame.font.Font(None, 60))
    menuTitle.center_at(400, 150)
    menuTitle.set_highlight_color((255, 255, 255))

    # About info Font color, aligment, and font type
    info.center_at(400, 320)
    info.set_highlight_color((255, 255, 255))
    info.set_normal_color((200, 200, 255))

    clock = pygame.time.Clock()
    keepGoing = True

    while keepGoing:
        clock.tick(30)

        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                if event.key == pygame.K_q:
                    exit()

        # Draw
        screen.blit(background, (0, 0))
        menuTitle.draw(screen)
        info.draw(screen)
        pygame.display.flip()


def read_high_score_file(file_name):
    file = open(file_name, mode='r').readlines()
    score_list = []
    for line in file:
        line = line.strip(",[]\n").split(",")
        score_list.append([line[0][7:], int(line[1][6:])])
    print(score_list)
    print(score_list[0])
    return score_list


def write_high_score_file(file_name, score_list):
    file = open(file_name, mode='w')
    for i in range(min(len(score_list), 10)):
        print("[player:" + score_list[i][0] + ",score:" +
              str(score_list[i][1]) + "],",
              file=file)
    file.close()


def end_game(score):
    screen.fill(background_color)
    pygame.display.update()
    player_name = "cyy"  ###########
    high_score_file_name = "C:/Users/cyy/Desktop/snake/high_score_list.dat"
    high_score_list = read_high_score_file(high_score_file_name)
    high_score_list.append([player_name, score, -1])
    high_score_list.sort(key=lambda x: x[1], reverse=True)

    my_font = pygame.font.SysFont("", 60)
    # text_surface = my_font.render("GAME OVER", True, (250, 250, 250))
    # screen.blit(text_surface, (200, 200 + i * 60))

    menuTitle = Space_menu(["Game over"])
    menuTitle.set_font(pygame.font.Font(None, 80))
    menuTitle.center_at(375, 150)
    menuTitle.set_highlight_color((250, 250, 250))
    menuTitle.draw(screen)
    pygame.display.flip()
    time.sleep(1)

    for j in range(5):
        screen.fill(background_color)
        for i in range(min(len(high_score_list), 7)):
            if (j & 1 == 0) or high_score_list[i][-1] != -1:
                text_surface = my_font.render(
                    "player:" + high_score_list[i][0] + " score:" +
                    str(high_score_list[i][1]), True, (250, 250, 250))
                screen.blit(text_surface, (200, 200 + i * 60))
        pygame.display.update()
        time.sleep(0.5)
    write_high_score_file(high_score_file_name, high_score_list)
    time.sleep(1)

    screen.fill(background_color)
    pygame.display.update()

    info = Space_menu(["Press ESC back to menu"])
    info.set_font(pygame.font.Font(None, 40))
    info.center_at(375, 375)
    info.set_highlight_color((255, 255, 255))

    keepGoing = True
    while keepGoing:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
            elif event.type == pygame.QUIT:
                keepGoing = False

        info.draw(screen)
        pygame.display.flip()


def game():
    max_fps = 3
    board = Board([11, 11])
    snake = [(board.size[0] // 2, board.size[1] // 2)]

    score = 0
    last_press = 1
    current_frame = 0
    board.generate_food()
    main_loop_start_time = time.time()
    screen.fill(background_color)
    pygame.display.update()
    game_is_on = True
    while game_is_on:
        if (time.time() - main_loop_start_time) * max_fps > current_frame:
            current_frame += 1
            press = receive_keyboard()
            if press == None:
                press = last_press
            else:
                last_press = press
            status = board.snake_move(snake, press)
            if status == 1:
                score += 100
                board.generate_food()
            elif status == 2:
                end_game(score)
                game_is_on = False

            screen.blit(background, (0, 0))
            board.print_board()
            board.draw(screen, snake)
            pygame.display.update()


def main():
    # Title
    menuTitle = Space_menu(["Snake"])
    menuTitle.set_font(pygame.font.Font(None, 60))
    menuTitle.center_at(375, 150)
    menuTitle.set_highlight_color((255, 255, 255))

    # Menu settings
    menu = Space_menu(["Start", game], ["About", about_menu], ["Exit", quit])
    menu.center_at(375, 375)
    menu.set_highlight_color((255, 255, 255))
    menu.set_normal_color((200, 200, 255))

    clock = pygame.time.Clock()
    keepGoing = True

    while True:
        clock.tick(30)

        # Events
        events = pygame.event.get()

        # Update Menu
        menu.update(events)

        # Handle quit event
        for e in events:
            if e.type == pygame.QUIT:
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    quit()

        # Draw
        screen.blit(background, (0, 0))
        menu.draw(screen)
        menuTitle.draw(screen)

        pygame.display.flip()


# TODO 难度系统 修改速度和ai难度
if __name__ == "__main__":
    main()
