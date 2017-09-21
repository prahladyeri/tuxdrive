![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)
[![](https://www.paypalobjects.com/en_US/i/btn/x-click-but04.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=JM8FUXNFUK6EU)

# tuxdrive

##### Table of Contents

1. [Introduction](#introduction)
2. [Project Details](#project-details)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Contribution](#contribution)
6. [Donation](#donation)
7. [License](#license)

## Introduction

`tuxdrive` is a console based google drive client for Linux.

![Logo](https://raw.githubusercontent.com/prahladyeri/tuxdrive/master/logo_small.jpg)


## Project Details

- Lead Developer: [Prahlad Yeri](https://github.com/prahladyeri)
- Governance: Meritocracy.
- Issue tracker: [https://github.com/prahladyeri/tuxdrive/issues](https://github.com/prahladyeri/tuxdrive/issues)
- Discussion Room: [https://www.reddit.com/r/tuxdrive](https://www.reddit.com/r/tuxdrive)

## Installation

As a pre-requisite, you should have `python3` and `google-api-python-client` package installed through `pip3` or something:

	sudo pip3 install google-api-python-client

Then, just download the [latest `.DEB`](https://github.com/prahladyeri/tuxdrive/releases/latest) package and run the following command.

    sudo dpkg -i tuxdrive.deb
    
An alternative/manual way of installing is to just download the `tuxdrive` python source file from master branch and copy it to a folder on your machine. But then, you'll have to register your own app by going to the [Google API Console](https://console.cloud.google.com/?pli=1), enable Drive API, create credentials and copy the `client_id.json` to your `/etc/tuxdrive` folder. Only then the program will be able to work.

## Usage

`tuxdrive` has a command line interface to the google drive interface similar to traditional unix tools like `ftp` and `sftp` (though not as extensive and comprehensive yet!).

Once you start `tuxdrive` program, it will give you a `tux_drive>` prompt from which you can run the above commands. When you run `tuxdrive` the first time, it will open up the browser window and ask for permissions to access your google drive on your behalf. After that, you can start running commands. You can list your drive files using `ls` or `dir` command for example:

![Screenshot](https://github.com/prahladyeri/tuxdrive/raw/master/screenshot.png)


Similarly, you can run `push some_local_file.txt` to upload it to your drive, or `rcd my_drive_folder` to change the remote drive. Here is the entire command list:

	help (or ?): Shows this help facility.
	dir (or ls): Lists all files and folders on drive.
	!dir (or !ls): Lists all files and folders in current directory.
	get (or pull) <item>: Pulls the named file/folder from drive to current working directory.
	put (or push) <item>: Pushes the named file/folder from current working directory to drive.
	rm <item>: Delete the named file/folder on remote path.
	pwd: Print working directory (remote/drive).
	cd: Change working directory (remote/drive).
	lpwd: Print working directory (local).
	lcd: Change working directory (local).
	rdcache: Show remote directory mapping of id and folder paths.
	rfcache: Show remote files mapping of id and folder paths.
	mkdir: Create a directory on remote path.
	exit: Exits this program.

## Documentation

tuxdrive is under active development, so there is no extensive documentation. I'll keep updating the github wiki as and when I get time.

## Contribution

I'm presently looking for people who can contribute in the following ways:

1. Testing: Extensive user testing with feedback.
2. Code review: There is no such thing as bug-free code and more the number of eyeballs, the better it is.
3. Logo Design: The present logo is a bit hastily patched up, it would be great if you can design for me a new logo for this project!

## Donation


| Paypal | Bitcoin |
| ------ | ------- |
| [![](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=JM8FUXNFUK6EU) |  1Av4rPGBz5rJVPwewSTDCpYac1rjvkaSzT |


## License

`tuxdrive` is free and open source, and it always will be. It is licensed under the [MIT](https://opensource.org/licenses/MIT).

