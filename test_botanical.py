import unittest
from botanical_identity import Apple, Banana, AppleBananaSimulation, botanical_conflict_demo, play_music

class TestAppleEatingBanana(unittest.TestCase):
    def test_botanical_conflict_demo(self):
        self.assertEqual(botanical_conflict_demo(), "FORCED_CONFLICT_FROM_AYUSH")

    def test_play_music(self):
        # Just ensure it runs without error
        play_music()

    def test_banana_initialization(self):
        b = Banana(x=5.0, y=10.0, energy_value=30)
        self.assertEqual(b.x, 5.0)
        self.assertEqual(b.y, 10.0)
        self.assertEqual(b.energy_value, 30)
        self.assertFalse(b.is_eaten)

    def test_apple_initialization(self):
        apple = Apple(x=0.0, y=0.0, energy=100)
        self.assertEqual(apple.x, 0.0)
        self.assertEqual(apple.y, 0.0)
        self.assertEqual(apple.energy, 100)
        self.assertEqual(apple.bananas_eaten_count, 0)

    def test_apple_movement(self):
        apple = Apple(x=0.0, y=0.0)
        apple.move_towards(3.0, 4.0, step=5.0)
        self.assertAlmostEqual(apple.x, 3.0)
        self.assertAlmostEqual(apple.y, 4.0)

    def test_apple_eats_banana(self):
        apple = Apple(x=1.0, y=1.0, energy=100)
        banana = Banana(x=1.0, y=1.0, energy_value=50)
        
        success = apple.eat(banana)
        self.assertTrue(success)
        self.assertTrue(banana.is_eaten)
        self.assertEqual(apple.energy, 150)
        self.assertEqual(apple.bananas_eaten_count, 1)

        # Eating already eaten banana should fail
        success_again = apple.eat(banana)
        self.assertFalse(success_again)
        self.assertEqual(apple.energy, 150)

    def test_simulation_run(self):
        sim = AppleBananaSimulation(width=10, height=10)
        eaten_count = sim.run(max_steps=100)
        self.assertEqual(eaten_count, 5)
        self.assertTrue(all(b.is_eaten for b in sim.bananas))

if __name__ == '__main__':
    unittest.main()
