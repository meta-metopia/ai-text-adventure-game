from unittest import TestCase

from utils.get_selections import get_selections


class TestGetSelection(TestCase):
    def test_get_selections(self):
        message = """
        some text content
        ---selections---
        1. selection 1
        2. selection 2
        ---end selections---
        """
        game = get_selections(message)
        self.assertEqual(game.message.strip(), "some text content")
        self.assertEqual(game.selections, ["1. selection 1", "2. selection 2"])

    def test_get_selections_with_no_selections(self):
        message = """
        some text content
        """
        game = get_selections(message)
        self.assertEqual(game.message.strip(), "some text content")
        self.assertEqual(game.selections, [])

    def test_get_selections_with_no_selections_and_no_message(self):
        message = """
        """
        game = get_selections(message)
        self.assertEqual(game.message.strip(), "")
        self.assertEqual(game.selections, [])

    def test_get_selections_without_ending_selections(self):
        message = """
        some text content
        ---selections---
        1. selection 1
        2. selection 2
        """
        game = get_selections(message)
        self.assertEqual(game.message.strip(), "some text content")
        self.assertEqual(game.selections, ["1. selection 1", "2. selection 2"])
