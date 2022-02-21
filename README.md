# eeg
🧠 A collection of data and script examples for EEG analysis

## Setup for OpenBCI

### Drivers

Install the [virtual COM port driver](https://ftdichip.com/drivers/vcp-drivers/) to enable communication from your PC to the dongle

- [Direct link to latest Windows driver installer (as of 2022-02-21)](https://ftdichip.com/wp-content/uploads/2021/08/CDM212364_Setup.zip)

#### Fix buffer latency

This step should fix an issue with the default settings that make the data coming in "choppy".

[Follow the steps from the OpenBCI documentation](https://docs.openbci.com/Troubleshooting/TroubleshootingLanding/)

- [Direct link to Windows buffer fix instructions](https://docs.openbci.com/Troubleshooting/FTDI_Fix_Windows/)

### OpenBCI gui

Download and extract the latest [OpenBCI GUI application](https://openbci.com/downloads).
This lets you see data straight away, and also gives you a way to check everything is working ok.

- [Direct link to latest Windows OpenBCI GUI (as of 2022-02-21)](https://github.com/OpenBCI/OpenBCI_GUI/releases/download/v5.0.9/openbcigui_v5.0.9_2021-11-06_00-16-07_windows64.zip)

#### Fix HDPI screen scaling

If you have a relatively new computer or high resolution screen, the default settings make the app look messed up.

- Right click on `OpenBCI_GUI.exe`
- Click properties (on Windows 11, Show more options -> properties)
- Click the Compatibility tab
- Click the "Change high DPI settings" button
- Check the "Override high DBPI scaling behaviour." checkbox under "High DPI scaling override"
- Change "Scaling performed by:" to `System (Enhanced)`

![image](https://user-images.githubusercontent.com/75656/154969142-fcc82bd9-f18a-4395-a7d0-015cc86f16c5.png)

### Setup Hardware

#### Plug in dongle

Attach the dongle to a USB port.

#### Connect inputs

Follow the pin map diagram in the box (it will eventually be uploaded here too)

#### Verify connection

- Turn on the Cyton board, the switch should be in the PC position
- Start a session in OpenBCI GUI

![image](https://user-images.githubusercontent.com/75656/154969819-98630c3e-080e-428f-84c8-365a50b5c0d9.png)

Click "AUTO-CONNECT" then "START SESSION", you should see some data coming in. Make sure it's set to 16 channels (if that's what you want)

**Note: Denmark and other European countries use 50Hz AC frequency, so make sure it's set to 50Hz** otherwise you'll just see a ton of AC noise.




