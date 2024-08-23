import sublime
import sublime_plugin


search_initiated_in_reverse = False
starting_scroll_pos = None
starting_sel = None

class fsearch_begin(sublime_plugin.TextCommand):
	def run(self, edit):
		global starting_sel, starting_scroll_pos, search_initiated_in_reverse
		search_initiated_in_reverse = False
		starting_sel = self.view.sel()[0];
		starting_scroll_pos = self.view.viewport_position();
		# print ("starting pos is %d,%d" % (starting_sel.a, starting_sel.b))
		self.view.window().run_command("show_panel", {"panel": "find", "reverse" : False}) 

class rsearch_begin(sublime_plugin.TextCommand):
	def run(self, edit):
		global starting_sel, starting_scroll_pos, search_initiated_in_reverse
		search_initiated_in_reverse = True
		starting_sel = self.view.sel()[0];
		starting_scroll_pos = self.view.viewport_position();
		# print ("starting pos is %d,%d" % (starting_sel.a, starting_sel.b))
		self.view.window().run_command("show_panel", {"panel": "find", "reverse" : True}) 

class isearch_next_match(sublime_plugin.TextCommand):
	def run(self, edit):
		if search_initiated_in_reverse:
			self.view.window().run_command("find_prev") 
		else:
			self.view.window().run_command("find_next") 

class isearch_prev_match(sublime_plugin.TextCommand):
	def run(self, edit):
		if search_initiated_in_reverse:
			self.view.window().run_command("find_next") 
		else:
			self.view.window().run_command("find_prev") 


class isearch_escape(sublime_plugin.WindowCommand):
	def run(self):
		global starting_sel, starting_scroll_pos
		view = self.window.active_view()

		self.window.run_command("hide_panel") 
		
		# print ("starting pos on exit is %d,%d" % (starting_sel.a, starting_sel.b))
		# print ("init cursor pos is %d,%d" % (view.sel()[0].a, view.sel()[0].b))
		
		view.sel().clear() 
		view.sel().add(starting_sel)
		view.set_viewport_position(starting_scroll_pos, True)


		# print ("new  cursor pos is %d,%d" % (view.sel()[0].a, view.sel()[0].b))