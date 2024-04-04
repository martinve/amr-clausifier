import sys
import config


def debug_print(*args, **kwargs):
    if not config.debug_print_flag:
        return
    print(*args, **kwargs)


def debug_exit(*args, **kwargs):
    debug_print(*args, **kwargs)
    print("Exiting.")
    sys.exit(-1)
