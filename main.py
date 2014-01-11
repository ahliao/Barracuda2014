import socket
import json
import struct
import time
import sys

import socketLayer


def player(host, port):
    s = socketLayer.SocketLayer(host, port)

    gameId = None

    deck = [8]*13

    while True:
        msg = s.pump()
        if msg["type"] == "error":
            print("The server doesn't know your IP. It saw: " + msg["seen_host"])
            sys.exit(1)
        elif msg["type"] == "request":
            if msg["state"]["game_id"] != gameId:
                gameId = msg["state"]["game_id"]
                print("New game started: " + str(gameId))

            if msg["request"] == "request_card":
                cardToPlay = msg["state"]["hand"][0] #This gets the top card

                

                print(sum(msg["state"]["hand"])) #Gets the total sum of the hand
                s.send({"type": "move", "request_id": msg["request_id"],
                    "response": {"type": "play_card", "card": cardToPlay}})


                # Sam is awesome
                
            elif msg["request"] == "challenge_offered":
                s.send({"type": "move", "request_id": msg["request_id"],
                        "response": {"type": "reject_challenge"}})

        elif msg["type"] == "result":
            print("Last Card Played: " + msg["result"]["card"])

        elif msg["type"] == "greetings_program":
            print("Connected to the server.")

def loop(player, *args):
    while True:
        try:
            player(*args)
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(repr(e))
        time.sleep(10)


if __name__ == "__main__":
    loop(player, "cuda.contest", 9999)
