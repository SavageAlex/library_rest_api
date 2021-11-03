from decouple import config

if config('DEBUG', cast=bool, default=True) == False:
    from .prod import *
else:
    from .dev import *