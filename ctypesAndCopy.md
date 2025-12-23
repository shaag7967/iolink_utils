# ctypes (OctetDecoderBase) and copy semantics

This python package uses `ctypes.Structure` to decode and encode bytes (see `octetDecoder.py`). This is fast and 
creates readable code.
The drawback is, that these objects are not ints (e.g.) and are always assigned by reference and therefore work on 
the same memory. In most cases you don't want that - you want to have a deep copy.

If you have an OctetDecoder like this:
```python
class MyOctetDecoder(OctetDecoderBase):
    _fields_ = [
        ("one", ctypes.c_uint8, 4),
        ("two", ctypes.c_uint8, 4)
    ]
```

**WRONG: don't do this:**
```python
class MyClass:
    def __init__(self, decoder: MyOctetDecoder):
        self.decoder: MyOctetDecoder = decoder  # reference - no deepcopy
```

> If you change your passed variable (outside your class), your member variable (inside your class) will also change!

**CORRECT: do this instead:**
```python
class MyClass:
    def __init__(self, decoder: MyOctetDecoder):
        self.decoder: MyOctetDecoder = decoder.copy()  # OctetDecoderBase implements a copy() function for you
```

or this:
```python
class MyClass:
    def __init__(self, decoder: MyOctetDecoder):
        self.decoder: MyOctetDecoder = MyOctetDecoder(int(decoder))  # convert to int and create a new object with it
```

> Some classes also provide a `__deepcopy__` implementation (like Event and EventMemory).
