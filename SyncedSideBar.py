import sublime
import sublime_plugin


def get_settings_value(key):
    settings = sublime.load_settings(__name__ + '.sublime-settings')
    return settings.get(key)


class SideBarListener(sublime_plugin.EventListener):

    def on_activated(self, view):
        active = view.window()
        if active and get_settings_value('reveal-on-activate'):
            active.run_command('reveal_in_side_bar')
