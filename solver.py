from typing import List, Tuple, Any
from basic_driver import EMPTY_FIELD, BasicDriver
import itertools

class GameState:
  first_player_set: List[int]
  second_player_set: List[int]
  current_player: int
  field: int
  weights: List[int]
  version: str

  def __init__(self,
      first_player_set_: List[int],
      second_player_set_: List[int],
      current_player_ : int,
      field_: int,
      weights_: List[int] = [],
      version_: str = "normal"):
    self.first_player_set = first_player_set_
    self.second_player_set = second_player_set_
    self.current_player = current_player_
    self.field = field_
    self.weights = weights_
    self.version = version_

def prepare_legacy_solver(state: GameState) -> Tuple[Any, List[int]]:
  """
  Returns a solver that is in the provided state and a sorted list of cards
  """
  other_player = 1 - state.current_player
  extra_card = [(state.field, other_player)] if state.field is not EMPTY_FIELD else []
  # An array of (card_number, owner)
  card_info = list(
      sorted(
          itertools.chain(
              zip(state.first_player_set, [0] * len(state.first_player_set)),
              zip(state.second_player_set, [1] * len(state.second_player_set)),
              extra_card
          )
      )
  )

  card_owners = list(map(lambda x: x[1], card_info))
  # An array of (card_number, owner) but cards are renamed
  new_card_info = list(
    map(
      lambda x: (x[0] + 1, x[1]),
      enumerate(card_owners)
    )
  )

  solver = BasicDriver(
    list(
      map(
        lambda x: x[0],
        filter(
          lambda x: x[1] == other_player,
          new_card_info
        )
      )
    ),
    extra_card != [],
    state.weights,
    state.version
  )

  if extra_card:
    # make the fake move
    card_index = card_info.index(extra_card[0])
    assert(card_index != -1)
    solver.move_by_player(card_index + 1)

  card_names = list(map(lambda x: x[0], card_info))

  return (solver, card_names)

def find_optimal_move(state: GameState):
  solver, card_names = prepare_legacy_solver(state)
  idx = solver.move_by_computer()
  return card_names[idx - 1]
