from unittest import TestCase

from models.message_models import CreateMessageDto, Role


class TestCreateMessageDto(TestCase):
    def test_render(self):
        message = CreateMessageDto(
            role=Role.SYSTEM,
            content="Hello {{ name }}",
        )
        message.render(extra_data={"name": "John"})
        self.assertEqual(message.content, "Hello John")
