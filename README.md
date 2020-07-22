![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)
<!-- [![](https://www.paypalobjects.com/en_US/i/btn/x-click-but04.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=JM8FUXNFUK6EU) -->
[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=JM8FUXNFUK6EU)

# tuxdrive

##### Table of Contents

1. [Introduction](#introduction)
2. [Project Details](#project-details)
3. [Installation](#installation)
4. [Usage](#usage)
5. [License](#license)

## Introduction

`tuxdrive` is a console based DIY google drive client.

![Logo](https://raw.githubusercontent.com/prahladyeri/tuxdrive/master/logo_small.jpg)


## Project Details

- Home Page: [https://prahladyeri.github.io/tuxdrive/](https://prahladyeri.github.io/tuxdrive/)
- Lead Developer: [Prahlad Yeri](https://github.com/prahladyeri)
- Issue tracker: [https://github.com/prahladyeri/tuxdrive/issues](https://github.com/prahladyeri/tuxdrive/issues)
<!-- - Discussion Room: [https://www.reddit.com/r/tuxdrive](https://www.reddit.com/r/tuxdrive) -->

## Installation

	pip install tuxdrive


Since this is a DIY (Do-it-yourself) app, you'll have to register your own app by going to the [Google API Console](https://console.cloud.google.com/?pli=1), enable Drive API, create credentials and copy the `client_id.json` to your working folder. Only then the program will be able to work. For more information on how to do this, you may [refer to this article](https://prahladyeri.com/blog/2016/12/how-to-create-google-drive-app-python-flask.html).

(Note: As of version 2.0.0, `pip` is the only supported installation method, the old DEB/RPM method is depreciated)

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
mkdir: Create a directory on remote path.
list permissions <item>: Lists the permissions on specific file/directory.
clear permissions <item>: Clears permissions on specific file/directory.
share <item>: Shares the specific file/directory in remote drive publicly.
share <item> <email>: Shares the specific file/directory in remote drive to specified email.
exit: Exits this program.
rdcache: Show remote directory mapping of id and folder paths.
rfcache: Show remote files mapping of id and folder paths.


## Documentation

tuxdrive is under active development, so there is no extensive documentation. I'll keep updating the github wiki as and when I get time.

## License

`tuxdrive` is free and open source software. It is [MIT](https://opensource.org/licenses/MIT) licensed.

