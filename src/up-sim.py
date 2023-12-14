import sys
from time import sleep

from smartcard.ReaderMonitoring import ReaderMonitor, ReaderObserver


class printobserver(ReaderObserver):
    """A simple reader observer that is notified
    when readers are added/removed from the system and
    prints the list of readers
    """

    def update(self, observable, actions):
        (addedreaders, removedreaders) = actions
        print(f"Wykryte czytniki: {addedreaders[0]}, {addedreaders[1]}")


def display_reader_name():
    readermonitor = ReaderMonitor()
    readerobserver = printobserver()
    readermonitor.addObserver(readerobserver)
    sleep(0.1)
    readermonitor.deleteObserver(readerobserver)


if __name__ == "__main__":
    display_reader_name()

if "win32" == sys.platform:
    print("press Enter to continue")
    sys.stdin.read(1)
