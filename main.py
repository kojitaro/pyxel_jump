#!/usr/bin/env python
import os
import random
import math

import pyxel
from Box2D import b2

import game as g

# class GameMange:
#     def __init__(self):
#         self.coins = 0
#         self.stages = [False] * g.STAGE_NUM
    
#     def 


class Player(g.GContainer):
    def __init__(self, world):
        super().__init__()
        self.walk_counter = 0

        self.first_pos = (2,4)
        self.hit = False

        self.body = world.CreateDynamicBody(position=self.first_pos, angle=0)
        self.body.CreateCircleFixture(radius=0.45, density=1, friction=0.3)

    def update(self):
        super().update()

        x = 0
        if pyxel.btn(pyxel.KEY_LEFT):
            x = -5
            self.walk_counter += 1
        elif pyxel.btn(pyxel.KEY_RIGHT):
            x = 5
            self.walk_counter += 1

        self.body.linearVelocity = (x, self.body.linearVelocity[1])
        if self.body.linearVelocity[1] == 0:
            if pyxel.btn(pyxel.KEY_X) :
                self.body.linearVelocity = (self.body.linearVelocity[0], 7)
        else:
            self.walk_counter = 0

        pos = g.body_pos(self.body)
        if pos[1] < -10:
            self.hit = True
        if pos[0] >= g.STAGE_WIDTH_M:
            self.hit = True

        if self.hit:
            #  落ちた
            self.body.linearVelocity = (0,0)
            g.set_body_pos(self.body, self.first_pos)
            self.hit = False

        


    def draw(self):
        super().draw()

        if g.DEBUG_DRAW:
            g.draw_body(self.body, 8)
        g.draw_body_sprite(self.body, g.SpriteSet.PLAYER.value+int(self.walk_counter/4)%2)

class GroundGenerator:
    def __init__(self, a):
        random.seed(a)
        self.w = g.STAGE_ITEMEND_X_M-g.PLAYER_SCROLL_X_M-2
        self.h = g.SCREEN_HIGHT_M
        self.items = [False] * (self.w*self.h)

    def next(self):
        while True:
            n = random.randint(0, self.w*self.h-1)
            if self.items[n]:
                next
            self.items[n] = True

            return (g.PLAYER_SCROLL_X_M+2 + int(n % self.w),
                int(n / self.w)+0.5)
            


class Ground(g.GContainer):
    def __init__(self, world, generator):
        super().__init__()

        self.bodys = []
        
        for n in range(0, g.STAGE_WIDTH_M+(g.SCREEN_WIDTH_M-g.PLAYER_SCROLL_X_M)):
            body = world.CreateStaticBody(
                position=(n-0.5, -0.1),
                shapes=b2.polygonShape(box=(1, 0.05)),
            )
            self.bodys.append( body )


        # 板
        for n in range(50):
            pos = generator.next()
            body = world.CreateStaticBody(
                position=pos,
                shapes=b2.polygonShape(box=(0.5, 0.5))
                )
            self.bodys.append(body)

        self.coins = []
        for n in range(15):
            self.coins.append( generator.next() )

        self.traps = []
        for n in range(15):
            self.traps.append( generator.next() )

    def update(self, player):
        pb = g.body_pos(player.body)

        for s in self.coins[:]:
            d = math.sqrt((pb[0]-s[0])*(pb[0]-s[0])+(pb[1]-s[1])*(pb[1]-s[1]))
            if d <= 0.8:
                self.coins.remove(s)

        for s in self.traps[:]:
            d = math.sqrt((pb[0]-s[0])*(pb[0]-s[0])+(pb[1]-s[1])*(pb[1]-s[1]))
            if d <= 0.8:
                player.hit = True

    def draw(self):
        super().draw()

        # 地面を描画
        for body in self.bodys:
            g.draw_body(body, 3)

        # 旗描画
        g.draw_sprite_world(((g.STAGE_WIDTH_M, 0.5)), g.SpriteSet.FLAG)

        # コインを描画
        for coin in self.coins:
            g.draw_sprite_world(coin, g.SpriteSet.COIN)

        # わなを描画
        for trap in self.traps:
            g.draw_sprite_world(trap, g.SpriteSet.TRAP)
            




class SceneMain(g.Scene):
    def __init__(self):
        generator = GroundGenerator(0)

        self.world = b2.world(gravity=(0, -10), doSleep=True)
        self.player = Player(self.world)
        self.ground = Ground(self.world, generator)

    def update(self):
        self.world.Step(g.TIME_STEP, 10, 10)
        self.ground.update(self.player)
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
