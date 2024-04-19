from pyrf24  import RF24, RF24_PA_LOW, RF24_2MBPS
from tuntap import TunTap
import argparse

addresses = [b"B", b"M"]

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
  rx.openReadingPipe(1, addresses[not unit])
  tx.openWritingPipe(addresses[unit])

  # Flush rx & tx queues
  rx.flush_rx()
  tx.flush_tx()

  rx.print_pretty_details()
  tx.print_pretty_details()

  rx.powerDown()
  tx.powerDown()