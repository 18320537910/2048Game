import pygame
import pygame_gui
import sys
import random

from pygame_gui import UI_CONFIRMATION_DIALOG_CONFIRMED

from config import *


# 操作
def move_up(game_grid):
    moved = False
    score = 0
    for x in range(1, GRID_SIZE):
        for y in range(GRID_SIZE):
            if game_grid[x][y] != 0:
                current_x = x
                while current_x > 0 and game_grid[current_x - 1][y] == 0:
                    game_grid[current_x - 1][y] = game_grid[current_x][y]
                    game_grid[current_x][y] = 0
                    current_x -= 1
                    moved = True

                if current_x > 0 and game_grid[current_x - 1][y] == game_grid[current_x][y]:
                    game_grid[current_x - 1][y] *= 2
                    score += game_grid[current_x - 1][y]
                    game_grid[current_x][y] = 0
                    moved = True

    return game_grid, moved, score


def move_down(game_grid):
    moved = False
    score = 0
    for x in range(GRID_SIZE - 2, -1, -1):
        for y in range(GRID_SIZE):
            if game_grid[x][y] != 0:
                current_x = x
                while current_x < GRID_SIZE - 1 and game_grid[current_x + 1][y] == 0:
                    game_grid[current_x + 1][y] = game_grid[current_x][y]
                    game_grid[current_x][y] = 0
                    current_x += 1
                    moved = True

                if current_x < GRID_SIZE - 1 and game_grid[current_x + 1][y] == game_grid[current_x][y]:
                    game_grid[current_x + 1][y] *= 2
                    score += game_grid[current_x + 1][y]
                    game_grid[current_x][y] = 0
                    moved = True

    return game_grid, moved, score


def move_left(game_grid):
    moved = False
    score = 0

    for y in range(1, GRID_SIZE):
        for x in range(GRID_SIZE):
            if game_grid[x][y] != 0:
                current_y = y
                while current_y > 0 and game_grid[x][current_y - 1] == 0:
                    game_grid[x][current_y - 1] = game_grid[x][current_y]
                    game_grid[x][current_y] = 0
                    current_y -= 1
                    moved = True

                if current_y > 0 and game_grid[x][current_y - 1] == game_grid[x][current_y]:
                    game_grid[x][current_y - 1] *= 2
                    score += game_grid[x][current_y - 1]
                    game_grid[x][current_y] = 0
                    moved = True

    return game_grid, moved, score


def move_right(game_grid):
    moved = False
    score = 0

    for y in range(GRID_SIZE - 2, -1, -1):
        for x in range(GRID_SIZE):
            if game_grid[x][y] != 0:
                current_y = y
                while current_y < GRID_SIZE - 1 and game_grid[x][current_y + 1] == 0:
                    game_grid[x][current_y + 1] = game_grid[x][current_y]
                    game_grid[x][current_y] = 0
                    current_y += 1
                    moved = True

                if current_y < GRID_SIZE - 1 and game_grid[x][current_y + 1] == game_grid[x][current_y]:
                    game_grid[x][current_y + 1] *= 2
                    score += game_grid[x][current_y + 1]
                    game_grid[x][current_y] = 0
                    moved = True

    return game_grid, moved, score


# 添加新数字
def add_new_number(game_grid):
    empty_cells = [(x, y)
                   for x in range(GRID_SIZE)
                   for y in range(GRID_SIZE)
                   if game_grid[x][y] == 0]
    if empty_cells:
        x, y = random.choice(empty_cells)
        game_grid[x][y] = random.choice([2, 4])


# 得分情况
def draw_score(screen, score):
    font = pygame.font.Font(None, SCORE_FONT_SIZE)

    # Score text
    score_text = font.render(f"Score: {score}", True, FONT_COLOR)
    score_text_rect = score_text.get_rect(topleft=(10, SCREEN_SIZE[1] - 60))
    screen.blit(score_text, score_text_rect)

    # Best Score text
    best_score = load_best_score()
    best_score_text = font.render(f"Best Score: {best_score}", True, FONT_COLOR)
    best_score_text_rect = best_score_text.get_rect(topleft=(10, SCREEN_SIZE[1] - 30))
    screen.blit(best_score_text, best_score_text_rect)

    # Quit prompt text
    quit_prompt_text = font.render("Press F1 to quit", True, FONT_COLOR)
    quit_prompt_text_rect = quit_prompt_text.get_rect(topright=(SCREEN_SIZE[0] - 10, SCREEN_SIZE[1] - 60))
    screen.blit(quit_prompt_text, quit_prompt_text_rect)


# 是否结束
def is_game_over(game_grid):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if game_grid[x][y] == 0:
                return False
            if x < GRID_SIZE - 1 and game_grid[x][y] == game_grid[x + 1][y]:
                return False
            if y < GRID_SIZE - 1 and game_grid[x][y] == game_grid[x][y + 1]:
                return False
    return True


# 移动
def move(game_grid, direction):
    moved = False
    new_score = 0
    if direction == KEY_UP:
        game_grid, moved, new_score = move_up(game_grid)
    elif direction == KEY_DOWN:
        game_grid, moved, new_score = move_down(game_grid)
    elif direction == KEY_LEFT:
        game_grid, moved, new_score = move_left(game_grid)
    elif direction == KEY_RIGHT:
        game_grid, moved, new_score = move_right(game_grid)

    return game_grid, moved, new_score


# 记录和读取分数
BEST_SCORE_FILE = "best_score.txt"


