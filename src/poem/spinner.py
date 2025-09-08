import itertools
import sys
import threading
from time import sleep


class Spinner():
    """A simple spinner animation for console applications."""

    def __init__(self):
        self.spinner_cycle = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.running = False
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True

    def __enter__(self):
        self.running = True
        self.thread.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.running = False
        self.thread.join()
        sys.stdout.write('\b')
        sys.stdout.flush()

    def _animate(self):
        spinner_chars = itertools.cycle(self.spinner_cycle)
        while self.running:
            sys.stdout.write('\b' + next(spinner_chars))
            sys.stdout.flush()
            sleep(0.1)
