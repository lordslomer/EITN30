import time
from pyrf24  import RF24, RF24_PA_LOW, RF24_2MBPS
import threading
from myQueue import Queue
from pytun import TunTapDevice, IFF_NO_PI, IFF_TUN 
import argparse

FRAGMENT_SIZE = 31
CANCELBITS = 0xFE
MAXBITS = 0xFF
RADIO_ADDR = [b"B", b"M"]

in_buffer = Queue("incoming")
out_buffer = Queue("outgoing")


# Read packets from the TUN interface and queue them up in the out_buffer
def tun_receiving():
    while True:
        tun_packet = tun.read(tun.mtu)
        out_buffer.put(tun_packet)

# Fragment packets from the out_buffer and send them over tx
def tx_sending():
  while True:
    tun_packet = out_buffer.pop()

    # Start fragmentation
    tun_packet_size = len(tun_packet)
    if tun_packet_size>0:

      # Define the control byte as a seq_nbr by default (If not MAXBITS or CANCELBITS)
      c = 1

      while tun_packet:
          
          # If last fragment, c -> MAXBITS
          if (tun_packet_size <= FRAGMENT_SIZE):
              c = MAXBITS
          
          # Send the next fragment
          result = tx.write(c.to_bytes(1, 'big') + tun_packet[:FRAGMENT_SIZE])

          # If sending fails, send a cancel fragment containing CANCELBITS
          if not result: 

            # Loop until cancel successful 
            cancled = False
            while not cancled:
              cancled = tx.write(CANCELBITS.to_bytes(1, 'big'))

            # Reset packet 
            tun_packet = []
            tun_packet_size = 0
            continue
          
          # If sending successful, decrement the packet = packet - fragment 
          tun_packet = tun_packet[FRAGMENT_SIZE:]
          tun_packet_size = len(tun_packet)
          c += 1

# Write packets to the TUN interface from the in_buffer 
def tun_sending():
  while True:
    tun_packet = in_buffer.pop() 
    tun.write(tun_packet)

# Reassemble packets one fragment at a time and queue them in in_buffer
def rx_receiving():

  # Start with empty packet
  buffer = []
  while True:

    # Check if there is a fragment to read
    has_payload = rx.available()
    if has_payload:

      # Read fragment by size
      packet_size = rx.get_dynamic_payload_size()
      packet = rx.read(packet_size)

      # Extract control byte
      c = int.from_bytes(packet[:1], 'big')
      buffer.append(packet[1:])


      if c == MAXBITS:
        
        # Last fragment reached, reassemble packet and send to queue
        tun_packet = b''.join(buffer)
        buffer.clear()
        in_buffer.put(tun_packet)

      elif c == CANCELBITS:

        # Fragment lost, clear queue.
        buffer.clear()
      
    time.sleep(1/7900)

if __name__ == "__main__":
  try:
    argparse = argparse.ArgumentParser(description='NRF24L01+ myG')
    argparse.add_argument('--unit', dest='unit', type=int, default=0, help='Specify which unit this is, 0=base station 1=mobile station', choices=range(2))
    
    # 0 for base
    # 1 for mobile
    unit = argparse.parse_args().unit

    # Create the virtual interface 
    tun = TunTapDevice(name='myG', flags=IFF_TUN|IFF_NO_PI)

    # 10.0.0.1 for base
    # 10.0.0.2 for mobile
    tun.addr = f"10.0.0.{unit+1}"
    tun.dstaddr = f"10.0.0.{(not unit)+1}"
    tun.netmask="255.255.255.0"

    # Set MTU (max packet size) 
    tun.mtu = 1500
    tun.up()


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
    
    # Delay 1 * 250 us
    # 2 retries
    rx.set_retries(1, 2)
    tx.set_retries(1, 2)

    # uplink on channel 118
    # downlink on channel 107
    if unit == 0:
      rx.setChannel(118)
      tx.setChannel(107)
    else:
      rx.setChannel(107)
      tx.setChannel(118)

    # Set highest datarate 2Mbps
    rx.setDataRate(RF24_2MBPS)
    tx.setDataRate(RF24_2MBPS)

    # Select sending and listening pipes
    rx.open_rx_pipe(1, RADIO_ADDR[not unit])
    tx.open_tx_pipe(RADIO_ADDR[unit])
    
    # Enables automatic detection of fragment size
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

    # Create the workign threads
    tun_reading_thread = threading.Thread(target=tun_receiving, args=())
    tx_thread = threading.Thread(target=tx_sending, args=())
    tun_sending_thread = threading.Thread(target=tun_sending, args=())
    rx_thread = threading.Thread(target=rx_receiving, args=())

    # Start the working threads
    tun_sending_thread.start()
    tun_reading_thread.start()
    tx_thread.start()
    rx_thread.start()
    
  except KeyboardInterrupt:
    print(" Keyboard Interrupt detected. Powering down radio.")
    rx.powerDown()
    tx.powerDown()
    tun.close()
  

