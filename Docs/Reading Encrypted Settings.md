
# Reading Encrypted Settings

If you ever find yourself in need of reading the encrypted settings, open up `Python` in the apps main directory

```py
# Import settings & create settings object
from resources.config import settings_core
settings = settings_core()
# Read encrypted setting. Category not required but faster. 
decrypted_setting = settings.get_setting_value(category="CATEGORY", setting="SETTING_ID)
print(decrypted_setting)
```
