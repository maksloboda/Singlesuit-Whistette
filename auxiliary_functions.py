import copy
import time

pow2 = [0] * 51
pow2[0] = 1
for i in range(1, 51):
    pow2[i] = pow2[i - 1] * 2


def create_mask(vector):
    mask = 0
    for i in range(len(vector)):
        mask = mask * 2 + vector[i]
    return mask


def move_mask(mask, i, j):
    if (j > i):
        i, j = j, i
    mask = (mask // (pow2[i + 1])) * pow2[i] + (mask % pow2[i])
    return (mask // (pow2[j + 1])) * pow2[j] + (mask % pow2[j])


def make_vector(mask):
    vector = []
    while (mask > 0):
        vector.append(mask % 2)
        mask //= 2
    vector.reverse()
    return vector


def pl(mask, i):
    return (mask // pow2[i]) % 2