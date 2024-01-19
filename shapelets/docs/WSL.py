########################################################################################################################
# Copyright 2023 the authors (see AUTHORS file for full list).                                                         #
#                                                                                                                      #
# This file is part of shapelets.                                                                                      #
#                                                                                                                      #
# Shapelets is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General       #
# Public License as published by the Free Software Foundation, either version 2.1 of the License, or (at your option)  #
# any later version.                                                                                                   #
#                                                                                                                      #
# Shapelets is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied      #
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more  #
# details.                                                                                                             #
#                                                                                                                      #
# You should have received a copy of the GNU Lesser General Public License along with shapelets. If not, see           #
# <https://www.gnu.org/licenses/>.                                                                                     #
########################################################################################################################

r"""

# Additional WSL Installation Instructions

## Enable Custom Commands

The custom commands developed for the shapelets package will not be functional after successfully installing the package. To allow for use of these commands, please do the following:

1. In your Ubuntu terminal, type `cd` then `vim .bashrc`
2. Press `i` to enter *insert mode*, which will allow you to edit the file
3. Use the arrow keys to navigate to the bottom of the file, then add the line `export PATH="/home/user/.local/bin:$PATH"` where `user` is the username of your Ubuntu unix profile
4. Press `ESC` then type `:wq` to *write* your changes and *quit* from the VIM editor
5. Restart the Ubuntu 22.04 LTS application (close and re-open)

## Enable Graphics

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

"""