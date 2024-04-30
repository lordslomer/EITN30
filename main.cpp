#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <queue>
#include <cstdlib>     // For atoi
#include <RF24/RF24.h> // Assuming RF24 library is installed
#include <unistd.h>    // For sleep
#include <sys/ioctl.h>
#include <linux/if.h>
#include <linux/if_tun.h>
#include <fcntl.h>
#include <cstring>
#include <tuntap.h>

#define PSIZE 31
#define MAXBITS 0xFF
#define TUN_NAME "myG"
#define TUN_IP_BASE "10.0.0."
#define TUN_MTU 1500

std::mutex in_lock;
std::queue<std::vector<uint8_t>> in_buffer;
std::mutex out_lock;
std::queue<std::vector<uint8_t>> out_buffer;
std::condition_variable in_cv, out_cv;

uint8_t addresses[2][1] = {{'B'}, {'M'}};

void tun_receiving(RF24 &tx, int tun_fd);
void tx_sending(RF24 &tx);
void tun_sending(int tun_fd);
void rx_receiving(RF24 &rx);

void tun_receiving(device *dev)
{
  uint8_t buffer[TUN_MTU];
  while (true)
  {
    int bytes_read = tuntap_read(dev, reinterpret_cast<char *>(buffer), TUN_MTU);
    if (bytes_read < 0)
    {
      std::cerr << "Error reading from TUN device." << std::endl;
      return;
    }

    std::vector<uint8_t> tun_packet(buffer, buffer + bytes_read);
    {
      std::lock_guard<std::mutex> lock(out_lock);
      out_buffer.push(tun_packet);
    }
    out_cv.notify_all();
  }
}

void tx_sending(RF24 &tx)
{
  while (true)
  {
    std::vector<uint8_t> tun_packet;
    {
      std::unique_lock<std::mutex> lock(out_lock);
      out_cv.wait(lock, []
                  { return !out_buffer.empty(); });
      tun_packet = out_buffer.front();
      out_buffer.pop();
    }

    // Fragmentation
    size_t tun_packet_size = tun_packet.size();
    if (tun_packet_size > 0)
    {
      int c = 1;
      size_t index = 0;
      while (index < tun_packet_size)
      {
        // Determine the size of the fragment
        int max_size = std::min(PSIZE, static_cast<int>(tun_packet_size - index));
        int fragment_size = (max_size == PSIZE) ? PSIZE : MAXBITS;

        // Construct the fragment (size byte + data)
        std::vector<uint8_t> fragment;
        fragment.push_back(static_cast<uint8_t>(fragment_size));
        fragment.insert(fragment.end(), tun_packet.begin() + index, tun_packet.begin() + index + max_size);

        // Send the fragment
        tx.write(fragment.data(), fragment.size());

        index += max_size;
        c++;
      }
    }
  }
}

void tun_sending(struct device *dev)
{
  uint8_t buffer[TUN_MTU];
  while (true)
  {
    std::vector<uint8_t> tun_packet;
    {
      std::unique_lock<std::mutex> lock(in_lock);
      in_cv.wait(lock, []
                 { return !in_buffer.empty(); });
      tun_packet = in_buffer.front();
      in_buffer.pop();
    }

    std::memset(buffer, 0, sizeof(buffer));
    std::memcpy(buffer, tun_packet.data(), std::min(static_cast<int>(tun_packet.size()), TUN_MTU));

    int bytes_written = tuntap_write(dev, reinterpret_cast<char *>(buffer), TUN_MTU);
    if (bytes_written < 0)
    {
      std::cerr << "Error writing to TUN device." << std::endl;
      return;
    }
  }
}

void rx_receiving(RF24 &rx)
{
  std::vector<uint8_t> buffer;
  while (true)
  {
    if (rx.available())
    {
      std::vector<uint8_t> packet(rx.getDynamicPayloadSize());
      rx.read(packet.data(), rx.getDynamicPayloadSize());
      int c = packet[0];
      packet.erase(packet.begin());
      buffer.insert(buffer.end(), packet.begin(), packet.end());
      if (c == MAXBITS)
      {
        {
          std::lock_guard<std::mutex> lock(in_lock);
          in_buffer.push(buffer);
        }
        in_cv.notify_all();
        buffer.clear();
      }
    }
    usleep(100); // Sleep for a millisecond
  }
}

int main(int argc, char *argv[])
{
  if (argc != 2)
  {
    std::cerr << "Usage: " << argv[0] << " <unit>" << std::endl;
    return 1;
  }

  int unit = atoi(argv[1]);
  if (unit != 0 && unit != 1)
  {
    std::cerr << "Invalid unit number. Should be 0 or 1." << std::endl;
    return 1;
  }

  // Create the TUN interface
  struct device *dev = tuntap_init();
  if (!dev)
  {
    std::cerr << "Error creating TUN device." << std::endl;
    return 1;
  }
  tuntap_start(dev, TUNTAP_MODE_ETHERNET, 0);
  tuntap_set_ifname(dev, TUN_NAME);
  tuntap_set_ip(dev, (TUN_IP_BASE + std::to_string(unit + 1)).c_str(), 24);
  tuntap_set_mtu(dev, TUN_MTU);
  tuntap_up(dev);
  // two radios, one for sending and one for receiving
  RF24 rx(17, 0);
  RF24 tx(27, 10);

  // Start rx & tx
  if (!rx.begin())
  {
    std::cerr << "rx radio was not started" << std::endl;
    return 1;
  }
  if (!tx.begin())
  {
    std::cerr << "tx radio was not started" << std::endl;
    return 1;
  }

  // Set PA level
  rx.setPALevel(RF24_PA_LOW);
  tx.setPALevel(RF24_PA_LOW);

  rx.setRetries(10, 5);
  tx.setRetries(10, 5);

  if (unit == 0)
  {
    rx.setChannel(118);
    tx.setChannel(107);
  }
  else
  {
    rx.setChannel(107);
    tx.setChannel(118);
  }

  // Set highest datarate
  rx.setDataRate(RF24_2MBPS);
  tx.setDataRate(RF24_2MBPS);

  // Select sending and listening pipes
  rx.openReadingPipe(1, addresses[!unit]);
  tx.openWritingPipe(addresses[unit]);

  rx.enableDynamicPayloads();
  tx.enableDynamicPayloads();

  rx.setAutoAck(true);
  tx.setAutoAck(true);

  // enable rx & tx mode
  rx.startListening();
  tx.stopListening();

  // Flush rx & tx queues
  rx.flush_rx();
  tx.flush_tx();

  std::thread tun_reading_thread([&]()
                                 { tun_receiving(dev); });
  std::thread tx_thread([&]()
                        { tx_sending(tx); });
  std::thread tun_sending_thread([&]()
                                 { tun_sending(dev); });
  std::thread rx_thread([&]()
                        { rx_receiving(rx); });

  tun_reading_thread.join();
  tx_thread.join();
  tun_sending_thread.join();
  rx_thread.join();

  tuntap_destroy(dev);
  return 0;
}