from .common import *

DEBUG = True if os.environ.get('DEBUG', 'false').lower() in ['true', 1,
                                                             True, '1', 'True'
                                                             ] else False

if DEBUG:
    from .dev import *
else:
    from .prod import *

