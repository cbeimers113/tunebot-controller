import sys

from tunebot.frontend import FrontEnd


if __name__ == '__main__':
    # Create and start the application
    try:
        FrontEnd.FRONTEND = FrontEnd()
        FrontEnd.FRONTEND.run()
    except Exception:
        sys.exit(1)
