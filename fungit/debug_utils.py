import time
import logging

LOG = logging.getLogger(__name__)


def timeit_decorator(func):
    def timed(*args, **kw):
        ts = time.time()
        out = func(*args, **kw)
        LOG.debug(f"{func.__name__} completed in {time.time() - ts:.6f} seconds")
        return out

    return timed
