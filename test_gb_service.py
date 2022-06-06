import pytest
import redis

@pytest.fixture
def empty_redis():
    r = redis.Redis(host='localhost', port=6379)
    yield r
    r.delete('key')

def test_gb_push(empty_redis):
    empty_redis.rpush('key', 'q1', 'q2')
    values = [v.decode('utf-8') for v in empty_redis.lrange('key', 0, -1)]

    assert values == ['q1', 'q2']

def test_gb_list(empty_redis):
    assert True
    

