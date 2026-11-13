# timberline-cache

This repository contains the implementation of `timberline-cache`, a tiered
in-process cache with size-aware eviction for Python services.

## Status

Released. Version 2.x is maintained by the Timberline Labs team and is
published to the internal package index.

## Example

```python
from timberline import TieredCache
cache = TieredCache(hot_size=2048, warm_size=16384)
cache.set('customer:42', payload)
```
