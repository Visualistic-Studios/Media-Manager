
# Reading Encrypted Data

Sometimes you might need to read post data directly from Python. I did while debugging, so i'm posting it here!


```py
>>> from resources.crypt import get_fernet, get_key, decrypt
>>> fernet = get_fernet(get_key("KEYLOCHERE"))
>>> stuff = decrypt(fernet, b"ENCRYPTEDDATAHERE")
```