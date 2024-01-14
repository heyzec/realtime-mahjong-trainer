# script.py
# Taken from https://github.com/jaydangar/chaquopy_flutter#configuration-steps-
import sys
import threading
import traceback

from trainer.main import main

def wrap(function, *args):
    """Wrap a function call to catch exceptions."""
    def func(*storelist):
        store = storelist[0]
        output = "Oh no"
        try:
            output = function(*args)
        except BaseException:
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)
        finally:
            store[0] = output
            return

    return func


def mainTextCode(code):
    # We need to run python in a separate thread or the main thread will hang
    # store = [None]
    # callback = wrap(main)
    # t = threading.Thread(target=callback, args=[store], daemon=True)
    # t.start()
    # return store[0]

    # Run blockingly for now
    return wrap(main)()

