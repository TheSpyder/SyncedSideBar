import sublime
import sublime_plugin

# assume sidebar is visible by default on every window (there's no way to check, unfortunately)
DEFAULT_VISIBILITY = True

sidebar_visible = DEFAULT_VISIBILITY
lastWindow = None
lastView = None

# Keep track of active windows so we rememeber sidebar_visible for each one
windows = {}


class SideBarListener(sublime_plugin.EventListener):

    def on_activated(self, view):
        global lastView
        if lastView is not None and lastView.id() == view.id():
            # this view has already been processed, likely an alt-tab focus event
            return
        lastView = view

        global sidebar_visible, lastWindow
        activeWindow = view.window()

        if not activeWindow:
            return

        if not activeWindow.id() in windows:
            # first activation in this window, use default
            windows[activeWindow.id()] = DEFAULT_VISIBILITY

        if lastWindow is None:
            # plugin just loaded
            lastWindow = activeWindow
        elif lastWindow.id() != activeWindow.id():
            # store the old window state
            windows[lastWindow.id()] = sidebar_visible
            # load the new window state
            sidebar_visible = windows[activeWindow.id()]
            lastWindow = activeWindow

        if sidebar_visible and view.settings().get('reveal-on-activate') != False:
            activeWindow.run_command('reveal_in_side_bar')

    # Sublime text v3 window command listener, safe to include unconditionally as it's simply ignored by v2.
    def on_window_command(self, window, command_name, args):
        if command_name == "toggle_side_bar":
            global sidebar_visible
            sidebar_visible = not sidebar_visible


class SideBarUpdateSync(sublime_plugin.ApplicationCommand):

    def run(self):
        pass

    def updateSync(self, value):
        # Load in user settings
        settings = sublime.load_settings("Preferences.sublime-settings")

        # Update the setting
        settings.set("reveal-on-activate", value)

        # Save our changes
        sublime.save_settings("Preferences.sublime-settings")


class SideBarEnableSync(SideBarUpdateSync):

    def run(self):
        self.updateSync(True)


class SideBarDisableSync(SideBarUpdateSync):

    def run(self):
        self.updateSync(False)
