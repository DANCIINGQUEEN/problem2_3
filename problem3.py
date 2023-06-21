import turtle
import time
import threading


wn = turtle.Screen()
wn.bgcolor("black")
wn.title("2017125009")
wn.tracer(0)

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

shapes = ["pacman.gif", "cherry.gif", "x.gif"]

for shape in shapes:
    wn.register_shape(shape)


class Sprite:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.shape(self.image)
        pen.stamp()

    def is_distance_collision(self, other):
        distance = (((self.x - other.x) ** 2) + ((self.y - other.y) ** 2)) ** 0.5
        if distance < (self.width + other.width) / 2.0:
            return True
        else:
            return False


class Character(Sprite):
    def __init__(self, x, y, width, height, image, jump=False):
        super().__init__(x, y, width, height, image)
        self.jump = jump

    def rhop(self, distance=300): # 오른쪽으로 점프
        vy = 25  # y축 속도
        g = -1  # 중력 가속도
        self.y += vy  # y축 속도만큼 이동
        while self.y > -300:  # y축이 -300위치에 닿을 때까지 반복
            self.x += distance / 60  # x축 이동
            vy += g  # 중력 가속도 적용
            self.y += vy  # y축 속도만큼 이동
            print(f"x: {self.x}, y: {self.y}")
            pen.clear()  # 화면 지우기
            for sprite in sprites:  # 스프라이트 그리기
                sprite.render(pen)
            wn.update()  # 화면 업데이트
            time.sleep(0.01)  # 0.01초 대기

        self.y = -300  # 바닥에 닿은 위치로 초기화

    def lhop(self, distance=300): # 왼쪽으로 점프
        vy = 25  # y축 속도
        g = -1  # 중력 가속도
        self.y += vy  # y축 속도만큼 이동
        while self.y > -300:  # y축이 -300위치에 닿을 때까지 반복
            self.x -= distance / 60  # x축 이동
            vy += g  # 중력 가속도 적용
            self.y += vy  # y축 속도만큼 이동
            print(f"x: {self.x}, y: {self.y}")
            pen.clear()  # 화면 지우기
            for sprite in sprites:  # 스프라이트 그리기
                sprite.render(pen)
            wn.update()  # 화면 업데이트
            time.sleep(0.01)  # 0.01초 대기

        self.y = -300  # 바닥에 닿은 위치로 초기화


pacman = Character(-128, -300, 128, 128, "pacman.gif", jump=True)
cherry = Sprite(128, -300, 128, 128, "cherry.gif")
sprites = [pacman, cherry]

def rjump_pacman(distance=300): # 오른쪽으로 점프
    pacman.rhop(distance)
def ljump_pacman(distance=300): # 왼쪽으로 점프
    pacman.lhop(distance)
def move_right():
    pacman.x += 20
def move_left():
    pacman.x -= 20


def move_cherry():
    distance = 3    # 이동 거리
    direction = 1  # 이동 방향 설정 (1: 오른쪽, -1: 왼쪽)
    while True:
        cherry.x += direction * distance    # 이동
        print(f"x: {cherry.x}, y: {cherry.y}")  # 현재 좌표 출력
        time.sleep(0.01)    # 0.01초 대기

        # 화면 좌우 끝에 도달하면 방향을 반전시킴
        if cherry.x >= 500 or cherry.x <= -500:
            direction *= -1 # 이동 방향 반전
        if pacman.is_distance_collision(cherry):    # 충돌 시
            break   # 반복문 종료

wn.listen()
wn.onkeypress(move_right, "Right")
wn.onkeypress(move_left, "Left")
wn.onkeypress(rjump_pacman, "space")
wn.onkeypress(ljump_pacman, "Shift_L")

jump_thread = threading.Thread(target=rjump_pacman) # 오른쪽으로 점프하는 스레드 시작
jump_thread.start()
ljump_thread = threading.Thread(target=ljump_pacman)    # 왼쪽으로 점프하는 스레드 시작
ljump_thread.start()


move_cherry_thread = threading.Thread(target=move_cherry)   # 체리의 이동을 실행하는 스레드 시작
move_cherry_thread.start()

while True:
    for sprite in sprites:
        sprite.render(pen)
    if pacman.is_distance_collision(cherry):
        cherry.image = "x.gif"
    wn.update()
    pen.clear()
