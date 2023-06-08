# pyright: reportMissingImports=false

import fnmatch

import sublime
import sublime_plugin

# ++++ old hacks ++++
# before ST3 build 3098 we assume sidebar is visible by default on every window
# (there's no way to check, unfortunately)
DEFAULT_VISIBILITY = True
sidebarVisible = DEFAULT_VISIBILITY

# Keep track of active windows so we remember sidebarVisible for each one
lastWindow = None
# ++++ end old hacks ++++

# Used to know whether we've run reveal_all for a window
windows = {}

# preference from plugin settings file
pluginPref = DEFAULT_VISIBILITY

# List of file patterns to ignore when revealing a tab in the sidebar
pluginPatterns = []

# flag for alt-tab focus check
lastView = None

PACKAGE_SETTINGS = 'SyncedSideBar.sublime-settings'
USER_SETTINGS    = 'Preferences.sublime-settings'

def plugin_loaded():
    userSettings = sublime.load_settings(USER_SETTINGS)
    packageSettings = sublime.load_settings(PACKAGE_SETTINGS)

    def read_pref_user():
        vis = userSettings.get('reveal-on-activate')
        if vis is not None:
            global pluginPref
            pluginPref = vis

        ignores = userSettings.get('reveal-ignore-patterns')
        if ignores:
            global pluginPatterns
            pluginPatterns = ignores

    def read_pref_package():
        vis = packageSettings.get('reveal-on-activate')
        if vis is not None:
            global pluginPref
            pluginPref = vis

        ignores = packageSettings.get('reveal-ignore-patterns')
        if ignores:
            global pluginPatterns
            pluginPatterns = ignores

    # read initial setting
    read_pref_package()
    read_pref_user()

    # listen for changes
    userSettings.add_on_change('Preferences', read_pref_user)
    packageSettings.add_on_change('SyncedSideBar', read_pref_package)


# ST2 backwards compatibility
if (int(sublime.version()) < 3000):
    plugin_loaded()

def reveal_all(view):
    visUser = view.settings().get('reveal-all-tabs')

    if visUser is None:
        packageSettings = sublime.load_settings(PACKAGE_SETTINGS)
        visPackage = packageSettings.get('reveal-all-tabs')
        if visPackage is False:
            return
    elif visUser is False:
        return

    activeWindow = view.window()
    viewList = activeWindow.views()

    # Use set_timeout to give sublime a chance to fire normal events
    # between tab changes
    def reveal():
        if viewList:
            target = viewList.pop()
            activeWindow.focus_view(target)
            sublime.set_timeout(reveal, 25)
        else:
            # all tabs have been activated in this window, restore focus to the
            # tab that was first active
            activeWindow.focus_view(view)
    sublime.set_timeout(reveal, 50)


def manage_state(view):
    activeWindow = view.window()

    if activeWindow.id() not in windows:
        # first activation in this window, use default (unused for 3098
        # and above, but we need to store *something*)
        windows[activeWindow.id()] = DEFAULT_VISIBILITY

        # fire 'reveal all' in the background
        reveal_all(view)

    # ++++ old hacks ++++
    if (int(sublime.version()) < 3098):
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
    # ++++ end old hacks ++++


def show_view(view):
    userPref = view.settings().get('reveal-on-activate')
    reveal = userPref if userPref is not None else pluginPref

    userPatterns = view.settings().get('reveal-ignore-patterns')
    patterns = userPatterns if userPatterns else pluginPatterns

    activeWindow = view.window()

    def revealLater():
        activeView = activeWindow.active_view()

        if activeView:
            filename = activeView.file_name()

            if not filename:
                return

            # Some versions of Sublime Text crash when revealing files
            # under `.git/` in the side bar:
            # https://github.com/sublimehq/sublime_text/issues/5881
            if int(sublime.version()) < 4148 and '/.git/' in filename:
                return

            if any(fnmatch.fnmatch(filename, pattern) for pattern in patterns):
                return

        if (int(sublime.version()) >= 3098):
            # API provided by sublime
            shouldReveal = activeWindow.is_sidebar_visible()
        else:
            # backwards compatibility
            shouldReveal = sidebarVisible

        if shouldReveal and reveal is not False:
            activeWindow.run_command('reveal_in_side_bar')

    # When using quick switch project, the view activates before the sidebar
    # is ready. This tiny delay is imperceptible but works around the issue.
    sublime.set_timeout(revealLater, 100)


class SideBarListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        # don't even consider updating state if we don't have a window.
        # reveal in side bar is a window command only.
        # 'goto anything' activates views but doesn't set a window
        # until the file is selected.
        if view.settings().get("is_widget", False):
            return

        global lastView
        if lastView is not None and lastView.id() == view.id():
            # this view has just been processed, likely an alt-tab focus event
            return
        lastView = view

        manage_state(view)
        show_view(view)

    # Sublime text v3 window command listener, safe to include unconditionally
    # as it's simply ignored by v2. Eventually, v3 support
    # below 3098 will be dropped and this can be deleted.
    def on_window_command(self, window, command, _):
        if command == 'toggle_side_bar' and window.is_valid():
            global sidebarVisible
            sidebarVisible = not sidebarVisible

    def on_post_window_command(self, window, command, _):
        # v4 leaves focus on the sidebar after a `reveal_in_side_bar` command
        # So we need to manually force focus back to the file window
        if (int(sublime.version()) > 4000 and int(sublime.version()) < 4099):
            if command == 'reveal_in_side_bar' and window.is_valid():
                window.focus_view(lastView)


class SideBarUpdateSync(sublime_plugin.ApplicationCommand):
    # Update user preferences with the new value
    def run(self, enable):
        userSettings = sublime.load_settings(USER_SETTINGS)
        vis = userSettings.get('reveal-on-activate')
        if vis is not None:
            userSettings.set('reveal-on-activate', enable)
            sublime.save_settings(USER_SETTINGS)
        else:
            packageSettings = sublime.load_settings(PACKAGE_SETTINGS)
            packageSettings.set('reveal-on-activate', enable)
            sublime.save_settings(PACKAGE_SETTINGS)
