#!/usr/bin/python3
import argparse
import os
import requests

base_path = "/opt/minecraft-servers/"

parser = argparse.ArgumentParser(description="Minecraft command line interface", prog="minecrat-cmi")
parser.add_argument("action", type=str, help="The action to run.", choices=["create", "remove", "enable", "restart", "backup", "start", "stop", "status", "modify", "cd", "console"])
parser.add_argument("server", type=str, help="The name of the server to run action on.")
args = parser.parse_args()

os.chdir(base_path)

if args.action == "create":
    print(f"Started creation of server {args.server}")
    folder = base_path + args.server
    os.mkdir(folder)
    print(f"Created server folder at {folder}")
    os.chdir(folder)
    print("Changed working directory to server folder")
    print()
    answer = input("Would you like to use vanilla? (Y/n): ").lower()
    if "y" in answer or not answer:
        print("Creating vanilla server")
        print("Fetching version info...", end="")
        manifest = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").json()
        print("DONE!")
        print()
        wanted_version = input(f"What version would you like to use? ({manifest['latest']['release']}): ").strip()
        if not wanted_version:
            wanted_version = manifest['latest']['release']
        print(f"You selected {wanted_version}")
        print(f"Finding manifest for that version")
        version_info_url = ""
        for version in manifest['versions']:
            if version["id"] == wanted_version:
                print(f"Found manifest url: {version['url']}")
                version_info_url = version['url']
                print(f"Server version is of type '{version['type']}'")
                break
        if not version_info_url:
            print("Did not find that manifest. Try again with another version")
            quit(1)
        server_binary_url = requests.get(version_info_url).json()["downloads"]["server"]["url"]
        print(f"Server binary url found at {server_binary_url}")
        print("Downloading...", end="")
        with open("server.jar", "wb") as file:
            file.write(requests.get(server_binary_url, allow_redirects=True).content)
        print("DONE!")
        print("Server file written to server.jar")
        print("Running first time setup (creating files)...", end="")
        os.system("java -jar server.jar > /dev/null")
        print("DONE!")
        with open("eula.txt", "w") as file:
            file.write("eula=true\n")
            print("Accepted eula. (read https://minecraft.net/eula/)")
    else:
        print("This is not supported yet!")
        quit(1)
    print()
    print("Server creation done!")
    print(f"Start and enable the server using 'systemctl enable --now minecraft-server@{args.server}'")
elif args.action == "remove":
    confirmation = input(f"Are you sure that you want to remove {args.server}? (y/N): ").lower()
    if confirmation == "y" or confirmation == "yes":
        folder = base_path + args.server
        print(f"This will remove the folder {folder}")
        confirmation2 = input(f"Continue? (y/N): ").lower()
        if confirmation2 == "y" or confirmation2 == "yes":
            print("Removing server folder...")
            os.system(f"rm -r {folder}")
elif args.action == "enable":
    print(f"This will enable and start the service 'minecraft-server@{args.server}'")
    confirmation = input("Continue? (Y/n): ").lower()
    if "y" in confirmation or not confirmation:
        print(f"Enabling and starting the server {args.server}")
        os.system("systemctl enable --now minecraft-server@{args.server}")
elif args.action == "restart":
    print("This will save all worlds and restart the server")
    confirmation = input("Continue? (Y/n): ").lower()
    if "y" in confirmation or not confirmation:
        print(f"Restarting {args.server} in 5 seconds...", end="")
        os.system(f"systemctl restart minecraft-server@{args.server}")
        print("DONE!")
elif args.action == "status":
    print(f"Service status for minecraft-server@{args.server}:")
    os.system(f"systemctl status minecraft-server@{args.server}")
elif args.action == "cd":
    print("Changing directory to the server folder...", end="")
    os.system(f"cd {base_path + args.server}")
    print("DONE!")
elif args.action == "modify":
    print("Opening the server.properties file with your default editor")
    os.system(f"/usr/bin/editor {base_path + args.server}/server.properties")
elif args.action == "start":
    print("This will temporarily start the server until you stop it. To enable automatic restarts use the enable action instead.")
    confirmation = input("Continue? (Y/n): ").lower()
    if "y" in confirmation or not confirmation:
        print(f"Starting {args.server}...")
        os.system(f"systemctl start minecraft-server@{args.server}")
        print("DONE!")
elif args.action == "disable":
    print("This will disable auto start and auto restart on the server")
    confirmation = input("Continue? (y/N): ").lower()
    if confirmation == "y" or confirmation == "yes":
        print(f"Disabling minecraft-server@{args.server}..")
        os.system(f"systemctl disable minecraft-server@{args.server}")
        print("DONE!")
elif args.action == "stop":
    print("This will stop the server until you start it or, if the server is enabled, you restart the system")
    confirmation = input("Continue? (y/N): ").lower()
    if confirmation == "y" or confirmation == "yes":
        print(f"Stopping {args.server} in 5 seconds...")
        os.system(f"systemctl stop minecraft-server@{args.server}")
elif args.action == "console":
    print("This will attach you to the screen of the server. TO RETURN: Press Ctrl+A followed by Ctrl+D.")
    print("Ensure that you are running this as the correct user (the same one that is entered in the system service file, default is 'minecraft')")
    confirmation = input("Continue? (Y/n): ").lower()
    if "y" in confirmation or not confirmation:
        os.system(f"screen -Dr mc-{args.server}")
elif args.action == "backup":
    raise NotImplementedError("Backups will work in a later release")