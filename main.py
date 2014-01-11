import socket
import json
import struct
import time
import sys

import Comm
import Player
import cardCount

def player():
    gameId = None

    comm = Comm.Comm()
    deckCount = cardCount.CardCount()
    player = Player.Player()

    while True:
        comm.refresh()

        if comm.type == "error":
            print("The server doesn't know your IP. It saw: " + comm.host)
            sys.exit(1)
        elif comm.type == "request":

            # If a new game is starting
            if comm.game_id != gameId:
                gameId = comm.game_id;
                print("New game started: " + str(gameId))

            if comm.request == "request_card":
                player.playRequest(comm)
            elif comm.request == "challenge_offered":
                player.challenged(comm)
        elif comm.type == "result":
            player.result(comm)
            print(comm.resultType)
            print(comm.player_num)
            
        elif comm.type == "greetings_program":
            print("Connected to the server.")

def loop(player):
    while True:
        try:
            player()
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(e)
        time.sleep(10)


if __name__ == "__main__":
    loop(player)
