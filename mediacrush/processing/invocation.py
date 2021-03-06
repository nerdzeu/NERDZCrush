import os
import subprocess
import threading

from mediacrush.config import _cfgi


class Invocation:
    crashed = False
    exited = False
    stdout = None
    process = None
    args = []

    def __init__(self, command):
        self.command = command

    def __call__(self, *args, **kw):
        self.args = self.command.format(*args, **kw).split()
        return self

    def _target(self):
        try:
            self.process = subprocess.Popen(
                self.args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            self.stdout, _ = self.process.communicate()
        except:
            self.crashed = True
            return

    def run(self, timeout=_cfgi("max_processing_time")):
        if not self.args:
            self.args = self.command.split()

        thread = threading.Thread(target=self._target)
        thread.start()
        thread.join(timeout)

        if thread.is_alive():
            print("Terminating process")
            self.process.terminate()
            thread.join()
            self.exited = True
        self.stdout = self.stdout.decode("utf-8")
        self.returncode = self.process.returncode
