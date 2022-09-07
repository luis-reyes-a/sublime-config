import sublime
import sublime_plugin

class cursor_mark_swap(sublime_plugin.TextCommand):
	def run(self, edit):
		selections = self.view.sel()
		if selections.__len__() > 1:
			return;
			
		first_sel = selections[0];
		if first_sel.a == first_sel.b:
			return;
			
		print("swap marks");
		#first_sel.a, first_sel.b = first_sel.b, first_sel.a;
		#sublime.run_command("show_at_center");
		
		new_region = sublime.Region(first_sel.b, first_sel.a);
		self.view.sel().clear();
		self.view.sel().add(new_region);
		self.view.show(first_sel.a, show_surrounds=True, keep_to_left=True, animate=True);