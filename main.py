import socket
import json
import struct
import time
import sys

import Comm
import Player

def playTurn():
    gameId = None

    comm = Comm.Comm()
    player = Player.Player()

    while True:
        comm.refresh(player)

        if comm.type == "error":
            print("The server doesn't know your IP. It saw: " + comm.host)
            sys.exit(1)
        elif comm.type == "request":

            # If a new game is starting
            if comm.game_id != gameId:
                gameId = comm.game_id;
                print("New game started: " + str(gameId))
                player.counter.refreshDeck()


            if comm.request == "request_card":
                player.playRequest(comm)
            elif comm.request == "challenge_offered":
                player.challenged(comm)
        elif comm.type == "result":
            player.result(comm)
            
        elif comm.type == "greetings_program":
            print("Connected to the server.")


while True:
    try:
        playTurn()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(e)
    time.sleep(10)


