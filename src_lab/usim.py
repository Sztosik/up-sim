#!/usr/bin/env python3

from smartcard.System import readers
from smartcard.util import toBytes, padd
from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver

debug = True

def usim(reader_nb):
    # get all the available readers
    r = readers()
    print("Available readers:")
    for reader in r:
        print("-", reader)

    reader = r[reader_nb]
    print("Using:", reader)

    connection = reader.createConnection()
    if debug:
        observer = ConsoleCardConnectionObserver()
        connection.addObserver(observer)
    connection.connect()

    SELECT = "A0 A4 00 00 02 "
    GET_RESPONSE = "A0 C0 00 00 "

    # Select MF
    print("Select MF")
    data, sw1, sw2 = connection.transmit(toBytes(SELECT + "3F 00"))
    if sw1 != 0x9F:
        raise(Exception("Error"))

    # Select DF Telecom
    print("Select DF Telecom")
    data, sw1, sw2 = connection.transmit(toBytes(SELECT + "7F 10"))
    if sw1 != 0x9F:
        raise(Exception("Error"))

    # Select EF ADN
    print("Select EF ADN")
    data, sw1, sw2 = connection.transmit(toBytes(SELECT + "6F 3A"))
    if (sw1, sw2) != (0x9F, 0x0F):
        raise(Exception("Error"))

    # Get Response
    print("Get Response")
    data, sw1, sw2 = connection.transmit(toBytes(GET_RESPONSE) + [sw2])
    if (sw1, sw2) != (0x90, 0x00):
        raise(Exception("Error"))

    size = data[-1]

    pin = None
    if pin:
        print(pin)
        pin = list(map(ord, pin))
        padd(pin, 8)

        # Verify CHV
        VERIFY = "A0 20 00 01 08"
        cmd = toBytes(VERIFY) + pin
        data, sw1, sw2 = connection.transmit(cmd)
        if (sw1, sw2) != (0x90, 0x00):
            raise(Exception("Wrong PIN:" + pin))

    return size, connection


if __name__ == "__main__":
    usim(0)
