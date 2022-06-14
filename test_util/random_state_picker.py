import random
from typing import List, Tuple

def generate_random_state(allowed_sizes: List[int]) -> Tuple[List[int], List[int], int]:
  """
  Get a list of allowed game lengths and returns a random state
  Tuple[A cards, B cards, first player index]
  """
  size = random.choice(allowed_sizes)
  cards = list(range(1, size * 2 + 1))

  first_cards = random.sample(cards, k = size)
  second_cards = list(set(cards).difference(set(first_cards)))
  first_player = random.randrange(0, 2)

  return first_cards, second_cards, first_player