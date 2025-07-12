# Redis Basic Tasks – ALX Backend Storage

## Project Overview
This project demonstrates the use of Redis in Python to manage caching, data storage, method call tracking, and a simple expiring web cache. It focuses on decorators, type handling, and Redis operations.

## Directory
`0x02-redis_basic/`

## Technologies Used
- Python 3
- Redis
- `redis-py`
- Ubuntu 18.04 (with WSL/Windows integration)

## Key Features

### `exercise.py`
- **Cache Class**
  - `store(data)`: Stores data using a UUID key
  - `get(key, fn=None)`: Retrieves and converts stored data
  - `get_str(key)`: Returns data as UTF-8 string
  - `get_int(key)`: Returns data as integer

- **Decorators**
  - `count_calls`: Tracks how many times `store()` is called
  - `call_history`: Logs input/output of each `store()` call

- **Replay Function**
  - `replay(fn)`: Prints method call history from Redis logs

### `web.py`
- **get_page(url)**
  - Fetches and caches HTML content for a given URL
  - Tracks how often a URL is accessed using Redis counters
  - Cache expires after 10 seconds using `setex`

## Testing
Use `main.py` to validate functionality for each task:
```bash
python3 main.py
```

## Setup and Configuration
```
sudo apt-get -y install redis-server
pip3 install redis requests
sudo sed -i "s/bind .*/bind 127.0.0.1/g" /etc/redis/redis.conf
service redis-server start

```