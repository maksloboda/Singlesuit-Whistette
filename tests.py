import unittest
from legacy.deep_green import DeepGreen
from basic_driver import BasicDriver

class TestLegacySolverSimple(unittest.TestCase):

  def test_simple_game_1(self):
    bd = BasicDriver([2], True)
    self.assertEqual(bd.move_by_player(2), None)
    self.assertEqual(bd.move_by_computer(), 1)
    self.assertTrue(bd.is_end(), True)
  
  def test_simple_game_2(self):
    bd = BasicDriver([1], False)
    self.assertEqual(bd.move_by_computer(), 2)
    self.assertEqual(bd.move_by_player(1), None)
    self.assertTrue(bd.is_end(), True)    

if __name__ == "__main__":
  unittest.main()