
import speedtest
import time
import socket

# Define the IP address and port number of the laptop
laptop_ip = "127.0.0.1"
port = 500

# Set up the speedtest object
st = speedtest.Speedtest()

# Define a function to send the network data to the laptop
def send_network_data(download_speed, upload_speed):
    try:
        # Create a socket connection to the laptop
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((laptop_ip, port))

        # Send the download and upload speeds to the laptop
        s.sendall(f"{download_speed},{upload_speed}".encode())
        s.close()
    except:
        print("Unable to connect to laptop.")

# Run the network test every hour for 12 hours
for i in range(12):
    # Get the upload and download speeds
    download_speed = st.download() / 1000000.0
    upload_speed = st.upload() / 1000000.0

    # Send the network data to the laptop
    send_network_data(download_speed, upload_speed)

    # Wait for an hour before running the test again
    time.sleep(3600)
