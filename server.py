import socket
import pickle
import time
import classes

s = socket.socket()
host = "localhost"
port = 9999

playerOne = 1
playerTwo = 2

playerConn = list()
playerAddr = list()       

game = classes.TicTacToe()

def get_input(currentPlayer, conn):
    while True:
        try:
            conn.send("Input".encode())
            data = conn.recv(2048 * 10)
            conn.settimeout(20)
            dataDecoded = data.decode().split(",")
            x = int(dataDecoded[0])
            y = int(dataDecoded[1])
            if game.make_move(x, y, currentPlayer):
                break
            else:
                conn.send("Error".encode())
                print("Error occurred! Try again..")
        except:
            print("Error occurred! Try again..")

def start_server():
    try:
        s.bind((host, port))
        print("Tic Tac Toe server started \nBinding to port", port)
        s.listen(2) 
        accept_players()
    except socket.error as e:
        print("Server binding error:", e)
    
def accept_players():
    try:
        for i in range(2):
            conn, addr = s.accept()
            msg = "<<< You are player {} >>>".format(i+1)
            conn.send(msg.encode())

            playerConn.append(conn)
            playerAddr.append(addr)
            print("Player {} - [{}:{}]".format(i+1, addr[0], str(addr[1])))
    
        start_game()
        s.close()
    except socket.error as e:
        print("Player connection error", e)
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt")
        exit()
    except Exception as e:
        print("Error occurred:", e)

def start_game():
    result = 0
    i = 0
    while result == 0 and i < 9 :
        if (i%2 == 0):
            get_input(playerOne, playerConn[0])
        else:
            get_input(playerTwo, playerConn[1])
        result = game.check_win()
        i = i + 1
    
    send_common_msg("Over")

    if result == 1:
        lastmsg = "Player One is the winner!!"
    elif result == -1:
        lastmsg = "Player Two is the winner!!"
    else:
        lastmsg = "Draw game!! Try again later!"

    send_common_msg(lastmsg)
    time.sleep(10)
    for conn in playerConn:
        conn.close()
    

def send_common_msg(text):
    for conn in playerConn:
        conn.send(text.encode())
        time.sleep(1)

start_server()
