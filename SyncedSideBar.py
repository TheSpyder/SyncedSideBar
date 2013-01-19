import sublime
import sublime_plugin


class SideBarListener(sublime_plugin.EventListener):

    def on_activated(self, view):
        active = view.window()
        if active and view.settings().get('reveal-on-activate') != False:
            active.run_command('reveal_in_side_bar')


class SideBarEnableSync(sublime_plugin.ApplicationCommand):

    def run(self):
        # Load in user settings
        settings = sublime.load_settings("Preferences.sublime-settings")

        # Update the setting
        settings.set("reveal-on-activate", True)

        # Save our changes
        sublime.save_settings("Preferences.sublime-settings")
