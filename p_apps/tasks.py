from __future__ import absolute_import, unicode_literals
from .celery import app
import urllib.request

@app.task
def add(x, y):
    # print("adding {} and {} together".format(x,y))
    return x + y

@app.task
def fib(n):
    if n <= 1: return n
    return fib(n-2) + fib(n-1)

@app.task
def make_self_request():
    url = "https://boiling-headland-86603.herokuapp.com/"
    contents = urllib.request.urlopen(url)
    contents.readlines()