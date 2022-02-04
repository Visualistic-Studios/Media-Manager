## Reading Encrypted Streams


**Return Output**
```py
from io import BytesIO
from resources.crypt import decrypt_stream

result = None
with BytesIO() as output_stream:
    decrypt_stream(input_stream, output_stream)
    result = output_stream.getvalue()
```


**Export Output**

```py
from resources.crypt import decrypt_stream
input_stream="file/location/name.filetype"
output_stream="file/location/name.filetype"
decrypt_stream(input_stream, output_stream)
```
