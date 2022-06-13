from positions import *

f = {}
optimal_moves = {}
better_beat = {}
better_skip = {}
can_beat = {}
can_skip = {}
takings = {}
skippings = {}
best_mot = {}
bad_moves = {}

MAX_CONST = 10000
MIN_CONST = -10000

class DeepGreen:
    def __init__(self):
        self.type = 'normal'
        self.K = 0
        self.a = 0
        self.b = 1
        self.card = []
        self.mode = 'normal'
        self.weights = []

    def h(self, p):
        return (p.mask, p.curr_player, p.table)

    def g(self, p):
        if self.h(p) in f:
            return f[self.h(p)] + p.x
        if p.size == 0:
            return p.x
        return MIN_CONST

    def less(self, a, b):
        if self.type == 'normal':
            return a < b
        else:
            return a > b

    def greater(self, a, b):
        if self.type == 'normal':
            return a > b
        else:
            return a < b

    def Range(self, n):
        if self.type == 'normal':
            return range(n)
        else:
            return range(n - 1, -1, -1)

    def change_type_to_tiny(self):
        global MAX_CONST, MIN_CONST
        self.type = 'tiny'
        MAX_CONST, MIN_CONST = MIN_CONST, MAX_CONST

    def AddInterPositionPreview(self, ip, poss_moves):
        if self.type == 'tiny' or self.mode == 'weights':
            return

        better_beat[self.h(ip)] = True
        better_skip[self.h(ip)] = True
        can_beat[self.h(ip)] = False
        can_skip[self.h(ip)] = False
        for [i, g] in poss_moves:
            if i > ip.table:
                can_beat[self.h(ip)] = True
                if g == f[self.h(ip)]:
                    better_skip[self.h(ip)] = False
            else:
                can_skip[self.h(ip)] = True
                if g == f[self.h(ip)]:
                    better_beat[self.h(ip)] = False

    def AddPositionPreview(self, p, poss_moves):
        if self.type == 'tiny' or self.mode == 'weights':
            return

        bad_moves[self.h(p)] = 0
        for move in poss_moves:
            if move > f[self.h(p)]:
                bad_moves[self.h(p)] += 1

    def find_best_mot(self, p):
        if self.type == 'tiny':
            return optimal_moves[self.h(p)][0]
        elif self.mode == 'weights' or len(optimal_moves[self.h(p)]) == 1:
            return optimal_moves[self.h(p)][0]
        elif p.table != -1:
            b = Position([], p, optimal_moves[self.h(p)][0], 1)
            if bad_moves[self.h(b)] > b.size / 10:
                return optimal_moves[self.h(p)][0]
            else:
                return optimal_moves[self.h(p)][1]
        else:
            takings[self.h(p)] = []
            skippings[self.h(p)] = []
            prev = -100
            b = InterPosition(p, optimal_moves[self.h(p)][0])
            for mot in optimal_moves[self.h(p)]:
                if mot != prev + 1:
                    b = InterPosition(p, mot)
                if (better_beat[self.h(b)]) and (can_skip[self.h(b)]):
                    skippings[self.h(p)].append(mot)
                elif (better_skip[self.h(b)]) and (can_beat[self.h(b)]):
                    takings[self.h(p)].append(mot)
                prev = mot

            if (len(takings[self.h(p)]) != 0) and (len(skippings[self.h(p)]) != 0):
                if p.size - 1 - skippings[self.h(p)][-1] < takings[self.h(p)][0]:
                    return skippings[self.h(p)][-1]
                else:
                    return takings[self.h(p)][0]
            elif len(takings[self.h(p)]) != 0:
                return takings[self.h(p)][0]
            elif len(skippings[self.h(p)]) != 0:
                return skippings[self.h(p)][-1]
            else:
                return optimal_moves[self.h(p)][0]

    def AlternInterPositionPreviewWeights(self, ip, bribe):
        poss_moves = []
        m = MIN_CONST
        step = 0
        prev = -100
        prev_g = 0
        for i in self.Range(ip.size):
            if pl(ip.mask, ip.size - i - 1) != 0:
                continue

            elif abs(i - prev) == 1:
                poss_moves.append([i, prev_g])
                prev = i
                continue

            v = Position([], ip, i, bribe)
            self.PositionPreview(v, m - v.x)  # bound = m - v.x - ходы с меньшим итогом недопустимы

            if (self.g(v) == MIN_CONST):
                continue

            poss_moves.append([i, self.g(v)])
            if self.greater(self.g(v), m):
                m = self.g(v)
                step = i

            prev = i
            prev_g = self.g(v)

        f[self.h(ip)] = m
        optimal_moves[self.h(ip)] = [step]

        for move in poss_moves:
            if (move[1] == m and move[0] != step):
                optimal_moves[self.h(ip)].append(move[0])

        best_mot[self.h(ip)] = self.find_best_mot(ip)

    def InterPositionPreview(self, ip, bound):
        if (self.h(ip) in f):
            # print('Old InterPosition', 'mask:', make_vector(ip.mask), 'key = ', self.h(ip), 'x=', ip.x, 'f=',
            # f[self.h(ip)], 'g=', self.g(ip))
            return

        bribe = self.weights[self.K - ip.size // 2]

        if ip.curr_player == 0:
            if self.mode == 'weights':
                self.AlternInterPositionPreviewWeights(ip, bribe)
                return

            Min = MAX_CONST
            MinUpTable = MAX_CONST
            for i in self.Range(ip.size):
                if pl(ip.mask, ip.size - i - 1) != 0:
                    continue

                if self.less(i, Min):
                    Min = i
                if self.less(i, MinUpTable) and self.greater(i, ip.table):
                    MinUpTable = i


            # 1)
            p1 = Position([], ip, Min, bribe)
            self.PositionPreview(p1, MIN_CONST)
            f[self.h(ip)] = self.g(p1)
            optimal_moves[self.h(ip)] = [Min]

            # 2)
            if MinUpTable != MAX_CONST and MinUpTable != Min:
                p2 = Position([], ip, MinUpTable, bribe)
                self.PositionPreview(p2, f[self.h(ip)] - p2.x)  # bound = f[self.h(ip)] - p2.x
                # - Текущее значение ф-ии
                if self.greater(self.g(p2), f[self.h(ip)]):
                    f[self.h(ip)] = self.g(p2)
                    optimal_moves[self.h(ip)][0] = MinUpTable
                elif self.g(p2) == f[self.h(ip)]:
                    if self.type == 'normal':
                        optimal_moves[self.h(ip)].append(MinUpTable)
                    else:
                        optimal_moves[self.h(ip)] = [MinUpTable, Min]

            best_mot[self.h(ip)] = self.find_best_mot(ip)

            # print('InterPosition, 0 mot:', 'mask:', make_vector(ip.mask), 'key = ', self.h(ip), 'x=', ip.x, 'f=', f[self.h(ip)], 'g=', self.g(ip))

        else:
            m = MAX_CONST
            step = -100
            poss_moves = []
            for i in self.Range(ip.size):
                if pl(ip.mask, ip.size - i - 1) != 1:
                    continue

                v = Position([], ip, i, bribe)
                self.PositionPreview(v, MIN_CONST)

                if self.less(self.g(v), bound):
                    return

                poss_moves.append([i, self.g(v)])

                if self.less(self.g(v), m):
                    m = self.g(v)
                    step = i

            f[self.h(ip)] = m
            self.AddInterPositionPreview(ip, poss_moves)

            # print('InterPosition, 1 mot:', 'mask:', make_vector(ip.mask), 'key = ', self.h(ip), 'x=', ip.x, 'f=', f[self.h(ip)], 'g=', self.g(ip))

    def PositionPreview(self, p, bound):
        if (self.h(p) in f):
            # print('Old Position', 'mask:', make_vector(p.mask), 'key = ', self.h(p), 'x=', p.x, 'f=', f[self.h(p)],
            # 'g=', self.g(p))
            return

        if p.size == 0:
            # print('End Position:', 'mask:', make_vector(p.mask), 'key = ', self.h(p), 'g=', self.g(p))
            return

        if p.curr_player == 0:
            poss_moves = []
            m = MIN_CONST
            step = 0
            prev = -100
            prev_g = 0
            for i in self.Range(p.size):
                if pl(p.mask, p.size - i - 1) != 0:
                    continue

                elif abs(i - prev) == 1:
                    poss_moves.append([i, prev_g])
                    prev = i
                    continue

                b = InterPosition(p, i)
                self.InterPositionPreview(b, m)  # bound = m - ходы с меньшим итогом недопустимы
                if (self.g(b) == MIN_CONST):
                    continue

                poss_moves.append([i, self.g(b)])
                if self.greater(self.g(b), m):
                    m = self.g(b)
                    step = i

                prev = i
                prev_g = self.g(b)

            f[self.h(p)] = m
            optimal_moves[self.h(p)] = [step]

            for move in poss_moves:
                if (move[1] == m and move[0] != step):
                    optimal_moves[self.h(p)].append(move[0])

            best_mot[self.h(p)] = self.find_best_mot(p)

            # print('Position, 0 mot:', 'mask:', make_vector(p.mask), 'key = ', self.h(p), 'x=', p.x, 'f=', f[self.h(p)], 'g=', self.g(p))

        else:
            poss_moves = []
            m = MAX_CONST
            prev = -100
            for i in self.Range(p.size):
                if pl(p.mask, p.size - i - 1) != 1:
                    continue

                b = InterPosition(p, i)
                self.InterPositionPreview(b, MIN_CONST)

                if self.less(self.g(b), bound):
                    return

                if abs(i - prev) != 1:
                    poss_moves.append(self.g(b))

                if self.less(self.g(b), m):
                    m = self.g(b)

                prev = i

            f[self.h(p)] = m
            self.AddPositionPreview(p, poss_moves)

            # print('Position, 1 mot:', 'mask:', make_vector(p.mask), 'key = ', self.h(p), 'x=', p.x, 'f=', f[self.h(p)], 'g=', self.g(p))

    def PrintAddInf(self, p):
        if len(optimal_moves[self.h(p)]) == 1:
            print('Других оптимальных ходов нет |', end=' ')
        else:
            print('Все оптимальные ходы:', end=' ')
            for i in optimal_moves[self.h(p)]:
                print(self.card[i], end=' ')
            print('| ', end='')

        if self.h(p) in takings:
            if len(takings[self.h(p)]) == 0:
                print('Взятий нет |', end=' ')
            else:
                print('Взятия:', end=' ')
                for i in takings[self.h(p)]:
                    print(self.card[i], end=' ')
                print('| ', end='')

            if len(skippings[self.h(p)]) == 0:
                print('Пропусканий нет |', end=' ')
            else:
                print('Пропускания:', end=' ')
                for i in skippings[self.h(p)]:
                    print(self.card[i], end=' ')
                print('| ', end='')

        delta = p.k[0] - p.k[1] + f[self.h(p)]
        if self.mode == 'normal':
            print('Ожидаемое кол-во взяток у ', self.a, ': ', (self.K + delta) // 2, sep='', end=' | ')
            print('Ожидаемое кол-во взяток у ', self.b, ': ', (self.K - delta) // 2, sep='')
        else:
            w_sum = sum(self.weights)
            print('Ожидаемая сумма взяток у ', self.a, ': ', (w_sum + delta) // 2, sep='', end=' | ')
            print('Ожидаемая сумма взяток у ', self.b, ': ', (w_sum - delta) // 2, sep='')

    def Play(self, vector, first_player=0):
        for i in range(len(vector)):
            self.card.append(i + 1)

        p = Position(vector)
        p.curr_player = first_player

        self.PositionPreview(p, MIN_CONST)

        for i in range(self.K):
            if p.curr_player == 0:
                comp_mot = best_mot[self.h(p)]
                # print('Ход ', self.a, ': ', self.card[comp_mot], sep='', end='  ')
                # self.PrintAddInf(p)

                ip = InterPosition(p, comp_mot)
                # print('Ход ', self.b, ': ', sep='', end='')
                card_value = yield self.card[comp_mot]
                user_mot = self.card.index(card_value)
                bribe = self.weights[self.K - ip.size // 2]
                p = Position([], ip, user_mot, bribe)
                self.card.pop(max(comp_mot, user_mot))
                self.card.pop(min(comp_mot, user_mot))
            else:
                # print('Ход ', self.b, ': ', sep='', end='')
                card_value = yield None
                user_mot = self.card.index(card_value)
                ip = InterPosition(p, user_mot)
                comp_mot = best_mot[self.h(ip)]
                yield self.card[comp_mot]
                # print('Ход ', self.a, ': ', self.card[comp_mot], sep='', end='  ')
                # self.PrintAddInf(ip)

                bribe = self.weights[self.K - ip.size // 2]
                p = Position([], ip, comp_mot, bribe)
                self.card.pop(max(comp_mot, user_mot))
                self.card.pop(min(comp_mot, user_mot))

        if self.greater(p.k[0], p.k[1]):
            # print(self.a, 'Победил!')
            pass
        elif p.k[0] == p.k[1]:
            # print('НИЧЬЯ')
            pass
        else:
            # print(self.b, 'Победил!')
            pass

    def print_cards(self, vector):
        kit0 = []
        kit1 = []
        for i in range(len(vector)):
            card = i + 1
            if (vector[i] + self.a) % 2 == 0:
                kit0.append(card)
            else:
                kit1.append(card)
        print('Карты 0:', *kit0)
        print('Карты 1:', *kit1)
        print('')

    def read_vector(self, str):
        vector = []
        for c in str:
            if c == ' ':
                continue
            vector.append((int(c) + self.a) % 2)
        if len(vector) % 2 != 0:
            # print('MISTAKE!')
            return
        self.K = len(vector) // 2
        return vector

    def Game(self, lines): # считываем настройки из файла
        l = lines[1].split(' ')
        if l[2] != 'normal':
            self.change_type_to_tiny()
        l = lines[2].split(' ')
        self.b = int(l[2])  # игрок за которого играет user
        self.a = (self.b + 1) % 2  # игрок за которого играет комп
        l = lines[3].split(' ')
        first_player = (int(l[2]) + self.a) % 2

        vector = []
        l = lines[4].split()
        if len(l) > 2:
            vector = self.read_vector(lines[4][8:])
        else:
            l = lines[5].split()
            self.K = int(l[2])
            user_kit = set(map(int, lines[6][11:].split()))
            if (len(user_kit) != self.K):
                # print('MISTAKE!')
                return
            for i in range(2 * self.K):
                y = 0
                if (i + 1) in user_kit:
                    y = 1
                vector.append(y)
        # print('Двоичный вектор:', *[(y + self.a) % 2 for y in vector])

        l = lines[8].split(' ')
        if len(l) > 1:
            self.weights = list(map(int, lines[8][8:].split()))
            self.mode = 'weights'
        else:
            self.weights = [1] * self.K

        # self.print_cards(vector)
        return self.Play(vector, first_player)