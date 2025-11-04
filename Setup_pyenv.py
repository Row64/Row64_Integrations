import os
import subprocess as sp

'''===========================================================

  Setup pyenv for row64 integrations
  
  Since Ubuntu 24.04 and forward, you can't pip install on the OS level python,
  This is to prevent interfering with the OS python calls and corrupt the OS 
 
  The solution is to install a second version of python, and then pip install
  to that new version.  The simplest way to do this is to install pyenv
  More details here: https://realpython.com/intro-to-pyenv/

  All row64 integrations that use python depend on running this setup as a first step
  
  Install using:
  python3 Setup_pyenv.py
  (will ask for sudo password)

  After installation you will be able to:
    - call 'python' for your newly installed python that can be modified
    - call 'python3' to run the default OS version
    - call pip to install to your new installed python
    -call pyenv in the terminal to add additional python versions or change the setup

  How to test it's working in the terminal
    - in the terminal: pip install row64tools
    - in the terminal: python
    - python prompt: import row64tools
    - python prompt: quit()
    - if there's no error it's working, you've installed row64tools and imported it

==========================================================='''

def Setup_pyenv():

    # Since Ubuntu 24.04 and forward, you can't pip install libraries without installing
    # a second version of Python.  The simplest way to do this is to install pyenv
    # More details here: https://realpython.com/intro-to-pyenv/

    # ------------ Pandas dependencies ------------
    sp.call(["sudo", 'bash', '-c', "apt-get install libffi-dev"])

    # ------------ setup dependencies: terminal input ------------
    # sudo apt install -y make build-essential libssl-dev zlib1g-dev
    # sudo apt install -y libbz2-dev libreadline-dev libsqlite3-dev curl git libncursesw5-dev
    # sudo apt install -y xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
    
    # ------------ setup dependencies: from python ------------
    sp.call(["sudo", 'bash', '-c', "apt install -y make build-essential libssl-dev zlib1g-dev"])
    sp.call(["sudo", 'bash', '-c', "apt install -y libbz2-dev libreadline-dev libsqlite3-dev curl git libncursesw5-dev"])
    sp.call(["sudo", 'bash', '-c', "apt install -y xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev"])

    # ------------ install pyenv: terminal input ------------
    # curl -fsSL https://pyenv.run | bash

    # ------------ install pyenv: from python ------------
    sp.call(['bash', '-c', "curl -fsSL https://pyenv.run | bash"])

    # setup .bashrc to set path to pyenv when terminal is opened
    
    # ------------ setup .bashrc path: terminal input ------------
    # to do it by hand, use these steps and restart the terminal
    # echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    # echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    # echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc

    # ------------ setup .bashrc path: from python ------------
    brcPath = "/home/row64/.bashrc"
    with open(brcPath) as file:fContent = file.read()
    fContent += '''
    export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"'''
    f = open(brcPath, "w")
    f.write(fContent)
    f.close()

    # ------------ install python 3.14 and set global: terminal input ------------
    # --------- requires closing terminal and reopening before this step ---------
    # pyenv install 3.14
    # pyenv global 3.14        

    # --------- install python 3.14 and set global: from python ---------    
    sp.call(['bash', '-c', "/home/row64/.pyenv/bin/pyenv install 3.14"])
    sp.call(['bash', '-c', "/home/row64/.pyenv/bin/pyenv global 3.14"])
    
    print("                                                                           ")   
    print("---------------------- Python pyenv install complete ----------------------")
    print("                                                                           ")
    print("                                IMPORTANT                                  ")
    print("              Please close terminal and reopen before using                ")
    print("                                                                           ")
    print("---------------------------------------------------------------------------")
    print("                                                                           ")


Setup_pyenv()


