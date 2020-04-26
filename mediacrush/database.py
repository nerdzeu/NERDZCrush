import redis

from .config import _cfg, _cfgi

PREFIX = "mediacrush."
r = redis.StrictRedis(_cfg("redis-ip"), _cfgi("redis-port"), decode_responses=True)

_k = lambda x: "{}{}".format(PREFIX, x)
