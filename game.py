import os
from enum import Enum

import pyxel
import Box2D
from Box2D import b2

import main
import scenes

PPM = 16.0  # pixels per meter
TARGET_FPS = 30
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 224, 126
SCREEN_Y_ZERO_OFFSET = 120
STAGE_WIDTH_M = 70  # m
STAGE_ITEMEND_X_M = 67  # ここまでしかものが置かない

SCREEN_WIDTH_M = int(SCREEN_WIDTH/PPM)
SCREEN_HIGHT_M = int(SCREEN_HEIGHT/PPM)

DEBUG_DRAW=False

STAGE_NUM = 12
GAME_TIMEOUT_S = 60 # 秒

# プレイヤーの移動の起点
PLAYER_SCROLL_X_M = 3

# プレイヤーの移動に合わせた全体の描画の移動量
DRAW_OFFSET_X = 0
DRAW_OFFSET_X_M = 0

SPRITE_SETS = [
    [0,0,16,16], # プレイヤー
    [0,16,16,16],
    [0, 48, 16, 16], # コイン
    [0, 64, 16, 16], # わな
    [0, 32, 16, 16], # 旗
]
class SpriteSet(Enum):
    PLAYER = 0
    COIN = 2
    TRAP = 3
    FLAG = 4

    @staticmethod
    def map_rect(n):
        if isinstance(n, SpriteSet):
            n = n.value
        if n<0 or n >= len(SPRITE_SETS):
            return None
        return SPRITE_SETS[n]

def draw_sprite_world(pos, sprite_n):
    pos = world_to_draw_pos(pos)

    r = SpriteSet.map_rect(sprite_n)
    if r is None:
        return
    w = r[2]
    h = r[3]


    pyxel.blt(pos[0]-w/2 + DRAW_OFFSET_X,
        pos[1]-h/2,
        0,
        r[0],r[1],r[2],r[3],
        11)

def draw_body_sprite(body, sprite_n):
    pos = body_pos(body)
    draw_sprite_world(pos, sprite_n)

def draw_sprite(pos, sprite_n):
    r = SpriteSet.map_rect(sprite_n)
    if r is None:
        return
    pyxel.blt(pos[0] + DRAW_OFFSET_X,
        pos[1],
        0,
        r[0],r[1],r[2],r[3],
        11)

# 描画の全体のオフセット値を設定
def set_draw_offset_x_m(offset_m):
    global DRAW_OFFSET_X_M
    global DRAW_OFFSET_X

    DRAW_OFFSET_X_M = offset_m
    DRAW_OFFSET_X = int(offset_m * PPM)

# ボディの位置を取得　ワールド座標
def body_pos(body):
    return body.transform * (0,0)

def set_body_pos(body, pos):
    body.transform = (pos, 0)


# ボディの位置を取得　描画座標
def body_draw_pos(body):
    return world_to_draw_pos(body.transform * (0,0))

# 位置をワールド座標から描画座標に変換
def world_to_draw_pos(pos):
    return int(pos[0]* PPM), int(SCREEN_Y_ZERO_OFFSET - pos[1] * PPM)

# ポリゴンを描画
# 引数は描画座標の位置
def draw_polygon(vertices, color):
    n = len(vertices)
    for i in range(n-1):
        pyxel.line(vertices[i][0] + DRAW_OFFSET_X, vertices[i][1],
            vertices[i+1][0] + DRAW_OFFSET_X, vertices[i+1][1],
            color)

    pyxel.line(vertices[n-1][0] + DRAW_OFFSET_X, vertices[n-1][1],
        vertices[0][0] + DRAW_OFFSET_X, vertices[0][1],
        color)

# ボディを描画
def draw_body(body, color):
    for fixture in body.fixtures:
        shape = fixture.shape

        if type(shape) is Box2D.b2PolygonShape:
            # print(shape.vertices)
            vertices = [(body.transform * v) * PPM for v in shape.vertices]
            vertices = [(int(v[0]), int(SCREEN_Y_ZERO_OFFSET - v[1])) for v in vertices]
            # print(vertices)
            draw_polygon(vertices, color)
        elif type(shape) is Box2D.b2CircleShape:
            pos = (body.transform * shape.pos) * PPM
            pos = int(pos[0]), int(SCREEN_Y_ZERO_OFFSET - pos[1])
#            print(pos)
            pyxel.circb(pos[0] + DRAW_OFFSET_X, pos[1], int(fixture.shape.radius*PPM), color)

def draw_center_x(text, y, color):
    w = len(text)*5
    pyxel.text(int((SCREEN_WIDTH-w)/2),
        y,
        text,
        color)

class GameMode(Enum):
    TITLE = 0
    MAIN = 1
    STAGE = 2
    END = 3


class Game:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.load(os.path.join(os.path.dirname(__file__), "main.pyxel"))


        self.mode = GameMode.TITLE
        self.coins = 0
        self.score = 0
        self.stage = 0
        self.stages = [False] * STAGE_NUM
        self.timecount = 1000*GAME_TIMEOUT_S

        self.next_mode = GameMode.TITLE
        self.next_param = {}

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.next_mode:
            self.goto_next_mode()

        self.scene.update()

        if self.is_gaming():
            self.timecount -= (1000/TARGET_FPS)
            if self.timecount <= 0:
                self.game_end()
                
    def goto_next_mode(self):
        next_scenes = {
            GameMode.TITLE: scenes.SceneTitle,
            GameMode.STAGE: scenes.SceneStageSelect,
            GameMode.MAIN: main.SceneMain,
            GameMode.END: scenes.SceneEnd,
        }
        self.mode = self.next_mode
        self.scene = (next_scenes[self.next_mode])(self.next_param)
        self.next_mode = None
        self.next_param = None

    def is_gaming(self):
        return self.mode == GameMode.STAGE or self.mode == GameMode.MAIN

    def draw(self):
        pyxel.cls(0)
        self.scene.draw()

        if self.is_gaming():
            t = "TIME: %02d:%02d.%03d  SCORE:%03d" % (int(self.timecount/60/1000), 
                int(self.timecount/1000)%60,
                self.timecount%1000,
                self.score)
            pyxel.text(10,3, t, 7)

    def move_scene(self, next_mode, next_param):
        self.next_mode = next_mode
        self.next_param = next_param

    def game_start(self):
        self.coins = 0
        self.score = 0
        self.stages = [False] * STAGE_NUM
        self.timecount = 1000*GAME_TIMEOUT_S

        self.move_scene(GameMode.STAGE, {})

    def game_end(self):
        self.move_scene(GameMode.END, {})

    def stage_start(self, stage):
        self.coins = 0
        self.stage = stage
        self.move_scene(GameMode.MAIN, {"stage": stage})

    def stage_end(self):
        self.score += (self.coins+5)
        self.coins = 0
        self.stages[self.stage] = True
        self.move_scene(GameMode.STAGE, {})


    def get_coin(self):
        self.coins += 1


game = None
def game_main():
    global game
    game = Game()
    game.run()
