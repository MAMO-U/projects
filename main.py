import random
import time

# Constant
CARDS = ["ACE", 2, 3, 4, 5, 6, 7, 8, 9, 10, "K", "Q", "J", "ACE", 2, 3, 4, 5, 6, 7, 8, 9, 10, "K", "Q", "J",
         "ACE", 2, 3, 4, 5, 6, 7, 8, 9, 10, "K", "Q", "J", "ACE", 2, 3, 4, 5, 6, 7, 8, 9, 10, "K", "Q", "J"]
# Variables
bet = 0
bank = 300
sec_card = 0
playing = True
dealer_hand = []
player_hand = []
deck = []


# Put a bet
def bet_on(balance):
    global bet
    if (balance > 0) and (balance <= 50):
        bet = bank
        return print(f"You only have {bet} to bet")
    bet = int(input("How much you wanna bet?: "))
    if bet > balance:
        print("You have less money")
        return bet_on(bank)
    if (bet < 50) and (bet <= balance):
        print("Minimum bet is 50$")
        return bet_on(bank)


# Count total of a hand
def hand_total(hand):
    total = 0
    for card in hand:
        if (card == "K") or (card == "Q") or (card == "J"):
            total += 10
        elif card == "ACE":
            total += 11
        elif card == "?":
            pass
        else:
            total += card
    if (total > 21) and ("ACE" in hand):
        a = hand.count("ACE")
        total -= 10 * a
    return total


# Dealing cards for dealer and player
def deal(deck_cards):
    global deck
    global player_hand
    global dealer_hand
    global sec_card
    player_hand.clear()
    dealer_hand.clear()
    deck.clear()
    deck = deck_cards.copy()
    random.shuffle(deck)
    for card in range(0, 2):
        dealer_hand.append(deck[0])
        deck.pop(0)
        player_hand.append(deck[0])
        deck.pop(0)
    sec_card = dealer_hand[1]
    dealer_hand[1] = "?"


# Choose to hit or stand
def hit_stand():
    decision = input('Pick what to do "Hit" or "Stand"?: ')
    if decision.lower() == "hit":
        print("======================================================")
        return hit()
    elif decision.lower() == "stand":
        print("======================================================")
        return stand(player_hand, bank)
    else:
        print("======================================================")
        return hit_stand()


# Called when player stand or will be called automatically player hit 21 or goes over 21
# Check if dealer needs to pick one more card or no
def stand(player, balance):
    global dealer_hand
    global deck
    dealer_hand[1] = sec_card
    print("**Dealer 2nd card revealed**")
    info(dealer_hand, player, balance)
    print("======================================================")
    time.sleep(3)
    if (hand_total(player) == hand_total(dealer_hand)) and (hand_total(dealer_hand) < 16):
        add_card_dealer()
        print("**Dealer picked a card**")
        info(dealer_hand, player, balance)
        print("======================================================")
        time.sleep(3)
    elif (hand_total(player) > hand_total(dealer_hand)) and (hand_total(player) <= 21):
        while hand_total(player) >= hand_total(dealer_hand):
            add_card_dealer()
            print("**Dealer picked a card**")
            info(dealer_hand, player, balance)
            print("======================================================")
            time.sleep(3)


# Everytime player choose to hit adds card to his hand
def hit():
    global player_hand
    global deck
    player_hand.append(deck[0])
    deck.pop(0)
    print("**Player picked a card**")
    info(dealer_hand, player_hand, bank)
    if hand_total(player_hand) > 21:
        print("======================================================")
        print("*** You BUST ***")
        stand(player_hand, bank)
    elif hand_total(player_hand) == 21:
        print("======================================================")
        print("*** You hit BLACKJACK ***")
        stand(player_hand, bank)
    else:
        hit_stand()


# Add card to the dealer hand
def add_card_dealer():
    global dealer_hand
    global deck
    dealer_hand.append(deck[0])
    deck.pop(0)


# To show the balance, hands, total of both hands
def info(d_hand, p_hand, balance):
    print(f"Your balance= {balance}$        Your bet= {bet}$")
    print(f"Dealer hand : {d_hand}   Total={hand_total(d_hand)}")
    print(f"Player hand : {p_hand}   Total={hand_total(p_hand)}")


# Main
print("WELCOME TO BLACKJACK")
while (bank > 0) and playing:
    print(f"Your balance= {bank}$")
    bet_on(bank)
    deal(CARDS)
    info(dealer_hand, player_hand, bank)
    hit_stand()

    p_hand = hand_total(player_hand)
    d_hand = hand_total(dealer_hand)
    if ((p_hand > d_hand) and (p_hand <= 21)) or ((d_hand > 21) and (p_hand <= 21)):
        print(f"You won {bet * 2}$")
        bank += bet
    elif ((d_hand > p_hand) and (d_hand <= 21)) or ((p_hand > 21) and (d_hand <= 21)):
        print(f"You lost {bet}$")
        bank -= bet
    else:
        print("It's a tie")

    if bank > 0:
        keep_going = input('You want to keep playing click "Enter" if you want to cash out type "out"')
        if keep_going.strip().lower() == "out":
            playing = False
    print("======================================================")
print("======================================================")

if not playing:
    print(f"You Cash out {bank}")
else:
    print("You bankrupted, that's why gamba is haram")
