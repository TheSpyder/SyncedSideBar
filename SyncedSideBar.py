import sublime
import sublime_plugin

# ++++ old hacks ++++
# before ST3 build 3098 we assume sidebar is visible by default on every window (there's no way to check, unfortunately)
DEFAULT_VISIBILITY = True
sidebarVisible = DEFAULT_VISIBILITY

# Keep track of active windows so we remember sidebarVisible for each one
lastWindow = None
# ++++ end old hacks ++++

# Used to know whether we've run reveal_all for a window
windows = {}

# preference from plugin settings file
pluginPref = DEFAULT_VISIBILITY

# flag for alt-tab focus check
lastView = None

def plugin_loaded():
    userSettings    = sublime.load_settings('Preferences.sublime-settings')
    packageSettings = sublime.load_settings('SyncedSideBar.sublime-settings')

    def read_pref_user():
        vis = userSettings.get('reveal-on-activate')
        if vis is not None:
            global pluginPref
            pluginPref = vis

    def read_pref_package():
        vis = packageSettings.get('reveal-on-activate')
        if vis is not None:
            global pluginPref
            pluginPref = vis

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
    #print( 'view.settings().get(reveal-all-tabs): ' + str( visUser ) )
    if visUser is False:
        return
    
    packageSettings = sublime.load_settings('SyncedSideBar.sublime-settings')
    visPackage      = packageSettings.get('reveal-all-tabs')
    if visPackage is False:
        return
    
    activeWindow = view.window();
    viewList     = activeWindow.views();
    
    # Use set_timeout to give sublime a chance to fire normal events between tab changes
    def reveal():
        if (len(viewList) > 0):
            target = viewList.pop()
            activeWindow.focus_view(target)
            sublime.set_timeout(reveal, 25);
        else:
            # all tabs have been activated in this window, restore focus to the tab that was first active
            activeWindow.focus_view(view)
    sublime.set_timeout(reveal, 50);


def manage_state(view):
    activeWindow = view.window()

    if not activeWindow.id() in windows:
        # first activation in this window, use default (unused for 3098 and above, but we need to store *something*)
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

    win = view.window()

    # backwards compatibility
    if (int(sublime.version()) >= 3098):
        shouldReveal = win.is_sidebar_visible()
    else:
        shouldReveal = sidebarVisible

    if shouldReveal and reveal != False:
        def reveal():
            win.run_command('reveal_in_side_bar')

        # When using quick switch project, the view activates before the sidebar is ready.
        # This tiny delay is imperceptible but works around the issue.
        sublime.set_timeout(reveal, 100);


class SideBarListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        # don't even consider updating state if we don't have a window.
        # reveal in side bar is a window command only.
        # 'goto anything' activates views but doesn't set a window until the file is selected.
        if not view.window():
            return

        global lastView
        if lastView is not None and lastView.id() == view.id():
            # this view has just been processed, likely an alt-tab focus event
            return
        lastView = view

        manage_state(view)
        show_view(view)


    # Sublime text v3 window command listener, safe to include unconditionally as it's simply ignored by v2.
    # Eventually, v3 support below 3098 will be dropped and this can be deleted.
    def on_window_command(self, window, command_name, args):
        if command_name == 'toggle_side_bar':
            global sidebarVisible
            sidebarVisible = not sidebarVisible


class SideBarUpdateSync(sublime_plugin.ApplicationCommand):
    # Update user preferences with the new value
    def run(self, enable):
        userSettings = sublime.load_settings('Preferences.sublime-settings')
        vis          = userSettings.get('reveal-on-activate')
        if vis is not None:
            userSettings.set('reveal-on-activate', enable)
            sublime.save_settings('Preferences.sublime-settings')
        else:
            packageSettings = sublime.load_settings('SyncedSideBar.sublime-settings')
            vis             = packageSettings.get('reveal-on-activate')
            packageSettings.set('reveal-on-activate', enable)
            sublime.save_settings('SyncedSideBar.sublime-settings')


