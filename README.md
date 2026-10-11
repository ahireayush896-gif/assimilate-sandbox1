# assimilate-sandbox1

## Health Check

The repository includes a `health_check.py` script that provides a `ping()` function to verify system status.

### Usage

```python
from health_check import ping

status = ping()
print(status)  # {'status': 'ok'}
```

You can also execute the script directly:

```bash
python health_check.py
```
