"""
Unit tests for the AI Water Monitor Module (ai_water_monitor.py).
"""

import unittest
from ai_water_monitor import AIWaterMonitor, report_ai_water_footprint

class TestAIWaterMonitor(unittest.TestCase):
    """Test suite for AIWaterMonitor."""

    def test_init(self):
        monitor = AIWaterMonitor("TestModel")
        self.assertEqual(monitor.model_name, "TestModel")
        self.assertEqual(monitor.total_queries, 0)
        self.assertEqual(monitor.total_tokens_processed, 0)
        self.assertEqual(monitor.total_water_consumed_ml, 0.0)

    def test_estimate_inference_water(self):
        monitor = AIWaterMonitor("Llama-3")
        res = monitor.estimate_inference_water(100, 0.5)
        self.assertEqual(res["model_name"], "Llama-3")
        self.assertEqual(res["tokens_processed"], 100)
        self.assertEqual(res["water_consumed_ml"], 50.0)
        self.assertEqual(res["water_consumed_liters"], 0.05)
        self.assertEqual(res["total_cumulative_water_ml"], 50.0)
        self.assertEqual(monitor.total_queries, 1)
        self.assertEqual(monitor.total_tokens_processed, 100)

        # Test negative tokens
        res_neg = monitor.estimate_inference_water(-50, 0.5)
        self.assertEqual(res_neg["tokens_processed"], 0)
        self.assertEqual(res_neg["water_consumed_ml"], 0.0)

    def test_get_statistics(self):
        monitor = AIWaterMonitor("GPT-4")
        monitor.estimate_inference_water(200, 1.0)
        stats = monitor.get_statistics()
        self.assertEqual(stats["model_name"], "GPT-4")
        self.assertEqual(stats["total_queries"], 1)
        self.assertEqual(stats["total_tokens_processed"], 200)
        self.assertEqual(stats["total_water_consumed_ml"], 200.0)

    def test_report_ai_water_footprint(self):
        rep = report_ai_water_footprint("Claude", 150)
        self.assertEqual(rep["model_name"], "Claude")
        self.assertEqual(rep["tokens_processed"], 150)
        self.assertIn("water_consumed_ml", rep)

if __name__ == "__main__":
    unittest.main()


    #kjhfjasaskbfbassfbkajsfhkjfjkjjabssfkbkdbff
