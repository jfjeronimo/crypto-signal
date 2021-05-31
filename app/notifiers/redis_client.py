"""Notify Alerts via Redis-Stream
"""

import json

import structlog
from walrus import Database
from notifiers.utils import NotifierUtils


class RedisNotifier(NotifierUtils):
    """Used to notify alerts of signals via Redis.
    """

    def __init__(self, redis_server, redis_port, redis_db, stream):
        """Initialize redisNotifier class

        Args:
            redis_server (str): Redis erver Hostname / IP.
            redis_port   (int): Redis server port
            redis_db     (int): Redis server database number
            stream (str): Redis stream name.
        """
        self.redis_server = redis_server
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.stream = stream
        if self.redis_port is None:
            self.redis_port = "6379"
        if self.redis_db is None:
            self.redis_db = "0"

        self.logger = structlog.get_logger()
        self.connection = Database(host={}, port={}, db={}).format(self.redis_server, self.redis_port, self.redis_db)
        print(self.connection)
        self.channel = self.connection.Stream('{}').format(stream)

    def notify(self, message):
        """Send the notification.

        Args:
            message (str): The message to send.
        """

        max_message_size = 4096
        message_chunks = self.chunk_message(
            message=message, max_message_size=max_message_size)
        print(message_chunks)
        # exit()

        for message_chunk in message_chunks:
            self.channel.add(text=message_chunk)

    def send_messages(self, messages=[]):
        if len(messages) > 0:
            for message in messages:
                self.notify(message)
