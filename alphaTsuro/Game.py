import pygame
from Board import Board
from Deck import Deck
from Tile import Tile
WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        self.board = Board()
        self.deck = Deck.from_json("data/testDeck.json")
        self.initialize_screen()
        self.board.draw(self.screen)
        self.deck.draw().draw(self.screen, 40, 40)
        pygame.display.flip()
        self.game_loop()

    def initialize_screen(self):
        pygame.init()
        size = [400, 400]
        self.screen = pygame.display.set_mode(size)
        self.screen.fill(WHITE)

    def game_loop(self):
        #Loop until the user clicks the close button.
        done = False
        clock = pygame.time.Clock()
         
        while not done:
         
            # This limits the while loop to a max of 10 times per second.
            # Leave this out and we will use all CPU we can.
            clock.tick(10)
             
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done=True # Flag that we are done so we exit this loop