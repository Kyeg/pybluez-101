# pybluez-101

> Bluetooth for Python: [pybluez/pybluez](https://github.com/pybluez/pybluez)


## Environment

+ Platform: MacOS (Darwin) or Linux (+ zsh/oh-my-zsh)
+ Python: 3.9.2 (default Python version on Raspberry Pi OS, until 2023.10)
+ Package Management: venv/pyenv + pip
+ Formatter: Black


## Get Started

Install the environment through **pyenv** (for multiple versions)
```
pyenv install 3.9.2
pyenv virtualenv 3.9.2 project-name-version
pyenv activate project-name-version
pip3 install --upgrade pip
pip3 install -r requirements/requirements_platform_python_version.txt

pyenv deactivate
```

Install the environment through **venv** (for single version)
```
python3 -m venv .venv
source .venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements/requirements_platform_python_version.txt

deactivate
```

Always update the dependency files (Edit: top + Freeze: locked) if you install new packages:
```
vim requirements/requirements-top.txt
pip3 freeze > requirements/requirements_platform_python_version.txt
```

## Program Arguments

Optionally add program arguments in `.vscode/launch.json`.
For example, add bluetooth MAC address for connecting.


## Trouble-shooting for PyBluez

### Dependency
+ Linux
    + `$ sudo apt-get install bluetooth libbluetooth-dev bluez python-bluez`

### Trouble-shooting
+ 'Installation - error in PyBluez setup command: use_2to3 is invalid'
    + Install PyBluez==0.30 from source (latest Bluetooth Python extension module  as [pybluez/setup.py](https://github.com/pybluez/pybluez/blob/master/setup.py))
    + [< Ref >](https://github.com/pybluez/pybluez/issues/431#issuecomment-1107884273)
+ 'Discoverable Mode'
    + `$ sudo hciconfig hci0 piscan (can be added in shell booting procedure)`
    + or `$ bluetoothctl discoverable` + `$ bluetoothctl discoverable-timeout=0` (but may not feasible in every legacy device)
    + [< Ref >](https://github.com/sraodev/bluetooth-service-rfcomm-python)
+ 'No such file or directory'
    + Put `$ ExecStart=/usr/lib/bluetooth/bluetoothd -C` in /lib/systemd/system/bluetooth.service, and etc.
    + [< Ref >](https://stackoverflow.com/questions/36675931/bluetooth-btcommon-bluetootherror-2-no-such-file-or-directory/63455894#63455894)
+ 'Permission denied'
    + `$ sudo chgrp bluetooth /var/run/sdp`, and etc.
    + [< Ref >](https://stackoverflow.com/questions/34599703/rfcomm-bluetooth-permission-denied-error-raspberry-pi/42306883#42306883)
+ 'Connection refused'
    + `$ DisablePlugins = pnat`, and etc.
    + [< Ref >](https://stackoverflow.com/questions/31331741/what-does-disableplugins-pnat-do)


## ToDo List

+ [x] Basic RFCOMM Protocol
+ [x] Re-connect after Discovery Fail (n-times)
+ [x] Exchange JSON String
+ [x] Solve Bluetooth Buffer Size Constraint by Chunk-based Communication
+ [ ] Re-send after Send Fail (n-times)
+ [ ] Optimize Chunk-based Communication 
    + Problem: Small buffer size (e.g., BLE: only 20 bytes) -> Nearly Always Overflow
    + [ ] Trial-1: Measure Overhead of Chunk-combination -> Will doing Chunk-combination with Recv make recv faster !?
    + [ ] Trial-2: Do not recv the whole data once, but separate the data-to-be-sent beforehand and sent it / process it one-by-one (this assumption only holds when the data can be sequentially processed)
    + [ ] Trial-3: For Small Buffer Size (e.g., BLE: only 20 bytes), directly put Message Length in the 1st transmission (e.g., ML=xxxx), then other transmissions can be fill with messages themselves (e.g., { ooo: xxx })

