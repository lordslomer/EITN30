from pyrf24  import RF24, RF24_PA_LOW, RF24_2MBPS
from tuntap import TunTap
import threading
import argparse

PSIZE = 30
MAXBITS = 0xFFFF
addresses = [b"B", b"M"]

def tun_to_tx():
  while True:
    tun_packet = tun.read()
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
      packet_size = rx.getPayloadSize()
      packet = rx.read(packet_size)
      c = int.from_bytes(packet[:2], 'big')
      buffer.append(packet[2:])
      if c == MAXBITS:
        tun_packet = b''.join(buffer)
        buffer.clear()
        tun.write(tun_packet)

if __name__ == "__main__":
  argparse = argparse.ArgumentParser(description='NRF24L01+ myG')
  argparse.add_argument('--unit', dest='unit', type=int, default=0, help='Specify which unit this is, 0=base station 1=mobile station', choices=range(2))
  
  unit = argparse.parse_args().unit

  # Create the virtual interface 
  tun = TunTap(nic_type="Tun", nic_name="myG")
  tun.config(ip=f"10.0.0.{unit+1}", mask="255.255.255.0")

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
  
  # Set highest datarate
  rx.setDataRate(RF24_2MBPS)
  tx.setDataRate(RF24_2MBPS)

  # Select sending and listening pipes
  rx.open_rx_pipe(1, addresses[not unit])
  tx.open_tx_pipe(addresses[unit])
  
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

  sending_thread.join()
  reciving_thread.join()

