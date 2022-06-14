import unittest
from legacy.deep_green import DeepGreen
from basic_driver import BasicDriver

class TestLegacySolverSimple(unittest.TestCase):

  def test_simple_game_1(self):
    bd = BasicDriver([2], True)
    self.assertEqual(bd.move_by_player(2), None)
    self.assertEqual(bd.move_by_computer(), 1)
    self.assertTrue(bd.is_end(), True)

    bd = BasicDriver([1], False)
    self.assertEqual(bd.move_by_computer(), 2)
    self.assertEqual(bd.move_by_player(1), None)
    self.assertTrue(bd.is_end(), True)
  
#   def test_simple_game_2(self):
#     dg = DeepGreen()
#     game = dg.Game("""mode = Comp_vs_User
# type = normal
# user = 0
# first_player = 0
# vector =
# k = 2
# user_cards: 2 4

# weights:
#       """.split("\n")
#     )
#     self.assertEqual(next(game), None)
#     self.assertEqual(game.send(2), 3)
#     self.assertEqual(next(game), 1)
#     with self.assertRaises(StopIteration):
#       game.send(4)

if __name__ == "__main__":
  unittest.main()