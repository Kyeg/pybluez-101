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

# Arguments
Optionally add arguments in .vscode/launch.json 
