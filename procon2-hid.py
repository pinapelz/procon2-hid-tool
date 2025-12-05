import usb.core
import usb.util
import time
import sys

VENDOR_ID = 0x057E
PRODUCT_IDS = {
    0x2066: "Joy-Con (L)",
    0x2067: "Joy-Con (R)",
    0x2069: "Pro Controller",
    0x2073: "GCN Controller"
}

USB_INTERFACE_NUMBER = 1

INIT_COMMAND_0x03 = bytes([0x03, 0x91, 0x00, 0x0d, 0x00, 0x08, 0x00, 0x00, 0x01, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
UNKNOWN_COMMAND_0x07 = bytes([0x07, 0x91, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00])
UNKNOWN_COMMAND_0x16 = bytes([0x16, 0x91, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00])
REQUEST_CONTROLLER_MAC = bytes([0x15, 0x91, 0x00, 0x01, 0x00, 0x0e, 0x00, 0x00, 0x00, 0x02, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
LTK_REQUEST = bytes([0x15, 0x91, 0x00, 0x02, 0x00, 0x11, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
UNKNOWN_COMMAND_0x15_ARG_0x03 = bytes([0x15, 0x91, 0x00, 0x03, 0x00, 0x01, 0x00, 0x00, 0x00])
UNKNOWN_COMMAND_0x09 = bytes([0x09, 0x91, 0x00, 0x07, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
IMU_COMMAND_0x02 = bytes([0x0c, 0x91, 0x00, 0x02, 0x00, 0x04, 0x00, 0x00, 0x27, 0x00, 0x00, 0x00])
OUT_UNKNOWN_COMMAND_0x11 = bytes([0x11, 0x91, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00])
UNKNOWN_COMMAND_0x0A = bytes([0x0a, 0x91, 0x00, 0x08, 0x00, 0x14, 0x00, 0x00, 0x01, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x35, 0x00, 0x46, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
IMU_COMMAND_0x04 = bytes([0x0c, 0x91, 0x00, 0x04, 0x00, 0x04, 0x00, 0x00, 0x27, 0x00, 0x00, 0x00])
ENABLE_HAPTICS = bytes([0x03, 0x91, 0x00, 0x0a, 0x00, 0x04, 0x00, 0x00, 0x09, 0x00, 0x00, 0x00])
OUT_UNKNOWN_COMMAND_0x10 = bytes([0x10, 0x91, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00])
OUT_UNKNOWN_COMMAND_0x01 = bytes([0x01, 0x91, 0x00, 0x0c, 0x00, 0x00, 0x00, 0x00])
OUT_UNKNOWN_COMMAND_0x03 = bytes([0x03, 0x91, 0x00, 0x01, 0x00, 0x00, 0x00])
OUT_UNKNOWN_COMMAND_0x0A_ALT = bytes([0x0a, 0x91, 0x00, 0x02, 0x00, 0x04, 0x00, 0x00, 0x03, 0x00, 0x00])

def send_usb_data(ep_out, ep_in, data, description=""):
    try:
        ep_out.write(data)
        time.sleep(0.01)
        try:
            response = ep_in.read(32, timeout=100)
            hex_resp = " ".join([f"{x:02x}" for x in response])
            print(f"[{description}] Response: {hex_resp}")
        except usb.core.USBError as e:
            if e.errno == 110:
                print(f"[{description}] No response (Timeout)")
            else:
                print(f"[{description}] Read Error: {e}")

    except usb.core.USBError as e:
        print(f"[{description}] Write Error: {e}")
        raise

def set_player_leds(ep_out, ep_in, led_mask):
    command = [
        0x09, 0x91, 0x00, 0x07, 0x00, 0x08, 0x00, 0x00,
        led_mask,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    ]
    send_usb_data(ep_out, ep_in, bytes(command), f"Set LED Mask: 0x{led_mask:02x}")

def connect_usb():
    print("Searching for Nintendo Switch Controllers...")
    def match_device(dev):
        return dev.idVendor == VENDOR_ID and dev.idProduct in PRODUCT_IDS
    dev = usb.core.find(custom_match=match_device)
    if dev is None:
        raise ValueError("Device not found")

    product_name = PRODUCT_IDS.get(dev.idProduct, "Unknown Device")
    print(f"Found {product_name} (ID: {dev.idProduct:04x})")
    if dev.is_kernel_driver_active(USB_INTERFACE_NUMBER):
        try:
            print("Detaching kernel driver...")
            dev.detach_kernel_driver(USB_INTERFACE_NUMBER)
        except usb.core.USBError as e:
            sys.exit(f"Could not detach kernel driver: {e}")
    try:
        dev.set_configuration()
        print("Configuration set.")
    except usb.core.USBError as e:
        print(f"Error setting configuration: {e}")
    try:
        usb.util.claim_interface(dev, USB_INTERFACE_NUMBER)
        print(f"Interface {USB_INTERFACE_NUMBER} claimed.")
    except usb.core.USBError as e:
        sys.exit(f"Could not claim interface: {e}")
    cfg = dev.get_active_configuration()
    intf = cfg[(USB_INTERFACE_NUMBER,0)]
    ep_out = usb.util.find_descriptor(
        intf,
        custom_match = lambda e:  usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)

    ep_in = usb.util.find_descriptor(
        intf,
        custom_match =
        lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
    )

    if not ep_out:
        sys.exit("Could not find OUT endpoint")

    print(f"Found Endpoint OUT: 0x{ep_out.bEndpointAddress:02x}")
    print("Starting Initialization Sequence...")

    try:
        send_usb_data(ep_out, ep_in, INIT_COMMAND_0x03, "Init 0x03")
        send_usb_data(ep_out, ep_in, UNKNOWN_COMMAND_0x07, "Unknown 0x07")
        send_usb_data(ep_out, ep_in, UNKNOWN_COMMAND_0x16, "Unknown 0x16")
        send_usb_data(ep_out, ep_in, REQUEST_CONTROLLER_MAC, "Req MAC")
        send_usb_data(ep_out, ep_in, LTK_REQUEST, "Req LTK")
        send_usb_data(ep_out, ep_in, UNKNOWN_COMMAND_0x15_ARG_0x03, "Unknown 0x15")
        send_usb_data(ep_out, ep_in, UNKNOWN_COMMAND_0x09, "Unknown 0x09")
        send_usb_data(ep_out, ep_in, IMU_COMMAND_0x02, "IMU 0x02")
        send_usb_data(ep_out, ep_in, OUT_UNKNOWN_COMMAND_0x11, "OUT Unknown 0x11")
        send_usb_data(ep_out, ep_in, UNKNOWN_COMMAND_0x0A, "Unknown 0x0A")
        send_usb_data(ep_out, ep_in, IMU_COMMAND_0x04, "IMU 0x04")
        send_usb_data(ep_out, ep_in, ENABLE_HAPTICS, "Enable Haptics")
        send_usb_data(ep_out, ep_in, OUT_UNKNOWN_COMMAND_0x10, "OUT Unknown 0x10")
        send_usb_data(ep_out, ep_in, OUT_UNKNOWN_COMMAND_0x01, "OUT Unknown 0x01")
        send_usb_data(ep_out, ep_in, OUT_UNKNOWN_COMMAND_0x03, "OUT Unknown 0x03")
        send_usb_data(ep_out, ep_in, OUT_UNKNOWN_COMMAND_0x0A_ALT, "OUT Unknown 0x0A Alt")
        set_player_leds(ep_out, ep_in, 0x0F)

        print("Controller initialization sequence complete! All LEDs should be on.")

    except Exception as e:
        print(f"Error during sequence: {e}")

if __name__ == "__main__":
    try:
        connect_usb()
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"Unexpected error: {e}")
