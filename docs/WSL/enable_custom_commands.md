# WSL (Windows Subsystem for Linux) Additional Installation Steps

## Editing PATH to use `shapelets` custom commands

**Note**: this is for WSL users only.

The custom commands developed for the `shapelets` package will not be functional after successfully installing the package. To allow for use of these commands, please do the following:

1. In your Ubuntu terminal, type `cd` then `vim .bashrc`
2. Press `i` to enter *insert mode*, which will allow you to edit the file
3. Use the arrow keys to navigate to the bottom of the file, then add the line `export PATH="/home/user/.local/bin:$PATH"` where `user` is the username of your Ubuntu unix profile
4. Press `ESC` then type `:wq` to *write* your changes and *quit* from the VIM editor
5. Restart the Ubuntu 22.04 LTS application (close and re-open)