import os
from pyrf24  import RF24, RF24_PA_LOW, RF24_2MBPS
import threading
from pytun import TunTapDevice
import argparse

PSIZE = 30
MAXBITS = 0xFFFF
addresses = [b"B", b"M"]

def tun_to_tx():
  while True:
    tun_packet = tun.read(tun.mtu)
    tun_packet_size = len(tun_packet)
    
    radio_packages = []

    if tun_packet_size>0:
      c = 1
      while tun_packet:
          if (tun_packet_size <= PSIZE):
              c = MAXBITS
          radio_packages.append(c.to_bytes(2, 'big') + tun_packet[:PSIZE])
          tun_packet = tun_packet[PSIZE:]
          tun_packet_size = len(tun_packet)
          c += 1

    for package in radio_packages:
      tx.write(package)

def rx_to_tun():
  buffer = []
  while True:
    has_payload = rx.available()
    if has_payload:
      packet_size = rx.get_dynamic_payload_size()
      packet = rx.read(packet_size)
      c = int.from_bytes(packet[:2], 'big')
      buffer.append(packet[2:])
      if c == MAXBITS:
        tun_packet = b''.join(buffer)
        buffer.clear()
        tun.write(tun_packet)

if __name__ == "__main__":
  try:
    argparse = argparse.ArgumentParser(description='NRF24L01+ myG')
    argparse.add_argument('--unit', dest='unit', type=int, default=0, help='Specify which unit this is, 0=base station 1=mobile station', choices=range(2))
    
    unit = argparse.parse_args().unit

    # Create the virtual interface 
    tun = TunTapDevice(name='myG')
    tun.addr = f"10.0.0.{unit+1}"
    tun.dstaddr = f"10.0.0.{(not unit)+1}"
    tun.netmask="255.255.255.0"
    tun.mtu = 1500
    tun.up()

    # if unit == 1:
    #   os.system("sudo ip route add 10.0.0.1 dev myG")

    # two radios, one for sending (spidev0) and one for reciving (spidev1)
    rx = RF24(17,0)
    tx = RF24(27,10)
    
    # Start rx & tx
    if not rx.begin():
      print("rx radio was not started")
    if not tx.begin():
      print("tx radio was not started")
    
    # Set PA level
    rx.setPALevel(RF24_PA_LOW)
    tx.setPALevel(RF24_PA_LOW)
    
    rx.set_retries(15, 5)
    tx.set_retries(15, 5)

    if unit == 0:
      rx.setChannel(118)
      tx.setChannel(107)
    else:
      rx.setChannel(107)
      tx.setChannel(118)

    # Set highest datarate
    rx.setDataRate(RF24_2MBPS)
    tx.setDataRate(RF24_2MBPS)

    # Select sending and listening pipes
    rx.open_rx_pipe(1, addresses[not unit])
    tx.open_tx_pipe(addresses[unit])
    
    rx.dynamic_payloads = True
    tx.dynamic_payloads = True

    rx.set_auto_ack(True)
    tx.set_auto_ack(True)

    # enable rx & tx mode
    rx.listen = True
    tx.listen = False
    
    # Flush rx & tx queues
    rx.flush_rx()
    tx.flush_tx()


    sending_thread = threading.Thread(target=tun_to_tx, args=())
    reciving_thread = threading.Thread(target=rx_to_tun, args=())

    sending_thread.start()
    reciving_thread.start()
    
  except KeyboardInterrupt:
    print(" Keyboard Interrupt detected. Powering down radio.")
    rx.powerDown()
    tx.powerDown()
    tun.close()
  

