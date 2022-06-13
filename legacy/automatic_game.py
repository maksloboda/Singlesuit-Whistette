from deep_green import *

class CompWithCompGame:
    def __init__(self):
        self.player0 = DeepGreen()
        self.player0.a, self.player0.b = 0, 1
        self.player1 = DeepGreen()
        self.player1.a, self.player1.b = 1, 0
        self.K = 0
        self.card = []

    def Play(self, vector0, vector1, first_player=0):
        for i in range(len(vector0)):
            self.card.append(i + 1)

        self.player0.card = self.card
        self.player1.card = self.card

        p0 = Position(vector0)
        p0.curr_player = first_player
        p1 = Position(vector1)
        p1.curr_player = (p0.curr_player + 1) % 2

        self.player0.PositionPreview(p0, MIN_CONST)
        self.player1.PositionPreview(p1, MIN_CONST)

        for i in range(self.K):
            if p0.curr_player == 0:
                mot0 = best_mot[self.player0.h(p0)]
                print('Ход 0:', self.card[mot0], end='  ')
                self.player0.PrintAddInf(p0)

                ip0 = InterPosition(p0, mot0)
                ip1 = InterPosition(p1, mot0)

                time.sleep(1)
                mot1 = best_mot[self.player1.h(ip1)]
                print('Ход 1:', self.card[mot1], end='  ')
                self.player1.PrintAddInf(ip1)
                bribe = self.player0.weights[self.K - ip0.size // 2]
                p0 = Position([], ip0, mot1, bribe)
                p1 = Position([], ip1, mot1, bribe)
                self.card.pop(max(mot0, mot1))
                self.card.pop(min(mot0, mot1))
                time.sleep(1)
            else:
                mot1 = best_mot[self.player1.h(p1)]
                print('Ход 1:', self.card[mot1], end='  ')
                self.player1.PrintAddInf(p1)

                ip0 = InterPosition(p0, mot1)
                ip1 = InterPosition(p1, mot1)

                time.sleep(1)
                mot0 = best_mot[self.player0.h(ip0)]
                print('Ход 0:', self.card[mot0], end='  ')
                self.player0.PrintAddInf(ip0)
                bribe = self.player0.weights[self.K - ip0.size // 2]
                p0 = Position([], ip0, mot0, bribe)
                p1 = Position([], ip1, mot0, bribe)
                self.card.pop(max(mot0, mot1))
                self.card.pop(min(mot0, mot1))
                time.sleep(1)

        if self.player0.greater(p0.k[0], p0.k[1]):
            print('0 Победил!')
        elif p0.k[0] == p0.k[1]:
            print('НИЧЬЯ')
        else:
            print('1 Победил!')

    def Game(self, lines):
        l = lines[1].split(' ')
        if l[2] != 'normal':
            self.player0.change_type_to_tiny()
            self.player1.type = 'tiny'
        l = lines[3].split(' ')
        first_player = int(l[2])

        vector0 = []
        vector1 = []
        l = lines[4].split()
        if len(l) > 2:
            vector0 = self.player0.read_vector(lines[4][8:])
            vector1 = self.player1.read_vector(lines[4][8:])
            self.K = self.player0.K
        else:
            l = lines[5].split()
            self.K = int(l[2])
            self.player0.K = self.K
            self.player1.K = self.K
            kit0 = set(map(int, lines[7][8:].split()))
            print(kit0)
            if (len(kit0) != self.K):
                print('MISTAKE!')
                return
            for i in range(2 * self.K):
                if (i + 1) in kit0:
                    vector0.append(0)
                    vector1.append(1)
                else:
                    vector0.append(1)
                    vector1.append(0)
        print('Двоичный вектор:', *vector0)

        l = lines[8].split(' ')
        if len(l) > 1:
            self.player0.weights = list(map(int, lines[8][8:].split()))
            self.player1.weights = self.player0.weights
            self.player0.mode = 'weights'
            self.player1.mode = 'weights'
        else:
            self.player0.weights = [1] * self.K
            self.player1.weights = self.player0.weights

        self.player0.print_cards(vector0)
        self.Play(vector0, vector1, first_player)