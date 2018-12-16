#!/usr/bin/env python
import os

import pyxel
from Box2D import b2

import game as g


class Player(g.GContainer):
    def __init__(self, world):
        super().__init__()
        self.walk_counter = 0

        self.body = world.CreateDynamicBody(position=(2, 4), angle=0)
        self.body.CreateCircleFixture(radius=0.5, density=1, friction=0.3)

    def update(self):
        super().update()

        if self.body.linearVelocity[1] == 0:
            if pyxel.btn(pyxel.KEY_LEFT):
                self.body.angularVelocity = 20
            elif pyxel.btn(pyxel.KEY_RIGHT):
                self.body.angularVelocity = -20
            else:
                self.body.angularVelocity = 0

            if pyxel.btn(pyxel.KEY_X) :
                self.body.linearVelocity = (self.body.linearVelocity[0], 7)

    def draw(self):
        super().draw()

        g.draw_body(self.body, 8)

        plps = [[0,0,16,16],[0,16,16,16]]
        plp = plps[int(self.walk_counter/4)%2]
        #self.walk_counter

        pos = g.body_draw_pos(self.body)
        pyxel.blt(g.DRAW_OFFSET_X + pos[0]-16/2,
            pos[1]-16/2,
            0,
            plp[0],plp[1],plp[2],plp[3], 11)

class Ground(g.GContainer):
    def __init__(self, world):
        super().__init__()

        self.ground_body = world.CreateStaticBody(
            position=(g.STAGE_WIDTH_M/2, -1),
            shapes=b2.polygonShape(box=(g.STAGE_WIDTH_M/2, 2)),
        )
    
    def draw(self):
        super().draw()
        g.draw_body(self.ground_body, 3)

        # 旗描画
        pos = g.world_to_draw_pos((g.STAGE_WIDTH_M, 0))
        pyxel.blt(g.DRAW_OFFSET_X + pos[0]-16,
            pos[1]-16,
            0,
            0, 32, 16, 16, 11)





class SceneMain(g.Scene):
    def __init__(self):

        self.world = b2.world(gravity=(0, -10), doSleep=True)
        self.player = Player(self.world)
        self.ground = Ground(self.world)

    def update(self):
        self.world.Step(g.TIME_STEP, 10, 10)
        self.player.update()

    def draw(self):
        pyxel.text(0,0,"00:00", 7)

        # 描画のオフセットを計算
        pos = g.body_pos(self.player.body)
        g.set_draw_offset_x_m( min(0, g.PLAYER_SCROLL_X_M-pos[0]))

        self.player.draw()
        self.ground.draw()

class Game:
    def __init__(self):
        pyxel.init(g.SCREEN_WIDTH, g.SCREEN_HEIGHT)
        pyxel.load(os.path.join(os.path.dirname(__file__), "main.pyxel"))

        self.scene = SceneMain()

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.scene.update()

    def draw(self):
        pyxel.cls(0)
        self.scene.draw()



if __name__ == "__main__":
    game = Game()
