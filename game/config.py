from pygame.locals import *

# ====================定义配置====================

# 定义全局常量
TILE_SIZE = 100  # 单个方块的尺寸（宽和高）
GRID_MARGIN = 20  # 方块之间的间距
ANIMATION_SPEED = 0.8  # 动画速度（0 到 1 之间的浮点数，1 表示最快速度）

# 颜色定义
BACKGROUND_COLOR = (250, 248, 239)
GRID_BACKGROUND_COLOR = (204, 192, 179)
TEXT_COLOR = (119, 110, 101)
TEXT_COLOR_LIGHT = (249, 246, 242)

# 方块颜色定义
TILE_COLORS = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    4096: (179, 46, 245),
    8192: (153, 30, 225),
    16384: (128, 0, 128),
    32768: (102, 0, 102),
}

# 文字颜色定义
TEXT_COLORS = {
    0: TEXT_COLOR,
    2: TEXT_COLOR,
    4: TEXT_COLOR,
    8: TEXT_COLOR_LIGHT,
    16: TEXT_COLOR_LIGHT,
    32: TEXT_COLOR_LIGHT,
    64: TEXT_COLOR_LIGHT,
    128: TEXT_COLOR_LIGHT,
    256: TEXT_COLOR_LIGHT,
    512: TEXT_COLOR_LIGHT,
    1024: TEXT_COLOR_LIGHT,
    2048: TEXT_COLOR_LIGHT,
    4096: TEXT_COLOR_LIGHT,
    8192: TEXT_COLOR_LIGHT,
    16384: TEXT_COLOR_LIGHT,
    32768: TEXT_COLOR_LIGHT,
}

FONT_SIZE = 36  # 字体大小

# 基本参数
SCREEN_SIZE = (400, 500)
GRID_SIZE = 4
GRID_PADDING = 10
BACKGROUND_COLOR = (187, 173, 160)
GRID_BACKGROUND_COLOR = (204, 192, 180)
FONT_COLOR = (119, 110, 101)
TITLE_FONT_SIZE = 36
SCORE_FONT_SIZE = 24

# 按键设置
KEY_UP = K_UP
KEY_DOWN = K_DOWN
KEY_LEFT = K_LEFT
KEY_RIGHT = K_RIGHT
# 退出键
KEY_EXIT = K_F1


# 屏幕尺寸计算
GRID_WIDTH = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * GRID_MARGIN
GRID_HEIGHT = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * GRID_MARGIN
SCREEN_SIZE = (GRID_WIDTH, GRID_HEIGHT)
