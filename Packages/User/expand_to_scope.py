import sublime
import sublime_plugin
from collections import defaultdict

#scopes for braces
# source.c++ meta.namespace.c++ meta.function.c++ meta.block.c++ meta.block.c++ 
# punctuation.definition.block.end.c++ 
# meta.block.c++ 

class my_expand_to_scope(sublime_plugin.TextCommand):
	def run(self, edit):
		if self.view.sel().__len__() > 1:
			return; #this command only works for one selection
		
		
		view = self.view;
		
		"""
		first_sel     = self.view.sel()[0];
		print ("Prev sel is (%d, %d)" % (first_sel.a, first_sel.b));
		first_sel     = self.view.sel()[0];
		print ("Next sel is (%d, %d)" % (first_sel.a, first_sel.b));
		"""
		
		first_sel = None;
		first_pos = None;
		for i in range(0, 5):
			#nonlocal first_sel, first_pos;
			prev_sel = self.view.sel()[0];
			view.run_command("expand_selection", {"to": "scope"});
			first_sel = self.view.sel()[0];
			first_pos = first_sel.begin();
			first_word = view.substr(first_pos);
			if (prev_sel.begin() != first_pos) and (first_word == "{"):
				break;
		
		if first_sel.b != first_pos:
			new_region = sublime.Region(first_sel.b, first_sel.a);
			self.view.sel().clear();
			self.view.sel().add(new_region);
		self.view.show(first_pos, show_surrounds=True, keep_to_left=True, animate=True);
			
				

			