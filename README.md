SyncedSideBar
=============

[Sublime Text 2](http://www.sublimetext.com/) plugin to sync project sidebar
(folder view) with currently active file.

Sublime Text 2 highlights only those files that are already expanded. This plugin highlights all files (eg. opened with cmd+p).

Figured out by Mylith at sublimetext.com forum.
http://www.sublimetext.com/forum/viewtopic.php?f=2&t=4080

Usage
-----

#### Note

This plugin works on both Sublime Text 2 and Sublime Text 3 beta. None of the APIs this plugin uses changed between releases.

When running on Sublime Text 3 beta, the plugin is able track the sidebar visibility (but only when the keyboard shortcut for "toggle_side_bar" is used, not the view -> sidebar toggle). It still forces the sidebar to become visible the first time a window is activated, but after that the plugin will detect when the keyboard shortcut is used and stop calling "reveal_in_side_bar" until it is used again. It will even remember the visible state when multiple windows are open.

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

