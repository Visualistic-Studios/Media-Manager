
# Reading Encrypted Data

Sometimes you might need to read post data directly from Python. I did while debugging, so i'm posting it here!


```py
from resources.crypt import Crypt, Key
from resources.config import settings_core
settings = settings_core()
key = Key(settings.key_location)
crypt = Crypt(key, settings.block_size)

stuff = crypt.decrypt(b"Stuff here")
```
