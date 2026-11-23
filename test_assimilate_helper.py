"""
Unit tests for assimilate_helper module.
Validates detection and playful response handling for whimsical/consumption queries.
"""

import unittest
from assimilate_helper import is_consumption_query, handle_prompt, DEFAULT_HUMOROUS_RESPONSE


class TestAssimilateHelper(unittest.TestCase):
    """Test suite for Whimsical Prompt Handling and Consumption Safety."""

    def test_is_consumption_query_positive(self):
        """Test that whimsical ingestion/consumption queries are identified correctly."""
        consumption_prompts = [
            "hello can i eat you?",
            "Can I eat you right now?",
            "Can I consume you?",
            "are you edible?",
            "I want to devour this program",
            "Can I bite you?",
            "Will you digest me?",
        ]
        for prompt in consumption_prompts:
            with self.subTest(prompt=prompt):
                self.assertTrue(
                    is_consumption_query(prompt),
                    f"Failed to identify consumption query: '{prompt}'"
                )

    def test_is_consumption_query_negative(self):
        """Test that standard operational queries are not falsely identified as consumption."""
        standard_prompts = [
            "Hello, how are you today?",
            "What features does Assimilate Automation offer?",
            "Can you help me generate a report?",
            "Create a new database workflow.",
            "",
        ]
        for prompt in standard_prompts:
            with self.subTest(prompt=prompt):
                self.assertFalse(
                    is_consumption_query(prompt),
                    f"Falsely identified standard query as consumption: '{prompt}'"
                )

    def test_handle_prompt_whimsical(self):
        """Test prompt handling for a whimsical consumption prompt."""
        prompt = "hello can i eat you?"
        result = handle_prompt(prompt)

        self.assertEqual(result["prompt"], prompt)
        self.assertEqual(result["category"], "whimsical_consumption")
        self.assertTrue(result["is_whimsical"])
        self.assertEqual(result["response"], DEFAULT_HUMOROUS_RESPONSE)

    def test_handle_prompt_standard(self):
        """Test prompt handling for a standard prompt."""
        prompt = "Explain automated workflows."
        result = handle_prompt(prompt)

        self.assertEqual(result["prompt"], prompt)
        self.assertEqual(result["category"], "standard")
        self.assertFalse(result["is_whimsical"])
        self.assertIn("Processed input:", result["response"])

    def test_handle_prompt_invalid_input(self):
        """Test handling of non-string inputs."""
        result = handle_prompt(12345)  # type: ignore
        self.assertEqual(result["category"], "invalid")
        self.assertFalse(result["is_whimsical"])
        self.assertIn("Invalid prompt format", result["response"])


if __name__ == "__main__":
    unittest.main()
