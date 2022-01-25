
# Reading Encrypted Settings

If you ever find yourself in need of reading the encrypted settings, open up `Python` in the apps main directory

```py
# Import settings & create settings object
>>> import resources.config
>>> from resources.config import settings_core
>>> settings = settings_core()
# Read encrypted setting
>>> decrypted_setting = settings.read_encrypted_setting("CATEGORY","SETTING")
>>> print(decrypted_setting)
```