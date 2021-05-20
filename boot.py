# set up to broadcast a webpage
# regsister and prepare the temp probes
import network

AP = network.WLAN(network.AP_IF)
AP.config(essid="compost")
# what is the config var for password lol
AP.active(True)
