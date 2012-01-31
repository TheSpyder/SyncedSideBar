import sublime
import sublime_plugin

class SideBarListener(sublime_plugin.EventListener):
    
    def on_activated(self, view):
        view.window().run_command('reveal_in_side_bar')

