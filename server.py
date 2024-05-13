import socket
import pickle
import time

#Created socket and defined host,port,matrix
s = socket.socket()
host = "localhost"
port = 9999
matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

#2 players list for connection and address storage
playerOne = 1
playerTwo = 2
playerConn = list()
playerAddr = list()       

#4 It's checks for player and then notes down its connection, it then received input from client in row,column form and decods it into integer, to add values to matrix
#If player1 then matrix value=1, if player 2 then matrix value=2
def get_input(currentPlayer):
    if currentPlayer == playerOne:
        player = "Player 1 Turn"
        conn = playerConn[0]
    else:
        player = "Player 2 Turn"
        conn = playerConn[1]
    print(player)
    send_common_msg(player)
    try:
        #Sends both client input to receive their next move
        conn.send("Input".encode())
        data = conn.recv(2048 * 10)
        conn.settimeout(20)
        dataDecoded = data.decode().split(",")
        x = int(dataDecoded[0])
        y = int(dataDecoded[1])
        matrix[x][y] = currentPlayer
        #Sends updated matrix to both client
        send_common_msg("Matrix")
        send_common_msg(str(matrix))
    except:
        conn.send("Error".encode())
        print("Error occured! Try again..")

def check_rows():
    
    result = 0
    for i in range(3):
        if matrix[i][0] == matrix[i][1] and matrix[i][1] == matrix[i][2]:
            result = matrix[i][0]
            if result != 0:
                break
    return result

def check_columns():
    
    result = 0
    for i in range(3):
        if matrix[0][i] == matrix[1][i] and matrix[1][i] == matrix[2][i]:
            result = matrix[0][i]
            if result != 0:
                break
    return result

def check_diagonals():
    
    result = 0
    if matrix[0][0] == matrix[1][1] and matrix[1][1] == matrix[2][2]:
        result = matrix[0][0]
    elif matrix[0][2] == matrix[1][1] and matrix[1][1] == matrix[2][0]:
        result = matrix[0][2]
    return result

#5 Checks if a player has won by rows,column or diagonal otherwise draw
def check_winner():
    result = 0
    result = check_rows()
    if result == 0:
        result = check_columns()
    if result == 0:
        result = check_diagonals()
    return result

#1 The host and port are binded, it can only accept 2 players
def start_server():
    
    try:
        s.bind((host, port))
        print("Tic Tac Toe server started \nBinding to port", port)
        s.listen(2) 
        accept_players()
    except socket.error as e:
        print("Server binding error:", e)
    

#2 In iteration of 2 players, connection and address are stored to the list using s.accept()
def accept_players():
    try:
        for i in range(2):
            conn, addr = s.accept()
            msg = "You are player {}".format(i+1)
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

#3 Until result changes or 9 iterations are complete loop will get input from player and check for winner
def start_game():
    result = 0
    i = 0
    while result == 0 and i < 9 :
        if (i%2 == 0):
            get_input(playerOne)
        else:
            get_input(playerTwo)
        result = check_winner()
        i = i + 1
        
    #Sends message to both clients to inform that game is over
    send_common_msg("Over")

    if result == 1:
        lastmsg = "Player One is the winner!!"
    elif result == 2:
        lastmsg = "Player Two is the winner!!"
    else:
        lastmsg = "Draw game!! Try again later!"

    send_common_msg(lastmsg)
    time.sleep(10)
    for conn in playerConn:
        conn.close()
    
#Sends message to connection of both players
def send_common_msg(text):
    playerConn[0].send(text.encode())
    playerConn[1].send(text.encode())
    time.sleep(1)

start_server()