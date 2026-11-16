import unittest
import tkinter as tk
from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = Calculator(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_initial_state(self):
        self.assertEqual(self.app.equation, "")
        self.assertEqual(self.app.display_var.get(), "")

    def test_number_input(self):
        self.app.on_button_click('7')
        self.app.on_button_click('+')
        self.app.on_button_click('3')
        self.assertEqual(self.app.equation, "7+3")
        self.assertEqual(self.app.display_var.get(), "7+3")

    def test_calculation(self):
        self.app.on_button_click('5')
        self.app.on_button_click('*')
        self.app.on_button_click('4')
        self.app.on_button_click('=')
        self.assertEqual(self.app.equation, "20")
        self.assertEqual(self.app.display_var.get(), "20")

    def test_clear(self):
        self.app.on_button_click('9')
        self.app.on_button_click('C')
        self.assertEqual(self.app.equation, "")
        self.assertEqual(self.app.display_var.get(), "")

if __name__ == '__main__':
    unittest.main()
