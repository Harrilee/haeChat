import os
import random
import time
import socket
import select
import sys
import indexer
import json
from chat_utils import *
import chat_group as grp
import threading


def main():
    class Card():
        def __init__(self,suit = None,rank = 0):
            self.ranks = [None,"A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
            self.rank = self.ranks[rank]
            self.suits = {'d': 'diamond','c':'club', 'h':'heart', 's':'spade'}
            if suit is None:
                self.suit = suit
            else:
                self.suit = self.suits[suit]
            self.value = -1

        def get_rank(self):
            return self.rank

        def get_suit(self):
            return self.suit

        def show(self):
            print(self.suits, self.rank)

        def __repr__(self):
            return self.suit + ' ' + str(self.rank)



    class Deck():
        def __init__(self):
            self.cards = []
            self.build()
        def build(self):
            for s in ["d", "c", "h", "s"]:
                for v in range(1,14):
                    self.cards.append(Card(s,v))
        def show(self):
            for c in self.cards:
                c.show()

        def shuffle(self):
            for i in range(len(self.cards) -1, 0, -1):
                r = random.randint(0, i)
                self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

        def getCards(self):
            return self.cards

        def __repr__(self):
            return str(self.cards)

    #===========================
    # Pot Class - not finished
    #===========================
    class Pot():
        def __init__(self):
            self.size = 0

        def bets(self, bet):
            self.size += bet

        def reset(self):
            self.size = 0

        def __repr__(self):
            return str(self.size)


    class Players():
        def __init__(self, name = None, client = None):
            self.client = client
            self.name = name
            self.money = 100
            self.status = ''
            self.instructions = ''
            self.to_send = ''
            self.to_receive = []
            self.action = ''

        def out(self, message):
            self.to_receive.append(message)
            #'[ {} ] '.format(self.name)
            print(message)
            return
            mysend(to_sock, json.dumps({"action": "exchange_g", "from": msg["from"], "message": msg["message"]}))

        def inp(self):
            user_input = None
            while len(self.action) == 0:
                time.sleep(CHAT_WAIT)

            if len(self.action) > 0:
                user_input = self.action

            if not user_input is None:
                self.action = ''
                return user_input


    def total(hand):
        total = 0
        for card in hand:
            card = card.get_rank()
            if card == "J" or card == "Q" or card == "K":
                total += 10
            elif card == "A":
                if total >= 11:
                    total+=1
                else:
                    total += 11
            else:
                total += int(card)
        return total


    def hit(hand, deck):
        card = deck.pop()
        hand.append(card)
        return hand

    def print_results(player1, player2, player1_hand, player2_hand):
        print("\n{}: {} Total: {}".format(player1.name, player1_hand, str(total(player1_hand))))
        print("{}: {} Total: {}\n".format(player2.name, player2_hand, str(total(player2_hand))))

        #player1.out("{}: {}".format(player1.name, player1_hand)
        #player1.out("{}: {}".format(player2.name, player2_hand)
        #player2.out("{}: {}".format(player1.name, player1_hand)
        #player2.out("{}: {}".format(player2.name, player2_hand)

    def play_again(player1, player2):
        again = "Do you want to play again? (Y/N) : "

        ans = input(again).lower()

        if ans == 'y':
            game(player1, player2)

        #player1.out(again)
        #player2.out(again)
        #if player1.inp().lower() == 'y' or player2.inp().lower() == 'y':
        #    game()
        elif ans == 'n':
            pass
            #exit()


    def blackjack(player1, player2, player1_hand, player2_hand):
        congrats = "Congratulations! You got a Blackjack!\n"
        if total(player1_hand) == 21:
            print_results(player1, player2, player1_hand, player2_hand)
            print(player1.name + ' ' + congrats)
            #player1.out(congrats)
            #player2.out("Sorry, " + player1.name + " got a Blackjack.\n")
            play_again(player1, player2)
        elif total(player2_hand) == 21:
            print_results(player1, player2, player1_hand, player2_hand)
            print(player2.name + ' '+ congrats)
            #player2.out(congrats)
            #player1.out("Sorry, " + player2.name + " got a Blackjack.\n")
            play_again(player1, player2)

    def score(player1, player2, player1_hand, player2_hand):
        if total(player1_hand) == 21:
            print_results(player1, player2, player1_hand, player2_hand)
            print(player1.name + " got a Blackjack!\n")
            #player1.out('Congratulations! You got a Blackjack!\n')
            #player2.out("Sorry, " + player1.name + " got a Blackjack.\n")
        elif total(player2_hand) == 21:
            print_results(player1, player2, player1_hand, player2_hand)
            print(player2.name + " got a Blackjack!\n")
            #player2.out('Congratulations! You got a Blackjack!\n')
            #player1.out("Sorry, " + player2.name + " got a Blackjack.\n")
        elif total(player1_hand) > 21 and total(player2_hand) > 21:
            print_results(player1, player2, player1_hand, player2_hand)
            print("{} and {} both busted.".format(player1.name, player2.name))
            #player1.out('Sorry, both of you busted')
            #player2.out('Sorry, both of you busted')
        elif total(player1_hand) > 21:
            print_results(player1, player2, player1_hand, player2_hand)
            print('{} busted. {} wins!\n'.format(player1.name, player2.name))
            #player1.out('Sorry, you busted. You lose.\n')
            #player2.out(player1.name + ' busted. You win!\n')
        elif total(player2_hand) > 21:
            print_results(player1, player2, player1_hand, player2_hand)
            print('{} busted. {} wins!\n'.format(player2.name, player1.name))
            #player2.out('Sorry, you busted. You lose.\n')
            #player1.out(player1.name + ' busted. You win!\n')
        elif total(player1_hand) < total(player2_hand):
            print_results(player1, player2, player1_hand, player2_hand)
            print('{} score is lower. {} wins!\n'.format(player1.name, player2.name))
            #player1.out('Sorry, your score is lower than ' + player2.name + '. You lose.\n')
            #player2.out('Congratulations! You score is higher than ' + player1.name + '. You win!\n')
        elif total(player2_hand) < total(player1_hand):
            print_results(player1, player2, player1_hand, player2_hand)
            print('{} score is lower. {} wins!\n'.format(player2.name, player1.name))
            #player2.out('Sorry, your score is lower than ' + player1.name + '. You lose.\n')
            #player1.out('Congratulations! You score is higher than ' + player2.name + '. You win!\n')

    def game(player1, player2, pot=None):
        choice = 0
        #pot.reset()
        welcome = "\nWelcome to Blackjack!\n"
        print(welcome)
        #player1.out(welcome)
        #player2.out(welcome)

        dealer_hand = []

        player1_hand = []
        player2_hand = []

        for i in range(4):
            deck = Deck()
            deck.shuffle()
            dealer_hand.extend(deck.getCards())
        #shuffle again
        random.shuffle(dealer_hand)

        player1_hand.extend([dealer_hand[0], dealer_hand[2]])
        player2_hand.extend([dealer_hand[1], dealer_hand[3]])

        del dealer_hand[:4]

        if choice != 'q':

            dealer_card = 'The dealer is showing a ' + str(dealer_hand[0]) + '\n'
            print(dealer_card)

            #player1.out(dealer_card)
            #player2.out(dealer_card)

            player1_msg = 'Your hand: ' + str(player1_hand)[1:-1]
            player2_msg = 'Your hand: ' + str(player2_hand)[1:-1]

            print(player1.name + ' ' + player1_msg)
            print(player2.name + ' '+ player2_msg)
            print()

            #player1.out(player1_msg)
            #player2.out(player2_msg)

            blackjack(player1, player2, player1_hand, player2_hand)

            choice_msg = "Do you want to [H]it, [S]tand, or [Q]uit: "

            #player1.out(choice_msg)
            #player2.out(choice_msg)

            #choice1 = player1.inp().lower()
            #choice2 = player2.inp().lower()

            choice1 = input(player1.name + ' ' + choice_msg).lower()
            choice2 = input(player2.name + ' ' + choice_msg).lower()

            if choice1 == 'h':
                hit(player1_hand, dealer_hand)
                if choice2 == 'h':
                    hit(player2_hand, dealer_hand)
                    score(player1, player2, player1_hand, player2_hand)
                    play_again(player1, player2)
                elif choice2 == 's':
                    score(player1, player2, player1_hand, player2_hand)
                    play_again()
            elif choice1 == 's':
                if choice2 == 'h':
                    hit(player2_hand, dealer_hand)
                    score(player1, player2, player1_hand, player2_hand)
                    play_again(player1, player2)
                elif choice2 == 's':
                    score(player1, player2, player1_hand, player2_hand)
                    play_again(player1, player2)
            elif choice1 == 'q' or choice2 == 'q':
                pass
                #exit()
    pot = Pot()
    game(Players("A"), Players("B"))


        

if __name__ == "__main__":
    main()


    #haven't yet done the pot
    
