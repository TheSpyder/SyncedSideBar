SyncedSideBar
=============

[Sublime Text 2](http://www.sublimetext.com/) plugin to sync project sidebar
(folder view) with currently active file.

Sublime Text 2 highlights only those files that are already expanded. This plugin highlights all files (eg. opened with cmd+p).

Figured out by Mylith at sublimetext.com forum.
http://www.sublimetext.com/forum/viewtopic.php?f=2&t=4080

Usage
-----

### Configuration

SyncedSideBar enables/disables automatic syncing via the setting `reveal-on-activate`.

If `true`, syncing will automatically happen. If `false`, syncing will be disabled.

Helper commands for enabling/disabling automatic syncing are available as 'Side Bar: Enable Sync' and 'Side Bar: Disable Sync'.

This can be found in the Command Palette (Command+Shift+P on Mac, Ctrl+Shift+P on Linux/Windows).

### Manually reveal files

Files can be manually revealed via the command 'Side Bar: Reveal File'.

This can be found in the Command Palette (Command+Shift+P on Mac, Ctrl+Shift+P on Linux/Windows).

Installation
------------

### Using Package control

This plugin is available through [Package Control](http://wbond.net/sublime_packages/package_control),
which is the easiest way to install it.

### Manual installation

Go to your Packages subdirectory under Sublime Text 2 data directory:

* Windows: %APPDATA%\Sublime Text 2
* OS X: ~/Library/Application Support/Sublime Text 2
* Linux: ~/.config/sublime-text-2

Then clone this repository:

    git clone git://github.com/sobstel/SyncedSideBar

