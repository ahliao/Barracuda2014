import socket
import json
import struct
import time
import sys

import socketLayer
import Comm
import Player


def player(host, port):
    comm = Comm.Comm()
	player = Player.Player()

    gameId = None

    comm = Comm.Comm()
    deckCount = cardCount.cardCount()

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

def loop(player, *args):
    while True:
        try:
            player(*args)
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(e)
        time.sleep(10)


if __name__ == "__main__":
    loop(player, "cuda.contest", 9999)
