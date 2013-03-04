import sublime
import sublime_plugin

# assume sidebar is visible by default on every window (there's no way to check, unfortunately)
DEFAULT_VISIBILITY = True

sidebar_visible = DEFAULT_VISIBILITY
lastActive = None

# Keep track of active windows so we rememeber sidebar_visible for each one
windows = {}


class SideBarListener(sublime_plugin.EventListener):

    def on_activated(self, view):
        global sidebar_visible, lastActive
        active = view.window()

        if not active:
            return

        if not active.id() in windows:
            # first activation in this window, use default
            windows[active.id()] = DEFAULT_VISIBILITY

        if lastActive == None:
            # plugin just loaded
            lastActive = active
        elif lastActive != active:
            # store the old window state
            windows[lastActive.id()] = sidebar_visible
            # load the new window state
            sidebar_visible = windows[active.id()]
            lastActive = active

        if sidebar_visible and view.settings().get('reveal-on-activate') != False:
            active.run_command('reveal_in_side_bar')

    # Sublime text v3 window command listener, safe to include unconditionally as it's simply ignored by v2.
    def on_window_command(self, window, command_name, args):
        global sidebar_visible
        if command_name == "toggle_side_bar":
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
