### Setting Up Redis


For Windows:
1. Download Redis for Windows from Memurai (https://www.memurai.com/) or Redis for Windows GitHub Releases (https://github.com/microsoftarchive/redis/releases).
2. Install and start Redis:
Run redis-server.exe from the installation directory.
3. Verify Redis is running:
redis-cli ping
Expected response:
PONG
   
4. Configure Redis in Django

In the Django settings.py file, Redis is configured as the default cache backend:
```py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',  # Redis database index 1
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'TIMEOUT': 300,  # Cache timeout in seconds
    }
}
```
If you are using a cloud-based Redis (e.g., Heroku Redis), replace 127.0.0.1:6379/1 with the provided Redis URL:
LOCATION = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1')

## Testing Redis Integration

Using Django Shell:
1. Open the Django shell:
python manage.py shell
2. Run the following commands to test caching:
from django.core.cache import cache

### Set a value in Redis
cache.set('test_key', 'test_value', timeout=300)

### Retrieve the value from Redis
print(cache.get('test_key'))  # Expected output: 'test_value'

3. Verify the key in Redis:
redis-cli KEYS *

Testing API Endpoints:
- List Categories: GET /api/categories/
- List Products with Filters: GET /api/products/?category=Electronics&price_min=100&price_max=500

### Troubleshooting
Redis not running: \
Ensure Redis is running (redis-server or Docker container).
Verify connectivity with redis-cli ping.

Keys not appearing in Redis:\
Ensure cache.set() is used correctly in views.\
Check if Redis is properly configured in settings.py.

