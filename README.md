# minecraft-cli
A command line interface for creating minecraft servers on linux

## What can this do?
- You can manage servers using systemd easily. To create a server, write `minecraft-cli create testServer1` and follow the on-screen instructions. (Downloads the correct server.jar file and allows you to choose version)
- You can easily set servers to autostart and autorestart with `minecraft-cli enable testServer1`
- You can access the console by running `minecraft-cli console testServer1`
- You can open the server.properties with `minecraft-cli modify testServer1`
- You can easily cd into the server's folder with `minecraft-cli cd testServer1`

## Setup:
Currently there's no easy way to set this up. In short:

- You need to have python 3.6 or later, and pip for python 3.6 (or the python version you use)
- You need the requests library: `pip3 install requests`
- You need to have `screen` installed
- You need a user called 'minecraft' (not a sudoer)
- You need a folder at `/opt/minecraft-servers` owned by `minecraft:minecraft` (`chown minecraft:minecraft /opt/minecraft-servers`)
- You need to add a symlink from `./minecraft-server@.service` to `/etc/systemd/system/minecraft-server@.service` (let systemd do it: `sudo systemctl link $PWD/minecraft-service@.service`)
- You need to add a symlink from `./minecraft-cli.py` to `/usr/bin/minecraft-cli` (`ln -s minecraft-cli.py /usr/bin/minecraft-cli`)
- Make sure that the file `./minecraft-cli.py` has the `x` permission so that you can run it
- You need to have some text editor at `/usr/bin/editor` (should be done automatically)
- You need to be able to use an interactive prompt (uses python's input function, so if your shell doesn't support that, use another shell)

### In even shorter:
- Install `python3.6` or later, `git` and `screen`. Make sure that you have pip3 installed too.
  On ubuntu-server 18.04 you can run `sudo apt update && sudo apt install python3.6 python3-pip screen git` to install those packages.
- Make sure that the `/usr/bin/editor` is a text editor.

- After that, run these commands:
```bash
$ pip3 install requests
$ git clone https://github.com/alvesvaren/minecraft-cli.git
$ cd minecraft-cli
$ sudo adduser minecraft
$ sudo mkdir /opt/minecraft-servers
$ sudo chown minecraft:minecraft /opt/minecraft-servers
$ sudo ln -s minecraft-cli.py /usr/bin/minecraft-cli
$ sudo systemctl link $PWD/minecraft-server@.service
$ chmod +x minecraft-cli.py
```

- Now this should be installed correctly. Try `minecraft-cli test` to make a test-server, start it, stop it and then remove it.

## TODO-list:
- Add some sort of backup system (both automatic as a service and manually)
- Improve the code so that it doesn't look as ugly as it does right now
- Add some sort of setup script that does the setup for you
- Add support for custom .jars
- Add support for buildtools (spigot, craftbukkit and paper)
- Add a custom status command, to see online players, tps etc.
- Add more options to the creation interface (like port settings and spawn protection)
