# procon2-hid-tool
A small tool to enable HID Input on Nintendo Pro Controller 2. This will allow for you to use the controller with Steam (or other applications) until better drivers/support is added. 

---

# Note
**Tested only on Linux.**

---

# Installation

1. Download the files:
* procon2-hid.py
* pyproject.toml
* uv.lock

2. Plug in your Nintendo Pro Controller 2.

3. In the folder with the files, run the following commands:
   
	```bash
	$ python3 procon2-hid.py
	```

	If all went well then you should see all 4 player number indicator lights light up (this is those square looking LEDs by the charging port) and the success message:

	```
	Controller initialization sequence complete! All LEDs should be on.
	```

5. Run your program that requires a controller (such as Dolphin) and see if the controller connected successfully.

---

# Additional Notes

This is essentially just a Python version of [Procon2Tool](https://handheldlegend.github.io/procon2tool/) since WebHID is dodgy on the Firefox based browser I use.

Tested on Manjaro Linux (Arch Linux-based)

---

# Troubleshooting

## I'm seeing the error "Searching for Nintendo Switch Controllers...Device not found"

Make sure your controller is plugged into your computer and your OS recognizes your controller being plugged in.  You can verify if your OS detects your controller by looking in the `/dev/input` directory.  There you should see `js#` (where `#` is all input devices connected to your computer).  When you plug your controller in, you should see a new "character device" file type.  If you do not see this new file being added, either the resource is busy or your OS cannot detect the device.  If the resource is busy, you will need to exit any program that may be interferring with the controller (in my testing, if Dolphin is already open, then my controller cannot connect - instead, I would need to close Dolphin first, plug in my controller then reopen Dolphin).  If your OS cannot detect your device, you will need to consult your Linux distribution's documentation for connecting game controllers.  
