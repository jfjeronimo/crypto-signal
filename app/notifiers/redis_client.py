"""Notify Alerts via Redis-Stream
"""

import json

import structlog
from walrus import Database
from notifiers.utils import NotifierUtils


class RedisNotifier(NotifierUtils):
    """Used to notify alerts of signals via Redis.
    """

    def __init__(self, redis_server, redis_port, stream):
        """Initialize redisNotifier class

        Args:
            redis_server (str): Redis erver Hostname / IP.
            redis_port   (int): Redis server port
            redis_db     (int): Redis server database number
            stream (str): Redis stream name.
        """
        self.redis_server = redis_server
        self.redis_port = redis_port
        self.stream = stream
        if self.redis_port is None:
            self.redis_port = "6379"

        self.logger = structlog.get_logger()
        self.connection = Database(host=self.redis_server, port=self.redis_port)
        print(self.connection)
        self.channel = self.connection.Stream(self.stream)

    def notify(self, message):
        """Send the notification.

        Args:
            message (str): The message to send.
        """

        self.channel.add({'signal': message})

    def send_messages(self, messages=[]):
        if len(messages) > 0:
            for message in messages:
                self.notify(message)
