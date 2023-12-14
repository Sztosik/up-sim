#!/usr/bin/env python3

from smartcard.util import toBytes, toASCIIString
import usim
from dataclasses import dataclass
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
        print(f"\n\n\n\nWykryte czytniki: {addedreaders[0]}, {addedreaders[1]}")


def display_reader_name():
    readermonitor = ReaderMonitor()
    readerobserver = printobserver()
    readermonitor.addObserver(readerobserver)
    sleep(0.1)
    readermonitor.deleteObserver(readerobserver)

@dataclass
class Contact:
    phone_nr: str
    name: str

def decode_record(record):
    """
    decode_record(toBytes("43 75 73 74 6F 6D 65 72 20 43 61 72 65 FF 06 A1 80 00 07 70 00 FF FF FF FF FF FF FF"))
    >> ['Customer Care', '0800700700']
    """
    X = len(record) - 14
    name = toASCIIString(record[0:X - 1]).replace("ÿ", "")
    # number of bytes for the phone number
    tel_size = record[X]
    phone = record[X + 2:X + tel_size + 1]

    decoded = ""
    for n in phone:
        hex = "%02X" % n
        high = hex[0]
        low = hex[1]
        decoded += low + high
    # if the number of digits is odd we suppress the padding
    if decoded[-1] == "F":
        decoded = decoded[:-1]
    phone = decoded

    return name, phone


def usim_read(reader_nb):
    # Select the EF ADN
    (size, connection) = usim.usim(reader_nb)

    contacts = []

    for nbr in range(1, 250):
        #  Read record
        header = [0xA0, 0xB2]
        record_idx = nbr
        cmd = header + [record_idx, 0x04, size]
        data, sw1, sw2 = connection.transmit(cmd)
        if (sw1, sw2) != (0x90, 0x00):
            return

        name, phone = decode_record(data)

        if data == [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]:
            break

        if name != "":
            contacts.append(Contact(phone, name))
            # print(f"{record_idx}: Name: {name}, phone: {phone}")

    display_reader_name()
    print("\nKontakty: ")
    print("---------")
    for contact in contacts:
        print(f"{contact.name}, nr tel.: {contact.phone_nr}")
    print("---------")


if __name__ == "__main__":
    import sys
    if 2 == len(sys.argv):
        reader_nb = int(sys.argv[1])
    else:
        reader_nb = 0
    usim_read(reader_nb)