def load_best_score():
    try:
        with open(BEST_SCORE_FILE, "r") as file:
            best_score = int(file.read().strip())
    except (FileNotFoundError, ValueError):
        best_score = 0

    return best_score


def save_best_score(best_score):
    with open(BEST_SCORE_FILE, "w") as file:
        file.write(str(best_score))


# 在这里，我们将添加 pygame_gui 相关的代码，以在游戏结束时显示一个弹窗
def show_game_over_dialog(screen, manager, final_score, best_score, new_record):
    game_over_dialog = pygame_gui.windows.UIConfirmationDialog(
        rect=pygame.Rect((screen.get_width() // 2 - 140, screen.get_height() // 2 - 90), (280, 180)),
        manager=manager,
        window_title="Game Over",
        action_long_desc=f"Final Score: {final_score}\nBest Score: {best_score}\n{'New Record!' if new_record else ''}",
        action_short_name="OK",
        blocking=True,
    )

    return game_over_dialog


# 弹出退出确认对话框
def show_confirmation_dialog(manager, current_score, best_score):
    dialog_width = 400
    dialog_height = 300
    dialog_title = "Quit Game"
    dialog_message = f"Are you sure you want to quit?\n\nYour current score: {current_score}\nBest score: {best_score}"

    dialog = pygame_gui.windows.UIConfirmationDialog(
        rect=pygame.Rect(SCREEN_SIZE[0] // 2 - dialog_width // 2, SCREEN_SIZE[1] // 2 - dialog_height // 2,
                         dialog_width, dialog_height),
        manager=manager,
        window_title=dialog_title,
        action_long_desc=dialog_message,
        action_short_name="QUIT",
        blocking=True,
    )

    return dialog


# 手动终止游戏
def handle_game_over(screen, time_delta, manager, score, game_grid):
    # 从文件加载最高分
    best_score = load_best_score()

    # 显示确认对话框
    confirmation_dialog = show_confirmation_dialog(manager, score, best_score)
    while confirmation_dialog.alive():
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            manager.process_events(event)

        manager.update(time_delta)

        screen.fill(BACKGROUND_COLOR)
        draw_board(screen, game_grid)
        draw_score(screen, score)
        manager.draw_ui(screen)

        pygame.display.flip()
        pygame.time.wait(50)


# 主流程
def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("2048")

    game_grid = initialize_game()
    score = 0

    manager = pygame_gui.UIManager(SCREEN_SIZE)

    clock = pygame.time.Clock()

    # 在游戏循环开始之前绘制初始游戏状态
    screen.fill(BACKGROUND_COLOR)
    draw_board(screen, game_grid)
    draw_score(screen, score)
    pygame.display.flip()

    while True:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # 手动结束游戏
            if event.type == UI_CONFIRMATION_DIALOG_CONFIRMED:
                save_best_score(score)
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                moved = False
                new_score = 0
                # 方向按钮
                if event.key in (KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT):
                    game_grid, moved, new_score = move(game_grid, event.key)
                # 退出按钮
                elif event.key == KEY_EXIT:
                    handle_game_over(screen, time_delta, manager, score, game_grid)

                if moved:
                    add_new_number(game_grid)
                    score += new_score
                    if is_game_over(game_grid):
                        best_score = load_best_score()  # 从文件加载最高分
                        new_record = False
                        if score > best_score:
                            new_record = True
                            save_best_score(score)  # 将新的最高分保存到文件

                        game_over_dialog = show_game_over_dialog(screen, manager, score, best_score, new_record)
                        while game_over_dialog.alive:
                            for event in pygame.event.get():
                                if event.type == QUIT:
                                    pygame.quit()
                                    sys.exit()
                                manager.process_events(event)

                            manager.update(time_delta)

                            screen.fill(BACKGROUND_COLOR)
                            draw_board(screen, game_grid)
                            draw_score(screen, score)
                            manager.draw_ui(screen)

                            pygame.display.flip()
                            pygame.time.wait(50)

                        pygame.quit()
                        sys.exit()

                manager.process_events(event)

                manager.update(time_delta)

                screen.fill(BACKGROUND_COLOR)
                draw_board(screen, game_grid)
                draw_score(screen, score)
                manager.draw_ui(screen)
                pygame.display.flip()
                pygame.time.wait(50)


# 指定的屏幕位置绘制卡片（方块）的值和背景色
def draw_tile(screen, value, rect):
    font = pygame.font.Font(None, 36)

    # 画背景
    pygame.draw.rect(screen, TILE_COLORS[value], rect)

    # 画数字
    if value != 0:
        text = font.render(str(value), True, FONT_COLOR)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)


# 绘制棋盘和数字方块
def draw_board(screen, game_grid):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            value = game_grid[x][y]
            rect = pygame.Rect(y * (SCREEN_SIZE[0] // GRID_SIZE) + GRID_PADDING,
                               x * (SCREEN_SIZE[1] // GRID_SIZE - 20) + GRID_PADDING,
                               SCREEN_SIZE[0] // GRID_SIZE - 2 * GRID_PADDING,
                               SCREEN_SIZE[1] // GRID_SIZE - 2 * GRID_PADDING - 20)
            pygame.draw.rect(screen, GRID_BACKGROUND_COLOR, rect)

            if value != 0:
                draw_tile(screen, value, rect)


# 初始化游戏
def initialize_game():
    game_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    for _ in range(2):
        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if game_grid[x][y] == 0:
                game_grid[x][y] = random.choice([2, 4])
                break

    return game_grid


if __name__ == "__main__":
    main()
