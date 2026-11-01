import time
import turtle

screen = turtle.Screen()
screen.setup(1200, 420)
screen.title("Sheep Wrestling - Buttons (No def)")
screen.tracer(0)

SD = turtle.Turtle() #SD -> Static drawer
SD.hideturtle()
SD.penup()
SD.speed(0)

ED = turtle.Turtle() #ED -> entity drawer
ED.hideturtle()
ED.penup()
ED.speed(0)

# Field geometry
BOX_Y = 0
BOX_X_START = -440
BOX_SIZE = 80

# Colors
BG = "forestgreen"
FIELD_COLOR = "saddlebrown"
QUEUE_COLOR = "#6b4f2f"
TEXT_COLOR = "black"
PS_COLOR = "white"
ES_COLOR = "black"
BTN_FILL = "#cccccc"
BTN_TEXT = "black"

screen.bgcolor(BG)

# Field slots
NUM_SLOTS = 10

SD.color(FIELD_COLOR)
for i in range(NUM_SLOTS):
    x0 = BOX_X_START + i * BOX_SIZE
    SD.penup()
    SD.goto(x0, BOX_Y)
    SD.pendown()
    SD.begin_fill()
    for _ in range(2):
        SD.forward(BOX_SIZE)
        SD.left(90)
        SD.forward(80)
        SD.left(90)
    SD.end_fill()
SD.penup()
screen.update()

# ------------------ Game data ------------------
data = {
    'PS': {
        'S1': {'Number': 1, 'Power': 1, 'CD': 0},
        'S2': {'Number': 2, 'Power': 3, 'CD': 0},
        'S3': {'Number': 3, 'Power': 5, 'CD': 0}
    },
    'ES': {
        'S1': {'Number': -1, 'Power': 1, 'CD': 0},
        'S2': {'Number': -2, 'Power': 3, 'CD': 0},
        'S3': {'Number': -3, 'Power': 5, 'CD': 0}
    }
}

Field = [0] * 12

enemy_cycle = ["S1", "S2", "S3"]
enemy_idx = 0

click_xy = None
click_pressed = False

screen.listen()
screen.onscreenclick(lambda x, y: globals().update(click_xy=(x, y), click_pressed=True))

button_width = 120
button_height = 48
button_gap = 18

field_left = BOX_X_START
field_right = BOX_X_START + (NUM_SLOTS - 1) * BOX_SIZE + BOX_SIZE
buttons_total_width = 5 * button_width + 4 * button_gap
buttons_left = (field_left + field_right)/2 - buttons_total_width/2
buttons_y = BOX_Y - 120

buttons = []
labels = ["1", "2", "3", "Skip", "Exit"]
values = [1, 2, 3, 4, 5]
for idx, lab in enumerate(labels):
    bx = buttons_left + idx * (button_width + button_gap)
    by = buttons_y
    buttons.append((bx, by, bx + button_width, by + button_height, lab, values[idx]))

size_map = {1: 25, 2: 35, 3: 45}
SD.clear()
# draw boxes
SD.color(FIELD_COLOR)
for i in range(NUM_SLOTS):
    x0 = BOX_X_START + i * BOX_SIZE
    SD.penup()
    SD.goto(x0, BOX_Y)
    SD.pendown()
    SD.begin_fill()
    for _ in range(2):
        SD.forward(BOX_SIZE)
        SD.left(90)
        SD.forward(80)
        SD.left(90)
    SD.end_fill()
    
left_qx = BOX_X_START - BOX_SIZE - 30
left_qy = BOX_Y + 10
SD.penup()
SD.goto(left_qx - 30, left_qy + 20)
SD.pendown()
SD.color(QUEUE_COLOR)
SD.begin_fill()
for _ in range(2):
    SD.forward(60)
    SD.left(90)
    SD.forward(40)
    SD.left(90)
SD.end_fill()
SD.penup()

right_qx = BOX_X_START + NUM_SLOTS * BOX_SIZE + 30
SD.goto(right_qx - 30, left_qy + 20)
SD.pendown()
SD.begin_fill()
for _ in range(2):
    SD.forward(60)
    SD.left(90)
    SD.forward(40)
    SD.left(90)
SD.end_fill()
SD.penup()

for (x1, y1, x2, y2, lab, val) in buttons:
    SD.penup()
    SD.goto(x1, y1)
    SD.pendown()

    SD.color(BTN_FILL)      
    SD.begin_fill()
    SD.goto(x2, y1)
    SD.goto(x2, y2)
    SD.goto(x1, y2)
    SD.goto(x1, y1)
    SD.end_fill()

    SD.penup()
    SD.color(BTN_TEXT)
    SD.goto((x1+x2)/2, y1 + button_height/2 - 8)
    SD.write(lab, align="center", font=("Arial", 14, "bold"))
SD.penup()
screen.update()



