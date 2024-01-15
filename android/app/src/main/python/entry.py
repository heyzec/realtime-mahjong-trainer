#unused
import sys
import os

# wrt /data/data/com.example.realtime_mahjong_trainer/ in device
BASE = "/data/data/com.example.realtime_mahjong_trainer/"
HOT_RELOAD_DIR = "files/reload"

def entry():
    print("entering")
    path = os.path.join(BASE, HOT_RELOAD_DIR)
    if not os.path.exists(path) or len(os.listdir(path)) == 0:
        print("use old files")
        # result = main()
        # print(os.getcwd())
        # print(sys.path)
        # print(__file__)
        # print(result)
        # time.sleep(10)
        # return result
        pass
    else:
        print("relaoding")
        try:
            sys.path.remove(os.path.join(BASE, "files/chaquopy/AssetFinder/app"))
            sys.path.append(os.path.join(BASE, HOT_RELOAD_DIR))
        except ValueError as e:
            print(e)

    from main import main
    print('starting main')
    main()








# def wrap(function, *args):
#     """Wrap a function call to catch exceptions."""
#     def func(*storelist):
#         store = storelist[0]
#         output = "Oh no"
#         try:
#             output = function(*args)
#         except BaseException:
#             exc_info = sys.exc_info()
#             traceback.print_exception(*exc_info)
#         finally:
#             store[0] = output
#             return

#     return func


# def mainTextCode(code):
#     # We need to run python in a separate thread or the main thread will hang
#     # store = [None]
#     # callback = wrap(main)
#     # t = threading.Thread(target=callback, args=[store], daemon=True)
#     # t.start()
#     # return store[0]

#     # Run blockingly for now
#     return wrap(main)()

