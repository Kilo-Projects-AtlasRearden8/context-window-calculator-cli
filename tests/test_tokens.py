import unittest

from context_calc.tokens import context_fit, estimate_tokens


class TestEstimateTokens(unittest.TestCase):
    def test_empty_text(self):
        self.assertEqual(estimate_tokens(""), 0)
        self.assertEqual(estimate_tokens(None), 0)

    def test_char_method_basic(self):
        self.assertEqual(estimate_tokens("test", chars_per_token=4), 1)
        self.assertEqual(estimate_tokens("abcd", chars_per_token=4), 1)
        self.assertEqual(estimate_tokens("abcde", chars_per_token=4), 2)

    def test_char_method_rounds_up(self):
        self.assertEqual(estimate_tokens("a" * 100, chars_per_token=4), 25)

    def test_word_method_basic(self):
        self.assertEqual(estimate_tokens("one two three", method="word", words_per_token=1.0), 3)

    def test_word_method_rounds_up(self):
        self.assertEqual(estimate_tokens("one two three four", method="word", words_per_token=2.0), 2)

    def test_custom_chars_per_token(self):
        self.assertEqual(estimate_tokens("abcdef", chars_per_token=2), 3)

    def test_unknown_method_raises(self):
        with self.assertRaises(ValueError):
            estimate_tokens("hello", method="bogus")

    def test_minimum_one_token_for_nonempty(self):
        self.assertEqual(estimate_tokens("x", chars_per_token=100), 1)
        self.assertEqual(estimate_tokens("x", method="word", words_per_token=100.0), 1)


class TestContextFit(unittest.TestCase):
    def test_fits_with_room(self):
        result = context_fit(100, 1000, reserve_completion=100)
        self.assertTrue(result["fits_within_context"])
        self.assertEqual(result["available_for_prompt"], 900)
        self.assertEqual(result["remaining_tokens"], 800)

    def test_exact_fit(self):
        result = context_fit(900, 1000, reserve_completion=100)
        self.assertTrue(result["fits_within_context"])
        self.assertEqual(result["remaining_tokens"], 0)

    def test_does_not_fit(self):
        result = context_fit(901, 1000, reserve_completion=100)
        self.assertFalse(result["fits_within_context"])
        self.assertEqual(result["remaining_tokens"], -1)

    def test_percent_of_context(self):
        result = context_fit(500, 1000)
        self.assertEqual(result["percent_of_context"], 50.0)

    def test_zero_context_window(self):
        result = context_fit(10, 0)
        self.assertEqual(result["percent_of_context"], 0.0)
        self.assertFalse(result["fits_within_context"])

    def test_no_reserve(self):
        result = context_fit(100, 1000)
        self.assertEqual(result["available_for_prompt"], 1000)


if __name__ == "__main__":
    unittest.main()
