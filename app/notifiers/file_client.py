"""Notify a user via file
"""
import structlog

from notifiers.utils import NotifierUtils


class FileNotifier(NotifierUtils):
    """Class for handling file notifications
    """

    def __init__(self):
        """Initialize StdoutNotifier class
        """

    def notify(self, message):
        """file send the message.

        Args:
            message (str): The message to print.
        """
        outF = open("files/alerts.json", "a")
        message += '\n'
        outF.write(message)
        outF.close()