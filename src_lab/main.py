
from time import sleep

from smartcard.ReaderMonitoring import ReaderMonitor, ReaderObserver


class printobserver(ReaderObserver):
    """A simple reader observer that is notified
    when readers are added/removed from the system and
    prints the list of readers
    """

    def update(self, observable, actions):
        (addedreaders, removedreaders) = actions
        print("Added readers", addedreaders)
        print("Removed readers", removedreaders)

if __name__ == '__main__':
    print("Add or remove a smartcard reader to the system.")
    print("This program will exit in 10 seconds")
    print("")
    readermonitor = ReaderMonitor()
    readerobserver = printobserver()
    readermonitor.addObserver(readerobserver)

    sleep(10)

    # don't forget to remove observer, or the
    # monitor will poll forever...
    readermonitor.deleteObserver(readerobserver)

    import sys
    if 'win32' == sys.platform:
        print('press Enter to continue')
        sys.stdin.read(1)