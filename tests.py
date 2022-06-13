import unittest
from legacy.deep_green import DeepGreen

class TestLegacySolverSimple(unittest.TestCase):

  def test_simple_game_1(self):
    dg = DeepGreen()
    game = dg.Game("""mode = Comp_vs_User
type = normal
user = 0
first_player = 0
vector =
k = 1
user_cards: 2

weights:
      """.split("\n")
    )
    self.assertEqual(next(game), None)
    self.assertEqual(game.send(2), 1)
    with self.assertRaises(StopIteration):
      next(game)
  
  def test_simple_game_2(self):
    dg = DeepGreen()
    game = dg.Game("""mode = Comp_vs_User
type = normal
user = 0
first_player = 0
vector =
k = 2
user_cards: 2 4

weights:
      """.split("\n")
    )
    self.assertEqual(next(game), None)
    self.assertEqual(game.send(2), 3)
    self.assertEqual(next(game), 1)
    with self.assertRaises(StopIteration):
      game.send(4)

if __name__ == "__main__":
  unittest.main()