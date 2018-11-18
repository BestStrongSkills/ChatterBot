"""
Filters set the base query that gets passed to the storage adapter.
"""


class Filter(object):
    """
    A base filter object from which all other
    filters should be subclassed.
    """

    def filter_selection(self, chatterbot, conversation):
        """
        Because this is the base filter class, this method just
        returns the storage adapter's base query. Other filters
        are expected to override this method.
        """
        return chatterbot.storage.base_query


def get_recent_repeated_responses(chatbot, conversation, sample=10, number=3):
    from collections import Counter

    # Get the most recent statements from the conversation
    conversation_statements = list(chatbot.storage.filter(
        conversation=conversation,
        order_by=['id']
    ))[sample * -1:]

    text_of_recent_responses = [
        statement.text for statement in conversation_statements
    ]

    counter = Counter(text_of_recent_responses)

    # Find the n most common responses from the conversation
    most_common = counter.most_common(number)

    return [text[0] for text in most_common]


class RepetitiveResponseFilter(Filter):
    """
    A filter that eliminates possibly repetitive responses to prevent
    a chat bot from repeating statements that it has recently said.
    """

    def filter_selection(self, chatterbot, conversation):
        from collections import Counter

        # Get the 10 most recent statements from the conversation
        conversation_statements = chatterbot.storage.filter(
            conversation=conversation,
            order_by=['id']
        )[-10:]

        text_of_recent_responses = [
            statement.in_response_to for statement in conversation_statements
            if statement is not None and statement.in_response_to is not None
        ]

        counter = Counter(text_of_recent_responses)

        # Find the two most common responses from the conversation
        most_common = counter.most_common(2)

        # Return the query with no changes if there are no statements to exclude
        if not most_common:
            return super().filter_selection(
                chatterbot,
                conversation
            )

        query = chatterbot.storage.base_query.statement_in_response_to_not_in(
            [text[0] for text in most_common]
        )

        return query
