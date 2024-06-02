def _decorator(func):
    def inner(args, **kwargs):
        print("Decorator:setting connection")
        func(args, **kwargs)

    return inner()