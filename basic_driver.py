import legacy.deep_green
from typing import List, Generator

INIT_FORMAT = \
"""
type = normal
user = 0
first_player = {first_player}
vector =
k = {size}
user_cards: {user_cards}

weights:
"""

EMPTY_FIELD = -1

class BasicDriver:
  """
  Handles legacy solver with a reasonable api
  """
  user_cards: List[int]
  is_user_turn: bool
  legacy_solver: Generator
  computer_move: int
  field: int
  is_finished: bool

  def __init__(self, user_cards_: List[int], is_user_first_: bool) -> None:
    self.user_cards = user_cards_
    self.is_user_turn = is_user_first_
    config = INIT_FORMAT.format(
      first_player = 0 if is_user_first_ else 1,
      size = len(user_cards_),
      user_cards = " ".join(
        map(str, user_cards_)
      )
    )
    dg = legacy.deep_green.DeepGreen()
    self.legacy_solver = dg.Game(config.split("\n"))
    self.computer_move = next(self.legacy_solver) 
    self.field = EMPTY_FIELD
    self.is_finished = False

  def move_by_player(self, card):
    assert(self.is_user_turn)
    try:
      self.computer_move = self.legacy_solver.send(card)
      assert(card in self.user_cards)
      self.user_cards.remove(card)
      if self.field == EMPTY_FIELD:
        self.field = card
        self.is_user_turn = False
      elif self.field > card:
        self.field = EMPTY_FIELD
        self.is_user_turn = False
      else:
        self.field = EMPTY_FIELD
        self.is_user_turn = True
    except StopIteration:
      self.is_finished = True
  
  def move_by_computer(self) -> int:
    assert(not self.is_user_turn)
    card = self.computer_move
    try:
      self.computer_move = next(self.legacy_solver)
      if card is None:
        card = self.computer_move
      assert(card not in self.user_cards)
      if self.field == EMPTY_FIELD:
        self.field = card
        self.is_user_turn = True
      elif self.field > card:
        self.field = EMPTY_FIELD
        self.is_user_turn = True
      else:
        self.field = EMPTY_FIELD
        self.is_user_turn = False
    except StopIteration:
      self.is_finished = True
    return card

  def is_end(self) -> bool:
    return self.is_finished

