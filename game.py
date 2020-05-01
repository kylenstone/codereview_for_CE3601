"""3/31/2019

Implementation of game of war using pygame and CardClasses
"""
from CardClasses import *
import pygame
green = (0, 200, 50)

def show_hand(screen, player):
    """Displays all cards in hand of player on pygame display object"""
    x, y, space_between_cards = 5, 462, 5
    for card in player.hand:
        card.position_x, card.position_y = x, y
        screen.blit(card.image, (x, y))
        x += card.horizontal_demension + space_between_cards
#     REVIEW: It might be nice to separate the core game logic from the GUI presentation here.
#     The spacing could be intrinsic properties of a hand, with the show_hand function is only responsible
#     for blitting to the UI.  That would align this code with the 'one responsibility' paradigm

def select_card(player, mouse_x, mouse_y):
    """Player selects a card to play"""
    if mouse_x:
        for card in player.hand:
            lower_x, upper_x = (card.position_x, card.position_x + card.horizontal_demension)
            lower_y, upper_y = (card.position_y, card.position_y + card.vertical_demension)
            # REVIEW: spelling: 'dimension', not 'demension'
            # A docstring somewhere could tell readers your program follows basic catersian coordinates.
            # Then you wouldn't have to name things 'lower_', 'upper_', etc, you could just write card(x, y), etc.


            if mouse_x > lower_x and mouse_x < upper_x:
                if mouse_y > lower_y and mouse_y < upper_y:
                    player.selected_card = card

def load_card_images(player):
    "Loads image, and demensions to card objects"
    for card in player.hand:
        card.image = pygame.image.load("Cards/" + str(card) + ".png")
        width, hieght = card.image.get_size()
        card.horizontal_demension = width
        card.vertical_demension = hieght
#     REVIEW: Spelling: 'height' not 'hieght'

def play_selected_card(screen, player):
    """Display card that is selected on pygame display object"""
    x = player.selected_card.position_x = 220
    y = player.selected_card.position_y
    screen.blit(player.selected_card.image, (x,y))

def show_winner(screen, player1, player2, my_font):
    """Display text stating game winner at end of game"""
    screen.fill(green)
    winner = str(player1) if player1.score > player2.score else str(player2)
    textsurface = my_font.render("The winner is: " + winner, False, (0, 0, 0))
    screen.blit(textsurface, (100, 270))
#     REVIEW: move this function to a more appropriate place, thus maintaining better flow between functions down the page.
#     i.e. I'm reading about card positioning, then suddenly there's a 'show winner' function.

def update_selected_card_position(player, new_y_position):
    """Change the Y position of selected card to move card to played position"""
    if player.selected_card:
        player.selected_card.position_y = new_y_position

def evaluate(player1, player2):
    """determines who won round and updates their score"""
    round_winner = None
    if player1.selected_card and player2.selected_card:
        pygame.time.delay(1000)
        round_winner = player1 if player1.selected_card > player2.selected_card else player2
        round_winner.score += 1
        player1.selected_card, player2.selected_card = None, None
    return round_winner

def show_player_scores(screen, player1, player2):
    """Left corner is player 1 score, right corner is player 2 score"""
    font_size = 12
    my_font = pygame.font.SysFont('Times New Roman', font_size)
    textsurface1 = my_font.render("Player 1 score: " + str(player1.score), False, (0, 0, 0))
    textsurface2 = my_font.render("Player 2 score: " + str(player2.score), False, (0, 0, 0))
    screen.blit(textsurface1, (0,0))
    screen.blit(textsurface2, (470,0))

def flip_turns(player1, player2):
    """Negates Turn attributes of player1 and player2"""
    player1.turn = not player1.turn
    player2.turn = not player2.turn
#     This could be a single-line return statement: return not player1.turn, not player2.turn

def turn(player, mouse_x, mouse_y, new_y_position):
    """Player will select card using mouse_x, and mouse_y, card will be removed from hand and played"""
    select_card(player, mouse_x, mouse_y)
    player.remove_from_hand(player.selected_card)
    update_selected_card_position(player, new_y_position)

def winner_goes_first(winner, loser):
    """Sets the winner to the starter of the next round"""
    winner.turn = True
    loser.turn = False
#   REVIEW: This function could be separated into a 'settings' or 'setup' file, to simplify the main game file.

def main():
    """GAME of war, each player is given a hand of 10 cards, on each turn a player will select a card to play,
    players cards will be compared and the player with the greater in value card will be assigned a point for round victory.
    When all cards in hand have been played game ends and winner is displayed

    """

    sc_width, sc_height = 555, 555
    selected_card_y_pos_player_1 = 330
    selected_card_y_pos_player_2 = 230
    font_size = 30
    delay_time_ms = 1000
    number_of_cards = 10
    turn_count = 1

    deck = Deck()
    deck.deck_shuffle()
    player1 = Player(input("Player 1 name: "), hand = deck.draw(number_of_cards), turn = True)
    player2 = Player(input("Player 2 name: "), hand = deck.draw(number_of_cards))

    pygame.init()
    screen = pygame.display.set_mode((sc_width, sc_height))
    load_card_images(player1)
    load_card_images(player2)

    pygame.font.init()
    my_font = pygame.font.SysFont('Times New Roman', font_size)

    """Main Game Loop"""
    game_is_running = True
    while game_is_running:
        screen.fill(green)
        # REVIEW: This can be called once - it does not need to be called every time in the main game loop

        mouse_x, mouse_y = None, None
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game_is_running = False
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()

        if player1.turn:
            show_hand(screen, player1)
            turn(player1, mouse_x, mouse_y, selected_card_y_pos_player_1)
            if player1.selected_card:
                flip_turns(player1, player2)
        else:
            show_hand(screen, player2)
            turn(player2, mouse_x, mouse_y, selected_card_y_pos_player_2)
            if player2.selected_card:
                flip_turns(player1, player2)

        if player1.selected_card:
            play_selected_card(screen, player1)
        if player2.selected_card:
            play_selected_card(screen, player2)
        # REVIEW: Logically, these actions should probably be folded beneath turn()

        show_player_scores(screen, player1, player2)
        pygame.display.update()

        winner = evaluate(player1,player2)
        if winner:
            if winner == player1:
                winner_goes_first(player1, player2)
            else:
                winner_goes_first(player2, player1)
        # REVIEW: You might write a Round() class, which tracks the winner of the previous round.
        # This would further simplify the main game loop and the observability of the code.

        if not player1.hand and not player2.hand:
            show_winner(screen, player1, player2, my_font)
            pygame.display.update()
            pygame.time.delay(delay_time_ms)
            game_is_running = False

if __name__ == '__main__':
    main()