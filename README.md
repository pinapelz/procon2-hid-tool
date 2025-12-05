# procon2-hid-tool
A small tool to enable HID Input on Nintendo Pro Controller 2. This will allow for you to use the controller with Steam (or other applications) until better drivers/support is added. (Note this is only tested on Linux)

Install the dependencies and then plug your controller in via USB. Then just run the script and hopefully it should find your controller and send the necessary sequence of commands.

If all went well then you should see all 4 player number indicator lights light up (this is those square looking LEDs by the charging port)

This is essentially just a Python version of [Procon2Tool](https://handheldlegend.github.io/procon2tool/) since WebHID is dodgy on the Firefox based browser I use.