# ------------------ Main loop ------------------
turn = 0
print("Welcome to sheep wrestling!!!\nTHe rules are simple:\n\nYou have three type of sheeps.\n -> Sheep 1: The weakest sheep with shortest cooldowm. Power = 1, CoolDown = 3")
print(" -> Sheep 2: The sheep with medium qualities. Power = 3, Cooldown = 5.")
print(" -> Sheep 3: The best sheep with longest cooldown. Power = 5, Cooldown = 7.")
print("You have to deploy sheeps only when their cooldown is 0. The sheeps, initially, have a cooldown of 0 seconds. Upon deployment, their cooldown changes to above values.")
print("When your and opponent's sheep collide, the side with sheeps having more power would push the other side. To win, you have to push your opponent's sheeps till",end='')
print("they go out of the field. When your all sheeps are on cooldown, you wouldn't be given any choice.")
while True:
    turn += 1
    print("\n----- TURN", turn, "START -----")
    print("CD PS:", {k: data["PS"][k]["CD"] for k in data["PS"]})
    print("CD ES:", {k: data["ES"][k]["CD"] for k in data["ES"]})
    print("Click a button (1/2/3/Skip/Exit).")

    click_xy = None
    click_pressed = False
    pending_deploy = None

    # wait for user click on a button
    while True:
        screen.update()
        if click_pressed:
            cx, cy = click_xy
            chosen = None
            for (x1, y1, x2, y2, lab, val) in buttons:
                if x1 <= cx <= x2 and y1 <= cy <= y2:
                    chosen = val
                    break
            click_pressed = False
            click_xy = None
            if chosen is not None:
                pending_deploy = chosen
                break
        time.sleep(0.02)

    # if exit
    if pending_deploy == 5:
        print("Player exited.")
        break

    # COOLDOWN countdown at start of turn
    for side in ['PS', 'ES']:
        for s in data[side]:
            if data[side][s]['CD'] > 0:
                data[side][s]['CD'] -= 1

    # PLAYER DEPLOY
    if pending_deploy in (1, 2, 3):
        sid = "S" + str(pending_deploy)
        if data['PS'][sid]['CD'] == 0 and Field[0] == 0:
            Field[0] = data['PS'][sid]['Number']
            data['PS'][sid]['CD'] = {1: 3, 2: 5, 3: 7}[pending_deploy]
            print("Player deployed:", sid)
        else:
            print("Cannot deploy:", sid)
    elif pending_deploy == 4:
        print("Player skipped deployment.")

    # MOVE PLAYER SHEEP (right)
    for i in range(10, -1, -1):
        if Field[i] > 0 and Field[i+1] == 0:
            v = Field[i]
            Field[i] = 0

            start_x = BOX_X_START + i * BOX_SIZE + BOX_SIZE/2
            end_x   = BOX_X_START + (i+1) * BOX_SIZE + BOX_SIZE/2
            mid_y   = BOX_Y + 40
            size    = size_map.get(abs(v), 30)
            color   = PS_COLOR if v > 0 else ES_COLOR

            ED.clear()
            ED.penup()
            ED.goto(start_x + (end_x - start_x), mid_y)
            ED.dot(size, color)
            screen.update()

            Field[i+1] = v

    # MOVE ENEMY SHEEP (left)
    for i in range(1, 12):
        if Field[i] < 0 and Field[i-1] == 0:
            v = Field[i]
            Field[i] = 0

            start_x = BOX_X_START + (i-1) * BOX_SIZE + BOX_SIZE/2 + BOX_SIZE
            end_x   = BOX_X_START + (i-1) * BOX_SIZE + BOX_SIZE/2
            mid_y   = BOX_Y + 40
            size    = size_map.get(abs(v), 30)
            color   = PS_COLOR if v > 0 else ES_COLOR

            ED.clear()
            ED.penup()
            ED.goto(start_x + (end_x - start_x), mid_y)
            ED.dot(size, color)
            screen.update()

            Field[i-1] = v

    # COLLISION
    collision_index = None
    for p in range(1, 11):
        if Field[p] > 0 and Field[p+1] < 0:
            collision_index = p
            break

    if collision_index is not None:
        p = collision_index
        left_empty = None
        for x in range(p, -1, -1):
            if Field[x] == 0:
                left_empty = x
                break
        if left_empty is None:
            left_empty = 0
        right_empty = None
        for x in range(p+1, 12):
            if Field[x] == 0:
                right_empty = x
                break
        if right_empty is None:
            right_empty = 11

        ps_load = 0
        es_load = 0
        for x in range(left_empty + 1, right_empty):
            v = Field[x]
            if v > 0:
                for k in data['PS'].values():
                    if k['Number'] == v:
                        ps_load += k['Power']
                        break
            elif v < 0:
                for k in data['ES'].values():
                    if k['Number'] == v:
                        es_load += k['Power']
                        break

        print(f"Collision at {p}&{p+1}, zone {left_empty+1}..{right_empty-1} | PS={ps_load} ES={es_load}")

        # single-step shift
        if ps_load > es_load:
            for pos in range(right_empty - 1, left_empty, -1):
                if Field[pos] != 0:
                    Field[pos + 1] = Field[pos]
                    Field[pos] = 0
            print("Player pushes forward!")
        elif es_load > ps_load:
            for pos in range(left_empty + 1, right_empty):
                if Field[pos] != 0:
                    Field[pos - 1] = Field[pos]
                    Field[pos] = 0
            print("Enemy pushes forward!")
        else:
            print("Equal — no movement")

    # ENEMY deployment
    if Field[11] == 0:
        tries = 0
        while tries < 3:
            key = enemy_cycle[enemy_idx]
            if data['ES'][key]['CD'] == 0:
                Field[11] = data['ES'][key]['Number']
                data['ES'][key]['CD'] = data['ES'][key]['Power'] * 3
                print("Enemy queued:", key)
                enemy_idx = (enemy_idx + 1) % 3
                break
            enemy_idx = (enemy_idx + 1) % 3
            tries += 1

    # DRAW / UPDATE visible field & queues & buttons
    SD.clear()
    # draw field boxes
    SD.color(FIELD_COLOR)
    for i in range(NUM_SLOTS):
        x0 = BOX_X_START + i * BOX_SIZE
        SD.penup()
        SD.goto(x0, BOX_Y)
        SD.pendown()
        SD.begin_fill()
        for _ in range(2):
            SD.forward(BOX_SIZE)
            SD.left(90)
            SD.forward(80)
            SD.left(90)
        SD.end_fill()
    SD.penup()
    # draw battlefield
    SD.color(TEXT_COLOR)
    for i in range(NUM_SLOTS):
        x0 = BOX_X_START + i * BOX_SIZE + BOX_SIZE/2
        SD.goto(x0, BOX_Y - 18)
        SD.write(str(i+1), align="center", font=("Arial", 9, "normal"))

    # left queue box and content
    left_qx = BOX_X_START - BOX_SIZE - 30
    left_qy = BOX_Y + 10
    SD.penup()
    SD.goto(left_qx - 30, left_qy + 20)
    SD.pendown()
    SD.color(QUEUE_COLOR)
    SD.begin_fill()
    for _ in range(2):
        SD.forward(60)
        SD.left(90)
        SD.forward(40)
        SD.left(90)
    SD.end_fill()
    SD.penup()
    if Field[0] != 0:
        n = Field[0]
        size = size_map.get(abs(n), 30)
        color = PS_COLOR if n > 0 else ES_COLOR
        ED.goto(left_qx, left_qy)
        ED.dot(size, color)

    # right queue box and content
    right_qx = BOX_X_START + NUM_SLOTS * BOX_SIZE + 30
    SD.penup()
    SD.goto(right_qx - 30, left_qy + 20)
    SD.pendown()
    SD.color(QUEUE_COLOR)
    SD.begin_fill()
    for _ in range(2):
        SD.forward(60)
        SD.left(90)
        SD.forward(40)
        SD.left(90)
    SD.end_fill()
    SD.penup()
    if Field[11] != 0:
        n = Field[11]
        size = size_map.get(abs(n), 30)
        color = PS_COLOR if n > 0 else ES_COLOR
        SD.goto(right_qx, left_qy)
        SD.dot(size, color)

    # draw sheep in battlefield positions
    for pos in range(1, 11):
        v = Field[pos]
        if v != 0:
            x = BOX_X_START + (pos-1) * BOX_SIZE
            size = size_map.get(abs(v), 30)
            color = PS_COLOR if v > 0 else ES_COLOR
            SD.penup()
            SD.goto(x + BOX_SIZE/2, BOX_Y + 40)
            SD.dot(size, color)

    # draw buttons (redraw)
    for (x1, y1, x2, y2, lab, val) in buttons:
        SD.penup()
        SD.goto(x1, y1)
        SD.pendown()
        SD.color(BTN_FILL)
        SD.begin_fill()
        SD.goto(x2, y1)
        SD.goto(x2, y2)
        SD.goto(x1, y2)
        SD.goto(x1, y1)
        SD.end_fill()
        SD.penup()
        SD.color(BTN_TEXT)
        SD.goto((x1+x2)/2, y1 + button_height/2 - 8)
        SD.write(lab, align="center", font=("Arial", 14, "bold"))

    screen.update()

    # WIN/LOSE check
    if Field[1] < 0:
        print("YOU LOSE")
        break
    if Field[11] > 0:
        print("YOU WIN")
        break

    # end-of-turn pause
    time.sleep(1.5)
    print("Next turn.")
# end main loop

print("Game over.")
screen.bye()
