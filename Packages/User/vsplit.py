import sublime
import sublime_plugin

class vsplit(sublime_plugin.TextCommand):
	def run(self, edit):
		filename = self.view.file_name();
		if filename is not None:
			first_sel = self.view.sel()[0];
			window = sublime.active_window();
			new_view = window.open_file(filename, sublime.ADD_TO_SELECTION, -1);
			
			new_region = sublime.Region(first_sel.b, first_sel.b);
			new_view.sel().clear();
			new_view.sel().add(new_region);
			new_view.show(first_sel.a, show_surrounds=True, keep_to_left=True, animate=False);