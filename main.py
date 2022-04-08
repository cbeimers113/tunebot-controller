import sys

from tunebot.frontend import FrontEnd
from util.log import Log


if __name__ == '__main__':
    log = Log()

    # Create and start the application
    try:
        FrontEnd.FRONTEND = FrontEnd()
        FrontEnd.FRONTEND.run()
    except Exception as e:
        log.error('An extreneous exception arose:')
        log.no_prefix(e)
        sys.exit(1)
