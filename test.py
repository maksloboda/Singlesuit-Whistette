import copy


class Position:
    def __init__(self, mask=None, ip=None, mot=None):
        self.k = [0] * 2
        self.curr_player = 0
        self.table = 0
        self.key = -1
        self.count2 = 0
        if ip is None:
            self.mask = copy.copy(mask)
        else:
            self.mask = copy.copy(ip.mask)
            self.mask[mot - 1] = 2
            self.count2 = ip.count2 + 1
            i = ip.curr_player
            j = (ip.curr_player + 1) % 2
            if mot > ip.table:
                self.curr_player = i
                self.k[i] = ip.k[i] + 1
                self.k[j] = ip.k[j]
            else:
                self.curr_player = j
                self.k[i] = ip.k[i]
                self.k[j] = ip.k[j] + 1


class InterPosition:
    def __init__(self, p, mot):
        self.mask = copy.copy(p.mask)
        self.mask[mot - 1] = 2
        self.k = p.k
        self.curr_player = (p.curr_player + 1) % 2
        self.table = mot
        self.key = -1
        self.count2 = p.count2 + 1

f = {}
optimal_moves = {}


class DeepGreen:
    def __init__(self, K=3):
        self.K = K
        self.type = 'ordinary'

    def h(self, p):
        if p.key == -1:
            p.key = p.curr_player
            for i in range(2 * self.K):
                p.key = p.key * 3 + p.mask[i]

        return (p.key, p.k[0], p.k[1], p.table)

    def InterPositionPreview(self, ip, bound=-100):
        if ip.curr_player == 0:
            Min = 100
            MinUpTable = 100
            for i in range(2 * self.K):
                if ip.mask[i] != 0:
                    continue

                card = i + 1
                if card < Min:
                    Min = card
                if card < MinUpTable and card > ip.table:
                    MinUpTable = card

            # 1)
            p1 = Position([], ip, Min)
            self.PositionPreview(p1)
            f[self.h(ip)] = f[self.h(p1)]
            optimal_moves[self.h(ip)] = [Min]

            # 2)
            if MinUpTable != 100 and MinUpTable != Min:
                p2 = Position([], ip, MinUpTable)
                self.PositionPreview(p2, f[self.h(ip)])  # bound = f[self.h(ip)] - Текущее значение ф-ии
                if f[self.h(p2)] > f[self.h(ip)]:
                    f[self.h(ip)] = f[self.h(p2)]
                    optimal_moves[self.h(ip)][0] = MinUpTable
                elif f[self.h(p2)] == f[self.h(ip)]:
                    optimal_moves[self.h(ip)].append(MinUpTable)

            #print(ip.mask, ' table: ', ip.table, ' ', f[self.h(ip)], ' ', optimal_moves[self.h(ip)])

        else:
            m = 100
            for i in range(2 * self.K):
                if ip.mask[i] != 1:
                    continue

                card = i + 1
                v = Position([], ip, card)
                self.PositionPreview(v)

                if f[self.h(v)] <= bound:
                    f[self.h(ip)] = f[self.h(v)]
                    return

                if (f[self.h(v)] < m):
                    m = f[self.h(v)]

            f[self.h(ip)] = m

    def PositionPreview(self, p, bound=-100):
        if p.count2 == 2 * self.K:
            f[self.h(p)] = p.k[0] - p.k[1]
            return

        if p.curr_player == 0:
            poss_moves = []
            m = -100
            step = 0
            for i in range(2 * self.K):
                if p.mask[i] != 0 or (i != 0 and p.mask[i] == p.mask[i - 1]):
                    continue

                card = i + 1
                b = InterPosition(p, card)
                self.InterPositionPreview(b, m)  # bound = m - ходы с меньшим итогом недопустимы
                poss_moves.append([card, f[self.h(b)]])
                if (f[self.h(b)] > m):
                    m = f[self.h(b)]
                    step = card

            f[self.h(p)] = m
            optimal_moves[self.h(p)] = [step]

            for move in poss_moves:
                if (move[1] == m and move[0] != step):
                    optimal_moves[self.h(p)].append(move[0])

            #print(p.mask, ' ', f[self.h(p)], '  best mot: ', optimal_moves[self.h(p)])
        else:
            m = 100
            for i in range(2 * self.K):
                if p.mask[i] != 1:
                    continue

                card = i + 1
                b = InterPosition(p, card)
                self.InterPositionPreview(b)

                if f[self.h(b)] <= bound:
                    f[self.h(p)] = f[self.h(b)]
                    return

                if (f[self.h(b)] < m):
                    m = f[self.h(b)]

            f[self.h(p)] = m

    def TinyInterPositionPreview(self, ip, bound=100):
        if ip.curr_player == 0:
            Max = -100
            MaxLessTable = -100
            for i in range(2 * self.K):
                if ip.mask[i] != 0:
                    continue

                card = i + 1
                if card > Max:
                    Max = card
                if card > MaxLessTable and card < ip.table:
                    MaxLessTable = card

            # 1)
            p1 = Position([], ip, Max)
            self.TinyPositionPreview(p1)
            f[self.h(ip)] = f[self.h(p1)]
            optimal_moves[self.h(ip)] = [Max]

            # 2)
            if MaxLessTable != -100 and MaxLessTable != Max:
                p2 = Position([], ip, MaxLessTable)
                self.TinyPositionPreview(p2, f[self.h(ip)])  # bound = f[self.h(ip)] - Т
                if f[self.h(p2)] < f[self.h(ip)]:
                    f[self.h(ip)] = f[self.h(p2)]
                    optimal_moves[self.h(ip)][0] = MaxLessTable
                elif f[self.h(p2)] == f[self.h(ip)]:
                    optimal_moves[self.h(ip)].append(MaxLessTable)

            #print(ip.mask, ' table: ', ip.table, ' ', f[self.h(ip)], ' ', optimal_moves[self.h(ip)])

        else:
            m = -100
            for i in range(2 * self.K):
                if ip.mask[i] != 1:
                    continue

                card = i + 1
                v = Position([], ip, card)
                self.TinyPositionPreview(v)

                if f[self.h(v)] >= bound:
                    f[self.h(ip)] = bound
                    return

                if (f[self.h(v)] > m):
                    m = f[self.h(v)]

            f[self.h(ip)] = m

    def TinyPositionPreview(self, p, bound=100):
        if p.count2 == 2 * self.K:
            f[self.h(p)] = p.k[0] - p.k[1]
            return

        if p.curr_player == 0:
            poss_moves = []
            m = 100
            step = 0
            for i in range(2 * self.K):
                if p.mask[i] != 0 or (i != 0 and p.mask[i] == p.mask[i - 1]):
                    continue

                card = i + 1
                b = InterPosition(p, card)
                self.TinyInterPositionPreview(b, m)
                poss_moves.append([card, f[self.h(b)]])
                if (f[self.h(b)] < m):
                    m = f[self.h(b)]
                    step = card

            f[self.h(p)] = m
            optimal_moves[self.h(p)] = [step]

            for move in poss_moves:
                if (move[1] == m and move[0] != step):
                    optimal_moves[self.h(p)].append(move[0])

            #print(p.mask, ' ', f[self.h(p)], '  best mot: ', optimal_moves[self.h(p)])
        else:
            m = -100
            for i in range(2 * self.K):
                if p.mask[i] != 1:
                    continue

                card = i + 1
                b = InterPosition(p, card)
                self.TinyInterPositionPreview(b)

                if f[self.h(b)] >= bound:
                    f[self.h(p)] = f[self.h(b)]
                    return

                if (f[self.h(b)] > m):
                    m = f[self.h(b)]

            f[self.h(p)] = m

    def Play(self):
        print('Выберите K')
        self.K = int(input())
        print('Выберите вид игры (обычная или мизерная)')
        s = input()
        if (s == 'мизерная'):
            self.type = 'tiny'
        print('Введите двоичный вектор')
        mask = list(map(int, input().split()))
        p = Position(mask)
        a = 0  # a - игрок за которого играет комп
        b = 1  # b - игрок за которого играет User

        print('Выберете игрока (0 или 1)')
        player = int(input())
        if player == 0:
            a, b = b, a
            for i in range(2 * self.K):
                p.mask[i] = (p.mask[i] + 1) % 2
            p.curr_player = 1

        #print(p.mask)

        if self.type == 'ordinary':
            self.PositionPreview(p)
        else:
            self.TinyPositionPreview(p)

        for i in range(self.K):
            if p.curr_player == 0:
                comp_mot = optimal_moves[self.h(p)][0]
                print('Ход ', a, ': ', comp_mot, sep='', end='  ')

                if len(optimal_moves[self.h(p)]) == 1:
                    print('Других оптимальных ходов нет')
                else:
                    print('Другие оптимальные ходы:', optimal_moves[self.h(p)][1:])

                ip = InterPosition(p, comp_mot)
                print('Ход ', b, ': ', sep='', end='')
                user_mot = int(input())
                p = Position([], ip, user_mot)
            else:
                print('Ход ', b, ': ', sep='', end='')
                user_mot = int(input())
                ip = InterPosition(p, user_mot)
                comp_mot = optimal_moves[self.h(ip)][0]
                print('Ход ', a, ': ', comp_mot, sep='', end='  ')

                if len(optimal_moves[self.h(ip)]) == 1:
                    print('Других оптимальных ходов нет')
                else:
                    print('Другие оптимальные ходы:', optimal_moves[self.h(ip)][1:])

                p = Position([], ip, comp_mot)

        if self.type == 'ordinary':
            if p.k[0] > p.k[1]:
                print(a, 'Победил!')
            elif p.k[0] == p.k[1]:
                print('НИЧЬЯ')
            else:
                print(b, 'Победил!')
        else:
            if p.k[0] < p.k[1]:
                print(a, 'Победил!')
            elif p.k[0] == p.k[1]:
                print('НИЧЬЯ')
            else:
                print(b, 'Победил!')