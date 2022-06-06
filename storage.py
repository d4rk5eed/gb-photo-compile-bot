import redis
import sys
import logging

this = sys.modules[__name__]
this.__REDIS__ = None

def init():
    logging.info('Initializing Redis')
    this.__REDIS__ = redis.Redis(host='localhost', port=6379)

def push_value(user_id, file_name):
    user_id = str(user_id)
    logging.info(f"Pushing values\nuser_id: {user_id}, file_name: {file_name}")
    this.__REDIS__.rpush(user_id, file_name)

def list_values(user_id):
    user_id = str(user_id)
    logging.info(f"Listing values\nuser_id: {user_id}")
    return [v.decode('utf-8') for v in this.__REDIS__.lrange(user_id, 0, -1)]

def del_values(user_id):
    user_id = str(user_id)
    logging.info(f"Deleting values\nuser_id:{user_id}")
    this.__REDIS__.delete(user_id)
