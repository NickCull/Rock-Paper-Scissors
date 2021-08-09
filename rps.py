import random

moves = ['rock', 'paper', 'scissors']


# all player type classes will inherit the behavior from the plater class
class Player():
    # always plays rock
    def __init__(self):
        self.score = 0

    def play(self):
        return 'rock'

    def learn(self, last_bot_move):
        pass


class RandomPlayer(Player):
    # random selection from moves
    def play(self):
        index = random.randint(0, 2)
        return moves[index]


class ReflectPlayer(Player):
    # remembers what move the opponent played last round, and plays that move
    # this round
    def __init__(self):
        Player.__init__(self)
        self.last_bot_move = None

    def play(self):
        if self.last_bot_move is None:
            return super().play()

        return self.last_bot_move

    def learn(self, last_bot_move):
        self.last_bot_move = last_bot_move


class CyclePlayer(Player):
    # cylces through list of moves
    def __init__(self):
        Player.__init__(self)
        self.last_move = None

    def play(self):
        move = None
        if self.last_move is None:
            move = super().play()
        else:
            index = moves.index(self.last_move) + 1
            if index >= len(moves):
                index = 0
            move = moves[index]
        self.last_move = move
        return move


class HumanPlayer(Player):
    # ask the user to input the move
    def play(self):
        human_move = input('Rock, Paper, Scissors? >\nOr control+c to quit\n')
        while human_move not in moves:
            human_move = input('Invalid move, try again\n')
        return human_move


class Game:
    # play game
    def __init__(self):
        # choose game type
        # Player / RandomPlayer / ReflectPlayer / CyclePlayer
        self.player1 = HumanPlayer()
        self.player2 = RandomPlayer()
        self.round = 0

    def play_game(self):
        # start game
        # welcome message / final score at end
        input('Rock Paper Scissors Go!' + '\nPress enter to play\n')
        try:
            while True:
                self.play_round()
                print('Score: Human ' + str(self.player1.score) + ' x bot ' +
                      str(self.player2.score) + '\n')
        except KeyboardInterrupt:
            print('\n\n')
            print('Thanks for playing!')
            if self.player1.score > self.player2.score:
                print('You win!')
            elif self.player1.score < self.player2.score:
                print('You lose!')
            else:
                print('It\'s a draw!')
            print('The final score was ' + str(self.player1.score) + ' x ' +
                  str(self.player2.score))

    def play_round(self):
        player1_move = self.player1.play()
        player2_move = self.player2.play()
        result = Game.check_result(player1_move, player2_move)

        self.player1.learn(player2_move)
        self.player2.learn(player1_move)

        print('\nYou played ' + player1_move + '. \nThe bot played ' +
              player2_move + '.')

        self.round += 1
        if result == 1:
            self.player1.score += 1
            print('** You won! **')
        elif result == 2:
            self.player2.score += 1
            print('** The bot won! **')
        else:
            print('** Tie **')
        print(f"Round {self.round} --")


    def check_result(move1, move2):
        if Game.is_move_stronger(move1, move2):
            return 1
        elif Game.is_move_stronger(move2, move1):
            return 2
        else:
            return 0

    def is_move_stronger(move1, move2):
        if (move1 == 'scissors' and move2 == 'paper'):
            return True
        elif (move1 == 'rock' and move2 == 'scissors'):
            return True
        elif (move1 == 'paper' and move2 == 'rock'):
            return True
        return False


if __name__ == "__main__":
    # entry point: create a new game instance and start game
    game = Game()
    game.play_game()
