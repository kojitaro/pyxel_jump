import pyxel
from Box2D import b2

import game as g
import main

OUTSP = 20
INTERSP = 10

W = 4
H = 3

class SceneTitle():
    def __init__(self, p):
        self.color_counter = 0
    def update(self):
        if g.game.input.btnp(g.InputKey.A):
            g.game.game_start()

    def draw(self):
        self.color_counter += 1

        g.draw_center_x(
            "TITLE",
            g.SCREEN_HEIGHT/2-40,
            self.color_counter%16)
        g.draw_center_x(
            "HIT X Key",
            g.SCREEN_HEIGHT/2+16,
            7)

class SceneStageSelect():
    def __init__(self, p):
        self.selection = 0

    def update(self):
        sx = int(self.selection % W)
        sy = int(self.selection / W)

        if g.game.input.btnp(g.InputKey.LEFT):
            sx -= 1
        if g.game.input.btnp(g.InputKey.RIGHT):
            sx += 1
        if g.game.input.btnp(g.InputKey.UP):
            sy -= 1
        if g.game.input.btnp(g.InputKey.DOWN):
            sy += 1

        self.selection = (sx+W)%W + ((sy+H)%H)*W

        if g.game.input.btnp(g.InputKey.A):
            g.game.stage_start(self.selection)

    def draw(self):

        BOX_SIZE_W = int((g.SCREEN_WIDTH - OUTSP*2 - INTERSP*(W-1)) / W)
        BOX_SIZE_H = int((g.SCREEN_HEIGHT - OUTSP*2 - INTERSP*(H-1)) / H)

        for n in range(0,g.STAGE_NUM):
            x = int(n % W)
            y = int(n / W)

            px = OUTSP+(BOX_SIZE_W+INTERSP)*x
            py = OUTSP+(BOX_SIZE_H+INTERSP)*y
            c = 4 if self.selection == n else 7
            pyxel.rectb(px,
                py,
                px + BOX_SIZE_W,
                py + BOX_SIZE_H,
                c
            )

            pyxel.text(px+BOX_SIZE_W/2-3,
                py+BOX_SIZE_H/2-3,
                "%02d"%(n+1),
                c)

        g.draw_center_x(
            "HIT X Key to Select Stage",
            g.SCREEN_HEIGHT-8,
            7)

class SceneEnd():
    def __init__(self, p):
        self.color_counter = 0
    def update(self):
        if g.game.input.btnp(g.InputKey.A):
            g.game.move_scene(g.GameMode.TITLE,{})

    def draw(self):
        g.draw_center_x(
            "TotalScore: %d" %(g.game.score),
            g.SCREEN_HEIGHT/2-40,
            8)
        g.draw_center_x(
            "HIT X Key",
            g.SCREEN_HEIGHT/2+16,
            7)



if __name__ == "__main__":
    g.game_main()