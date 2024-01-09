# WSL (Windows Subsystem for Linux) Additional Installation Steps

## Ubuntu graphics correction to allow graphical interfaces

**Note**: this is for WSL users only. 

Unfortunately, Ubuntu via WSL does not come with GUI (graphical user interface) application support (shortformed an "X server"). In order to view output plots or any graphical interface (such as from `matplotlib`):

1. In your Ubuntu terminal, type `sudo apt-get install ubuntu-desktop`
2. Change your environment display variables with the following
    * In your Ubuntu terminal, type `cd` then `vim .bashrc`
    * Press `i` to enter *insert mode*, which will allow you to edit the file
    * Use the arrow keys to navigate to the bottom of the file, then add the line `export DISPLAY=$(ip route list default | awk '{print $3}'):0`
    * On a new line, add `export LIBGL_ALWAYS_INDIRECT=1`
    * Press `ESC` then type `:wq` to *write* your changes and *quit* from the VIM editor
    * Restart the Ubuntu 22.04 LTS application (close and re-open)
3. Enable Public Access on your X11 server for Windows. Follow this [tutorial](https://skeptric.com/wsl2-xserver/) but be sure to only follow the section labelled *Allow WSL Access via Windows Firewall*
4. Download [VcXsrv](https://sourceforge.net/projects/vcxsrv/). 
    * On your Windows machine (not Ubuntu), navigate to `C:\Program Files\VcXsrv` and open the application`xlaunch.exe`
    * Click Next until you reach the *Extra Settings* page. Check the box for *Disable Access Control*
    * Save the configuration file somewhere useful. Ensure that you run the `config.xlaunch` file before executing code with any graphical interface or support
