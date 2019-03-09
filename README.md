# hueSignal
A decorator that would change Phillips Hue color lights depending on the success or failure of a function.

At this stage the decorator assumes that you have a Phillips Hue bulb. 
The light will turn green if the code run and will turn red if it encountered an exception. 

Usage:

```python
from hueSignal import hueSignal
import time 

@hueSignal
def testing_function(success=True):
    i = 5
    while i >= 0:
        print(i, end="\r")
        time.sleep(1)
        i -= 1
    if success:
        return
    else:
        raise Exception("POTATO")

# Will turn the light green
testing_function(success=True)

# Will turn the light red
testing_function(success=False) 

```

TODO: 
- Clean code.
- Add lights and color options.
- Write the docs.
- Package