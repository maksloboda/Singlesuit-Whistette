import random
import unittest
from basic_driver import BasicDriver
from test_util.random_state_picker import generate_random_state
from solver import find_optimal_move, GameState

repeats = 10000

class TestLegacySolverSimple(unittest.TestCase):

  def test_simple_game_1(self):
    bd = BasicDriver([2], True)
    self.assertEqual(bd.move_by_player(2), None)
    self.assertEqual(bd.move_by_computer(), 1)
    self.assertTrue(bd.is_end())
  
  def test_simple_game_2(self):
    bd = BasicDriver([1], False)
    self.assertEqual(bd.move_by_computer(), 2)
    self.assertEqual(bd.move_by_player(1), None)
    self.assertTrue(bd.is_end())

class TestSolverStress(unittest.TestCase):
  def test_compvcomp(self):
    for _ in range(repeats):
      first_cards, second_cards, first_player = generate_random_state([1, 2, 3, 4])
      bd1 = BasicDriver(first_cards, first_player == 0)
      bd2 = BasicDriver(second_cards, first_player == 1)
      while not bd1.is_end() and not bd2.is_end():
        self.assertNotEqual(bd1.can_move_by_player(), bd2.can_move_by_player())
        computer, user = bd1, bd2
        first_player = 1
        if bd1.can_move_by_player():
          computer, user = bd2, bd1
          first_player = 0
        predicted_card = find_optimal_move(
          GameState(
            bd1.user_cards,
            bd2.user_cards,
            first_player,
            computer.field,
          )
        )
        card = computer.move_by_computer()
        self.assertEqual(card, predicted_card)
        user.move_by_player(card)
      self.assertEqual(bd1.is_end(), bd2.is_end())


if __name__ == "__main__":
  unittest.main()