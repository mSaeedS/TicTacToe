import pygame
import socket
import time
import threading
import pickle

s = socket.socket()
host = "localhost"
port = 9999

playerOne = 1
playerTwo = 2

allow = 0 # allow handling mouse events
xy = (-1, -1)

# Create worker threads
def create_thread(target):
    t = threading.Thread(target=target) # argument - target function
    t.daemon = True
    t.start()

# Initialize
pygame.init()

width = 600
height = 550
screen = pygame.display.set_mode((width, height))

# Set title
pygame.display.set_caption("Tic Tac Toe")

# Fonts
bigfont = pygame.font.Font('freesansbold.ttf', 64)
smallfont = pygame.font.Font('freesansbold.ttf', 32)
backgroundColor = (255, 255, 255)
titleColor = (0, 0, 0)
subtitleColor = (128, 0, 255)
lineColor = (0, 0, 0)

def buildScreen(bottomMsg, string, playerColor=subtitleColor):
    # your UI building logic
    pass

def handleMouseEvent(pos):
    # your mouse event handling logic
    pass

def start_player():
    try:
        s.connect((host, port))
        print("Connected to:", host, ":", port)
        recvData = s.recv(2048 * 10)
        bottomMsg = recvData.decode()
        if "1" in bottomMsg:
            currentPlayer = 1
        else:
            currentPlayer = 2
        start_game()
        s.close()
    except socket.error as e:
        print("Socket connection error:", e) 

def start_game():
    running = True
    global msg
    global matrix
    global bottomMsg
    create_thread(accept_msg)
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if allow:
                    handleMouseEvent(pos)
    
        if msg == "":
            break
        
        buildScreen(bottomMsg, msg)                      
        pygame.display.update()

def accept_msg():
    global msg
    global bottomMsg 
    global allow
    global xy
    while True:
        try: 
            recvData = s.recv(2048 * 10)
            recvDataDecode = recvData.decode()
            buildScreen(bottomMsg, recvDataDecode)

            if recvDataDecode == "Input":
                failed = 1
                allow = 1
                xy = (-1, -1)
                while failed:
                    try:
                        if xy != (-1, -1):
                            coordinates = str(xy[0]) + "," + str(xy[1])
                            s.send(coordinates.encode())
                            failed = 0
                            allow = 0
                    except:
                        print("Error occurred....Try again")

            elif recvDataDecode == "Error":
                print("Error occurred! Try again..")
            
            elif recvDataDecode == "Matrix":
                matrixRecv = s.recv(2048 * 100)
                matrix = pickle.loads(matrixRecv)
                print(matrix)  # This is for debugging, you'll integrate this data into your UI

            elif recvDataDecode == "Over":
                msgRecv = s.recv(2048 * 100)
                msg = msgRecv.decode("utf-8")
                bottomMsg = msg
                msg = "~~~Game Over~~~"
                break
            else:
                msg = recvDataDecode

        except KeyboardInterrupt:
            print("\nKeyboard Interrupt")
            time.sleep(1)
            break

        except:
            print("Error occurred")
            break

start_player()
