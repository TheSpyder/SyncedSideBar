import sublime
import sublime_plugin

# assume sidebar is visible by default on every window (there's no way to check, unfortunately)
DEFAULT_VISIBILITY = True
sidebarVisible = DEFAULT_VISIBILITY

# preference from plugin settings file
pluginPref = DEFAULT_VISIBILITY

# flag for alt-tab focus check
lastView = None

# Keep track of active windows so we remember sidebarVisible for each one
lastWindow = None
windows = {}

def plugin_loaded():
    s = sublime.load_settings('SyncedSideBar.sublime-settings')

    def read_pref():
        vis = s.get('reveal-on-activate')
        if vis is not None:
            global pluginPref
            pluginPref = vis

    # read initial setting
    read_pref()
    # listen for changes
    s.add_on_change("SyncedSideBar", read_pref)

# ST2 backwards compatibility
if (int(sublime.version()) < 3000):
    plugin_loaded()


def manage_state(view):
    activeWindow = view.window()

    if not activeWindow.id() in windows:
        # first activation in this window, use default
        windows[activeWindow.id()] = DEFAULT_VISIBILITY

    global sidebarVisible, lastWindow
    if lastWindow is None:
        # plugin just loaded
        lastWindow = activeWindow
    elif lastWindow.id() != activeWindow.id():
        # store the old window state
        windows[lastWindow.id()] = sidebarVisible
        # load the new window state
        sidebarVisible = windows[activeWindow.id()]
        lastWindow = activeWindow


def show_view(view):
    userPref = view.settings().get('reveal-on-activate')
    reveal = userPref if userPref is not None else pluginPref

    if sidebarVisible and reveal != False:
        win = view.window()
        def reveal():
            win.run_command('reveal_in_side_bar')

        # When using quick switch project, the view activates before the sidebar is ready.
        # This tiny delay is imperceptible but works around the issue.
        sublime.set_timeout(reveal, 100);


class SideBarListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        # don't even consider updating state if we don't have a window.
        # reveal in side bar is a window command only.
        # "goto anything" activates views but doesn't set a window until the file is selected.
        if not view.window():
            return

        global lastView
        if lastView is not None and lastView.id() == view.id():
            # this view has already been processed, likely an alt-tab focus event
            return
        lastView = view

        manage_state(view)
        show_view(view)


    # Sublime text v3 window command listener, safe to include unconditionally as it's simply ignored by v2.
    def on_window_command(self, window, command_name, args):
        if command_name == "toggle_side_bar":
            global sidebarVisible
            sidebarVisible = not sidebarVisible


class SideBarUpdateSync(sublime_plugin.ApplicationCommand):
    # Update user preferences with the new value
    def run(self, enable):
        settings = sublime.load_settings("Preferences.sublime-settings")
        settings.set("reveal-on-activate", enable)
        sublime.save_settings("Preferences.sublime-settings")
