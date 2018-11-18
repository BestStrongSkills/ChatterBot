from tests.base_case import ChatBotMongoTestCase


class RepetitiveResponseFilterTestCase(ChatBotMongoTestCase):
    """
    Test case for the RepetitiveResponseFilter class.
    """

    def test_filter_selection(self):
        """
        Test that repetitive responses are filtered out of the results.
        """
        from chatterbot.conversation import Statement
        from chatterbot.filters import RepetitiveResponseFilter
        from chatterbot.trainers import ListTrainer

        self.chatbot.filters = (RepetitiveResponseFilter(), )

        self.trainer = ListTrainer(
            self.chatbot,
            show_training_progress=False
        )

        self.trainer.train([
            'Hello',
            'Hi',
            'Hello',
            'Hi',
            'Hello',
            'How are you?',
            'I am good',
            'Glad to hear',
            'Thank you',
            'I am good',
            'Glad to hear',
        ])

        statement = Statement(text='Hello', conversation='training')
        first_response = self.chatbot.get_response(statement)
        second_response = self.chatbot.get_response(statement)

        self.assertEqual('How are you?', first_response.text)
        self.assertEqual('Hi', second_response.text)
