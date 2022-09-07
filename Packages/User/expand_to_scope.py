import sublime
import sublime_plugin
from collections import defaultdict

#scopes for braces
# source.c++ meta.namespace.c++ meta.function.c++ meta.block.c++ meta.block.c++ 
# punctuation.definition.block.end.c++ 
# meta.block.c++ 

class my_expand_to_scope(sublime_plugin.TextCommand):
	def run(self, edit):
		print("Need sublime version 4130 in order to do this command!\n");

""" NOTE this requires sublime version 4130 (which is a dev build at the moment)
class my_expand_to_scope(sublime_plugin.TextCommand):
	def run(self, edit):
		print("Hello there");
		selections = self.view.sel();
		if selections.__len__() > 1:
			print("Can only expand with 0 or 1 selections active\n");
			return; 
		
		print(selections.__len__());
		selection = selections[0];
		region = self.view.expand_to_scope(selection.begin(), 'punctuation.definition.block');
		if region:
			selection = region;
"""
			