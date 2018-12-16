import pyxel
import Box2D
from Box2D import b2

PPM = 16.0  # pixels per meter
TARGET_FPS = 30
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 224, 126
SCREEN_Y_ZERO_OFFSET = 120
STAGE_WIDTH_M = 70  # m



# プレイヤーの移動の起点
PLAYER_SCROLL_X_M = 3

# プレイヤーの移動に合わせた全体の描画の移動量
DRAW_OFFSET_X = 0
DRAW_OFFSET_X_M = 0

def set_draw_offset_x_m(offset_m):
    global DRAW_OFFSET_X_M
    global DRAW_OFFSET_X

    DRAW_OFFSET_X_M = offset_m
    DRAW_OFFSET_X = offset_m * PPM

def body_pos(body):
    return body.transform * (0,0)

def body_draw_pos(body):
    return world_to_draw_pos(body.transform * (0,0))

def world_to_draw_pos(pos):
    return int(pos[0]* PPM), int(SCREEN_Y_ZERO_OFFSET - pos[1] * PPM)

def draw_polygon(vertices, color):
    for i in range(len(vertices)-1):
        pyxel.line(vertices[i][0] + DRAW_OFFSET_X, vertices[i][1],
            vertices[i+1][0] + DRAW_OFFSET_X, vertices[i+1][1],
            color)

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




class GObject:
    def __init__(self):
        self.parent = None

    def update(self):
        pass
    
    def draw(self):
        pass

    def removeFromParent(self):
        if self.parent is None:
            return
        
        self.parent.children.remove(self)
        self.parent = None

class GContainer(GObject):
    def __init__(self):
        super().__init__()
        self.children = []
    
    def update(self):
        for child in self.children[:]:
            child.update()
    
    def draw(self):
        for child in self.children[:]:
            child.draw()

    def addChild(self, child):
        assert child.parent is None

        child.parent = self
        self.children.append(child)

class Scene:
    def __init__(self):
        pass
    
    def update(self):
        pass
    
    def draw(self):
        pass
