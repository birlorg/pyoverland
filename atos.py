import asyncio
import atexit
import threading
"""
Stolen from https://github.com/xloem/async_to_sync
sync_result = sync.coroutine(async_object.method())

import atos as sync

# an async object method to demonstrate use
class async_class:
        async def method(self):
                    return True
                async_object = async_class()

                # wrap all async methods of an object
                sync_object = sync.methods(async_object)

                assert sync_object.method() is True

                # wrap a single async callable
                sync_function = sync.function(async_object.method)

                assert sync_function() is True

                # wait for a coroutine
                sync_result = sync.coroutine(async_object.method())

                assert sync_result is True

                # manually stop default event loop
                sync.stop()

                # manually start default event loop
                sync.start()
"""

_loop = None
_thread = None

def get_default_event_loop():
    global _loop, _thread
    if _thread is None:
        if _loop is None:
            _loop = asyncio.get_event_loop()
        if not _loop.is_running():
            _thread = threading.Thread(
                target=_loop.run_forever,
                daemon=True)
            _thread.start()
    return _loop

def set_default_event_loop(loop):
    stop()
    _loop = loop

def start():
    get_default_event_loop()

@atexit.register
def stop():
    global _loop, _thread
    if _loop is not None:
        _loop.call_soon_threadsafe(_loop.stop)
    if _thread is not None:
        _thread.join()
        _thread = None

def coroutine(coroutine, loop = None):
    if loop is None:
        loop = get_default_event_loop()
    future = asyncio.run_coroutine_threadsafe(coroutine, loop)
    result = future.result()
    return result

def function(function, loop = None):
    def call(*params, **kwparams):
        async_coroutine = function(*params, **kwparams)
        return coroutine(async_coroutine, loop)
    return call

class methods:
    def __init__(self, object, loop = None):
        self.__object = object
        self.__loop = loop
    def __getattr__(self, name):
        result = getattr(self.__object, name)
        if asyncio.iscoroutinefunction(result):
            return function(result, self.__loop)
        else:
            return result
