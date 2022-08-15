# # Game Class
import random

class TicTacToe:
    def __init__(self, board = ['_' for i in range(9)]):
        self.board = board
        self.winner = None
        
        #extension
        self.available_moves = [i for i in range(9) if board[i] == '_']
        
    def print_board(self):
        print('-------status-------')
        for i in range(3):
            print('---    '+' '.join(self.board[i*3:(i+1)*3]) + '     ---')
        print('--------------------')   
        
    @staticmethod
    def print_board_nums():
        for i in range(3):
            print(' '.join([str(i*3 + x) for x in range(3)]))

    
    def print_available_moves(self):
        print('---avilable moves---')
        print(self.available_moves)
        print('--------------------')
    
    #for AI COM
    def unmake_move(self, move, index):
        self.board[move] = '_'
        self.available_moves.insert(index, move)
        
        
    def make_move(self, move, player):
        self.board[move] = player.letter
        self.available_moves.remove(move)
        
    def reset_game(self):
        self.board = ['_' for i in range(9)]
        self.available_moves = [i for i in range(9)]
        
    def game_finished(self, player):
        #check columns
        for i in range(3):
            for j in range(3):
                if self.board[j*3 + i] != player.letter:
                    break
                if j == 2:
                    self.winner = player
                    return True
        #check rows       
        for i in range(3):
            for j in range(3):
                if self.board[i*3 + j] != player.letter:
                    break
                if j == 2:
                    self.winner = player
                    return True    
    
        #check diags
        if self.board[4] != player.letter:
            return False
        if self.board[0] == player.letter and self.board[8] == player.letter:
            self.winner = player
            return True
        if self.board[2] == player.letter and self.board[6] == player.letter:
            self.winner = player
            return True
        
        return False
        


# # Player Class

class Player:
    # letter O or X
    def __init__(self, letter):
        self.letter = letter
        

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
        self.name = input("Enter you'r name: ")
    
    def get_move(self, game):
        while True:
            inp = input('Enter your move: ')
            try:
                inp = int(inp)
                if inp in game.available_moves:
                    break
                else:
                    print('these are available moves')
                    game.print_available_moves()
                    raise ValueError
                
            except ValueError:
                print('invalid move, try again')
                
        return inp   

class AI:
    def __init__(self, player, letter):
        self.letter = letter
        self.name = 'AI'
        self.vs_player = player
        
    def get_move(self, game):
        if len(game.available_moves) == 9:
            return random.randint(0, 9)
        
        def multiplier(player):
            return 1 if player == self else -1
        
        def get_score(player, game):
            #check for game status
            if game.game_finished(player):
                return multiplier(player)*(len(game.available_moves) + 1)
            elif len(game.available_moves) == 0:
                return 0
            
            #recursion
            #for COM we should maximize best score and need smallest number
            best_score = multiplier(player)*float('inf')
            #change player
            player = self.vs_player if player == self else self 
            #for each available move
            for index, move in enumerate(game.available_moves):
                #try
                game.make_move(move, player)
                #get best score for given player
                current_score = get_score(player, game)
                if multiplier(player) == 1:
                    best_score = max(best_score, current_score)
                else:
                    best_score = min(best_score, current_score) 
                #undo try
                game.unmake_move(move, index)
                
            return best_score
        
        moves = {}
        # adding extra loop to return move which has highest score
        for index, move in enumerate(game.available_moves):
            #try
            game.make_move(move, self)
            #get best score for given player
            moves[move] = get_score(self, game)
                    
            #undo try
            game.unmake_move(move, index) 
        print(moves) 
        result = max(moves, key=moves.get)
        if moves[result] > 0:
            return result
        moves = {key:value for key, value in moves.items() if value == 0}
        #random choice from zeroes
        return random.choice(list(moves.keys()))
            

class BasicComputer(Player):
    def __init__(self, letter):
        super().__init__(letter)
        self.name = 'COM-L'
        
    def get_move(self, game):
        return random.choice(game.available_moves)


def play(game, p1, p2, show=True):
    if show:
        game.print_board()
        game.print_available_moves()
    
    current_p = p1
    move = -1
    
    while len(game.available_moves) > 0:
        print(f"it's {current_p.name}'s move")
        move = current_p.get_move(game)
        
        game.make_move(move, current_p)
        
        #check for win condition only if 5 moves have passed
        if len(game.available_moves) <= 4:
            status = game.game_finished(current_p)
            if status:
                game.print_board()
                print(f'winner is {game.winner.name}')
                break
            
        current_p = p2 if current_p == p1 else p1
        
        #for com no need to show
        if show:
            game.print_board()
            game.print_available_moves()
    game.reset_game()


def get_players(n, player=None):
    if n == 0:
        p1 = HumanPlayer('X')
        p2 = AI(p1, 'O')
    elif n == 1:
        p2 = HumanPlayer('O')
        p1 = AI(p2, 'X')
    else:
        p1 = HumanPlayer('X')
        p2 = HumanPlayer('O')
    return p1, p2


def dialog_to_get_type():
    print('Possible matches:')
    print('   H vs AI : 0')
    print('   AI vs H : 1')
    print('   H vs H  : 2')
    tp = -1
    while tp not in [0,1,2]:
        try:
            tp = int(input('Enter your choice of game: '))
        except:
            pass
    return tp


def end_or_continue():
    print('Wanna continue?')
    while True:
        diag = input('Y/N: ')
        if diag in ['Y', 'N']:
            return diag == 'Y'


game = TicTacToe()
while True:
    tp = dialog_to_get_type()
    p1, p2 = get_players(tp)
    play(game, p1, p2)
    print('game finished')
    if not end_or_continue():
        print('good game')
        break



