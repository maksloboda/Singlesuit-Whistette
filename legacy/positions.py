from auxiliary_functions import *

class Position:
    def __init__(self, vector=None, ip=None, mot=None, bribe=None):
        self.k = [0] * 2
        self.x = 0
        self.curr_player = 0
        self.table = -1
        if ip is None:
            self.size = len(vector)
            self.mask = create_mask(vector)
        else:
            self.size = ip.size - 2
            self.mask = move_mask(ip.mask, ip.size - ip.table - 1, ip.size - mot - 1)
            i = ip.curr_player
            j = (ip.curr_player + 1) % 2
            if mot > ip.table:
                self.curr_player = i
                self.x = bribe
                self.k[i] = ip.k[i] + bribe
                self.k[j] = ip.k[j]
            else:
                self.curr_player = j
                self.x = -bribe
                self.k[i] = ip.k[i]
                self.k[j] = ip.k[j] + bribe

            if (ip.curr_player == 1):
                self.x *= -1


class InterPosition:
    def __init__(self, p, mot):
        self.size = p.size
        self.mask = p.mask
        self.x = 0
        self.k = copy.copy(p.k)
        self.curr_player = (p.curr_player + 1) % 2
        self.table = mot
