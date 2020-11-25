import pygame,time, random , math, copy

class Vector2:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"{self.x},{self.y}"
    def __sub__(self,other):
        return Vector2(self.x - other.x,self.y - other.y)
    def __add__(self,other):
        return Vector2(self.x + other.x,self.y + other.y)
    def __mul__(self,mul):
        return Vector2(self.x * mul,self.y * mul)
    def __rmul__(self,mul):
        return Vector2(self.x * mul,self.y * mul)
    def __truediv__(self,div):
        return Vector2(self.x / div,self.y / div)
    def int(self):
        return Vector2(int(self.x),int(self.y))
    def tuple(self):
        return (self.x,self.y)
    def normalize(self):
        magnitude = self.magnitude()
        if magnitude == 0:magnitude = 1
        nX = self.x / magnitude
        nY = self.y / magnitude
        return Vector2(nX,nY)
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)


class Body:
    def __init__(self,mass,radius,position,velocity):
        self.mass = mass
        self.radius = radius
        self.position = position
        self.velocity = velocity

def ToGameSpace(screenVector):
    screenVector.y = screensize.y - screenVector.y
    return screenVector

def ToScreenSpace(gameVector):
    gameVector.y = screensize.y - gameVector.y
    return gameVector

def GetMousePos():
    pos = pygame.mouse.get_pos()
    pos = Vector2(pos[0],pos[1])
    return pos

screensize = Vector2(1000,1000)

pygame.init()
screen = pygame.display.set_mode(screensize.tuple())

fps = 60
bodies = []
gravitationalConstant = 100
smashEnergyReduction = 0.2
startMass = 10
startRadius = 5
throwPower = 1

lastFrame = time.time()

leftDown = False
holdDownPos = None

increaseMode = "gravity"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                bodies = []
            elif event.key == pygame.K_g:
                increaseMode = "gravity"
            elif event.key == pygame.K_UP:
                if increaseMode == "gravity":
                    gravitationalConstant += 10
                    print(gravitationalConstant)
            elif event.key == pygame.K_DOWN:
                if increaseMode == "gravity":
                    gravitationalConstant -= 10
                    print(gravitationalConstant)

    if time.time() - lastFrame < 1/fps:continue

    if pygame.mouse.get_pressed()[0] and not leftDown:
        holdDownPos = ToGameSpace(GetMousePos())
        leftDown = True
    elif not pygame.mouse.get_pressed()[0]:
        if leftDown:
            position = ToGameSpace(GetMousePos())
            force = (holdDownPos - position).magnitude() * throwPower
            velocity = (holdDownPos - position).normalize() * force
            bodies.append(Body(startMass,startRadius,holdDownPos,velocity))
        leftDown = False

    screen.fill((0,0,0))

    for body in bodies:
        for body1 in bodies:
            distance = (body.position - body1.position).magnitude()
            if distance < body.radius + body1.radius and body is not body1:
                body.mass += body1.mass
                body.velocity *= smashEnergyReduction
                body.radius += body1.radius
                bodies.remove(body1)
                continue
            distance -= body.radius + body1.radius
            try:
                force = (gravitationalConstant * body.mass * body1.mass) / distance ** 2
            except:
                force = 0
            direction = (body1.position - body.position).normalize()
            body.velocity += direction * force / body.mass

        body.position += body.velocity * (time.time() - lastFrame)

        pygame.draw.circle(screen,(255,255,255),ToScreenSpace(body.position.int()).tuple(),body.radius)

    pygame.display.flip()
    lastFrame = time.time()
