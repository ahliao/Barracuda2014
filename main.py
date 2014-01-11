import socket
import json
import struct
import time
import sys

import socketLayer
import Comm
import cardCount

def player(host, port):
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

            # If a card is requested/challenge can be issued
            if comm.request == "request_card":
                cardToPlay = comm.hand[0]
                comm.playCard(cardToPlay)
                deckCount.updateDeck(cardToPlay)    # update the deck 

            # If a challenge is offerred, handle logic
            elif comm.request == "challenge_offered":
                comm.acceptChallenge()

        # The result of the other player's turn
        # Handle any counting/probs stuff
        elif comm.type == "result":
            if comm.resultType == "trick_won": # Make sure that a card field exists
                deckCount.updateDeck(comm.card)
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
