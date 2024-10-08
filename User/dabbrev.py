import sublime
import sublime_plugin
import re

resample_word_again = True;
next_option_index = 1;
options = [];

class dabbrev(sublime_plugin.TextCommand):
	def run(self, edit):
		global resample_word_again, next_option_index, options, sample_region;
		first_sel     = self.view.sel()[0];
		sample_region = self.view.word(first_sel);
		# clamp sample region to end at cursor pos
		if sample_region.b > sample_region.a:
			sample_region.b = min(sample_region.b, first_sel.b);
		else:
			sample_region.a = min(sample_region.a, first_sel.b);
		
		"""
		transient_views = sublime.active_window().views(include_transient=True);
		normal_views    = sublime.active_window().views(include_transient=False);

		print("Num views is %d, transient is %d\n" % (len(normal_views), len(transient_views)));
		
		normal_sheets   = sublime.active_window().sheets();
		selected_sheets = sublime.active_window().selected_sheets();
		print("Num sheets is %d, selected is %d\n" % (len(normal_sheets), len(selected_sheets)));
		"""
		
		if resample_word_again:
			resample_word_again = False
			
			sample = self.view.substr(sample_region)
			regex  = "\W" + sample + "\w*";
			regex_flags = 0;
		
			#print("*********Find matches with regex: " + regex);
			point = first_sel.begin();
			
			# NOTE for some reason Sublime will open a popup screen whenever I try to run a command after any of these 
			# words, which completely halts dabbrev completion... so we just never allow them....
			ignore_words = ["for", "if", "else", "while", "struct", "union", "enum"]
		
			options = [sample] #first word will always be here, so add it anyways
			views = [self.view];
			
			#TODO would be cool if we could search the matching .h/.cpp file as well, but
			#don't feel comfortable enough in python to try to add that
			
			#if 0: #this adds more views based on recently opened files, you can ommit this if you only want the curernt view to be used
			window = sublime.active_window();
			recent_filenames = window.file_history();
			for filename in recent_filenames:
				view = window.find_open_file(filename);
				if view and view.id != self.view.id:
					views.append(view);
			
			
			view_index = 0;
			for view in views:
				if len(options) > 8:
					break; #NOTE we stop searching through views once we have a handful
					
				match_regions = [];
				if view_index == 0:
					match_regions = sorted(view.find_all(regex, regex_flags), key=lambda r: abs(point - r.begin()))
				else:
					match_regions = view.find_all(regex, regex_flags)
				
				for region in match_regions:
					word = view.substr(region)
					if (len(word) > 0) and not (word[0].isalpha() or word[0] == '_'):
						word = word[1:]; #move pass first character
						
					if word in ignore_words:
						continue;
					
					if (len(word) > 0) and (word not in options):
						options.append(word);
						
				view_index += 1;
			
			"""
			for option in options:
				print(option);
			"""
			
			
			# NOTE options should always have one element (sample word). If we find actual matches, begin at first index (1)
			next_option_index = 0;
			if len(options) > 1:
				next_option_index = 1;
			
			
		if len(options) > 0:
			self.view.replace(edit, sample_region, options[next_option_index])
			next_option_index += 1;
			if next_option_index == len(options):
				next_option_index = 0;
			#print("Next option index ", next_option_index);
			
class dabbrev_listen(sublime_plugin.EventListener):
	def on_post_text_command(self, view, command_name, args):
		global resample_word_again;
		if command_name != "dabbrev":
			resample_word_again = True
		#print("Post text command " + command_name);
	
	"""
	def on_selection_modified(self, view):
		print("Selection modified");
	"""