import sublime
import sublime_plugin
# from collections import defaultdict ## don't think we need this one ...
# import re open_file_in_vs used to include this...

emacs_mark_pos = None;


class emacs_copy_region(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.run_command("copy");
		self.view.run_command("deselect");

class emacs_set_mark(sublime_plugin.TextCommand):
	def run(self, edit):
		global emacs_mark_pos;
		emacs_mark_pos = self.view.sel()[0].a;

class emacs_paste(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.run_command("emacs_set_mark");
		self.view.run_command("paste");

class emacs_cut_line(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.run_command("move_to", {"to": "eol", "extend": True});
		self.view.run_command("cut");


class cursor_mark_swap(sublime_plugin.TextCommand):
	def run(self, edit):
		selections = self.view.sel()
		if selections.__len__() > 1:
			return;

		# NOTE if there is no selection, selection count is still 1
		global emacs_mark_pos;
		if self.view.sel()[0].a == self.view.sel()[0].b:
			new_region = sublime.Region(self.view.sel()[0].a, emacs_mark_pos);
			self.view.sel().add(new_region);
			self.view.show(self.view.sel()[0].a, show_surrounds=True, keep_to_left=True, animate=True);
			return;
			
		first_sel = selections[0];
		# if first_sel.a == first_sel.b:
		# 	return;
			
		# print("swap marks");
		# first_sel.a, first_sel.b = first_sel.b, first_sel.a;
		# sublime.run_command("show_at_center");
		
		new_region = sublime.Region(first_sel.b, first_sel.a);
		self.view.sel().clear();
		self.view.sel().add(new_region);
		self.view.show(first_sel.a, show_surrounds=True, keep_to_left=True, animate=True);
		emacs_mark_pos = first_sel.b;



class my_select_line(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view;
		# print ("Num sels is %d" % (self.view.sel().__len__()) );
		sel = self.view.sel()[0];
		if (sel.b == sel.a) : # no selection, just select first line
			view.run_command("move_to", {"to": "bol", "extend": False});
			view.run_command("move_to", {"to": "eol", "extend": True});
		else : # extend selection to next line
			view.run_command("move", {"by": "lines", "forward": True, "extend": True});
			view.run_command("move_to", {"to": "eol", "extend": True});


class my_select_word(sublime_plugin.TextCommand): 
	def run(self, edit):
		view = self.view;
		sel = self.view.sel()[0];
		if (sel.b == sel.a) : # no selection, just select first line
			view.run_command("move", {"by": "characters", "forward":True, "extend": False});
			view.run_command("move", {"by": "words", "forward":False, "extend": False});
			view.run_command("move", {"by": "word_ends", "forward":True,  "extend": True});
		else : # extend selection to next line
			view.run_command("move", {"by": "word_ends", "forward":True,  "extend": True})


class my_open_scope(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view;
		r = self.view.find("{", self.view.sel()[0].b, sublime.LITERAL|sublime.REVERSE)
		if r:
			r.a = r.end();
			r.b = r.a;
			self.view.sel().clear();
			self.view.sel().add(r);
			self.view.show(r.b, show_surrounds=True, keep_to_left=True, animate=True);
			view.run_command("insert", {"characters": "\n\n"});
			view.run_command("move", {"by": "lines", "forward": False, "extend": False});
			view.run_command("reindent");




# NOTE normally if we have one sheet open sublime will close that tab but I don't want it to close that tab
# since I don't use tabs at all... it's just annoying for me
class my_close_sheet(sublime_plugin.TextCommand):
	def run(self, edit):
		#print("close active sheet");
		window = sublime.active_window();
		selected_sheets = window.selected_sheets();
		
		if len(selected_sheets) > 1:
			active_sheet = window.active_sheet();
			active_sheet.close();



class my_next_sheet(sublime_plugin.TextCommand):
	def run(self, edit):
		window = sublime.active_window();
		selected_sheets = window.selected_sheets();
		active_sheet = window.active_sheet();
		
		# look for active sheet in the sheet stack
		# the sheet *after* it is the next desired sheet, focus it
		next_sheet = None;
		index = 0;
		for sheet in selected_sheets:
			if sheet.id() == active_sheet.id():
				if index == (len(selected_sheets)-1):
					next_sheet = selected_sheets[0];
				else:
					next_sheet = selected_sheets[index + 1];
				break;
			index += 1;
			
		if next_sheet is not None:
			window.focus_sheet(next_sheet);

class my_next_group(sublime_plugin.TextCommand):
	def run(self, edit):
		window = sublime.active_window();
		init_group_index = window.active_group();
		num_groups = window.num_groups();
		next_group_index = init_group_index + 1;
		if (next_group_index == num_groups):
			next_group_index = 0;
		window.focus_group(next_group_index);



"""
Got this one from github but I'm not sure what the for loop is trying to do...
class FileNameOnStatusBar(sublime_plugin.EventListener):
    def on_activated(self, view):
        path = view.file_name()
        print ("Normal path is %s\n" % (path));
        if path:
            for folder in view.window().folders():
                path = path.replace(folder + '/', '', 1)
            print ("Fixed path is %s\n" % (path));
            view.set_status('aaaa', path)
        else:
            view.set_status('aaaa', 'untitled')
"""

import os.path

class FileNameOnStatusBar(sublime_plugin.EventListener):
    def on_activated(self, view):
        path = view.file_name()
        filename  = os.path.basename(path)
        directory = os.path.dirname(path)
        message   = filename + " [" + directory + "]"
        if path:
        	view.set_status('aaaa', message)
        else:
        	view.set_status('aaaa', '[NO FILEPATH]')


# scopes for braces
# source.c++ meta.namespace.c++ meta.function.c++ meta.block.c++ meta.block.c++ 
# punctuation.definition.block.end.c++ 
# meta.block.c++ 

class my_expand_to_scope(sublime_plugin.TextCommand):
	def run(self, edit):
		if self.view.sel().__len__() > 1:
			return; # this command only works for one selection
		
		
		view = self.view;

		# for regions...
		# .b is where cursor is, .a is the other end
		# .begin() is always a lower pos (smaller number) than .end()...


		# annoying hacky thing to make expand_selection work
		if self.view.sel().__len__() == 1 :
			sel = self.view.sel()[0];
			w1  = view.substr(sel.begin())
			w2  = view.substr(sel.end()-1)
			# if (w1 == "{") and (w2 == "}") :
			if ((w1 == "{") and (w2 == "}")) or ((w1 == "(") and (w2 == ")")) :
				if sel.b == sel.begin() :
					inverted_region = sublime.Region(sel.b, sel.a);
					self.view.sel().clear();
					self.view.sel().add(inverted_region);
					# print ("inverted region at start")

		

		original_sel = self.view.sel()[0];
		revert_to_original_sel = True
		for i in range(0, 6) :
			prev_sel = self.view.sel()[0];
			view.run_command("expand_selection", {"to": "scope"});
			new_sel  = self.view.sel()[0];

			if (new_sel.begin() == prev_sel.begin()) and (new_sel.end() == prev_sel.end()) :
				break; # expand_selection couldn't find anything else to expand to, abort


			w1 = view.substr(new_sel.begin())
			w2 = view.substr(new_sel.end()-1)
			# print ("Found sel at %s and %s" % (w1, w2))

			if ((w1 == "{") and (w2 == "}")) or ((w1 == "(") and (w2 == ")")) :
				# found new valid selection
				revert_to_original_sel = False;
				break;
		

		if revert_to_original_sel :
			self.view.sel().clear();
			self.view.sel().add(original_sel);
		else : 
			# here we've selected something new, now make it so cursor is at top..
			new_sel = self.view.sel()[0];
			if (new_sel.begin() != new_sel.b):
				inverted_region = sublime.Region(new_sel.b, new_sel.a);
				self.view.sel().clear();
				self.view.sel().add(inverted_region);
			self.view.show(self.view.sel()[0].b, show_surrounds=True, keep_to_left=True, animate=True);
		
			
				

class open_file_in_vs(sublime_plugin.TextCommand):
	def run(self, edit):
		filename = self.view.file_name()
		if filename is None:
			return

		# print(filename)

		cursor_pos = self.view.sel()[0].a
		[cursor_y, cursor_x]  = self.view.rowcol(cursor_pos)
		linenum_str = str(cursor_y + 1)
		sublime.set_clipboard(linenum_str)

		cmd = "devenv /edit " +  filename
		self.view.window().run_command("exec", {"shell_cmd": cmd, "quiet": True})
		self.view.window().run_command("hide_panel", {"cancel": True}) # hide output panel that opens with ever you call "exec" (Is there a more direct way of doing this?)

class luis_move_right(sublime_plugin.TextCommand):
	def run(self, edit, extend = False):
		last_pos = self.view.sel()[0].b
		self.view.window().run_command("move", {"by": "word_ends", "forward": True, "extend": extend})
		new_pos = self.view.sel()[0].b
		while last_pos != new_pos:
			str = self.view.substr(new_pos-1)
			if str.isalnum() or str[0] == '_':
				break;
			else:
				last_pos = new_pos
				self.view.window().run_command("move", {"by": "word_ends", "forward": True, "extend": extend})
				new_pos  = self.view.sel()[0].b


class luis_move_left(sublime_plugin.TextCommand):
	def run(self, edit, extend = False):
		last_pos = self.view.sel()[0].b
		self.view.window().run_command("move", {"by": "words", "forward": False, "extend": extend})
		new_pos = self.view.sel()[0].b
		while last_pos != new_pos:
			str = self.view.substr(new_pos)
			if str.isalnum() or str[0] == '_':
				break;
			else:
				last_pos = new_pos
				self.view.window().run_command("move", {"by": "words", "forward": False, "extend": extend})
				new_pos  = self.view.sel()[0].b

class luis_backspace_word(sublime_plugin.TextCommand):
	def run(self, edit, extend = False):
		self.view.window().run_command("luis_move_left", {"extend": True})
		self.view.erase(edit, self.view.sel()[0])
		# self.view.window().run_command("left_delete")

class luis_delete_word(sublime_plugin.TextCommand):
	def run(self, edit, extend = False):
		self.view.window().run_command("luis_move_right", {"extend": True})
		# self.view.window().run_command("right_delete")
		self.view.erase(edit, self.view.sel()[0])






class vsplit(sublime_plugin.TextCommand):
	def run(self, edit):
		filename = self.view.file_name();
		if filename is not None:
			first_sel = self.view.sel()[0];
			window = sublime.active_window();
			new_view = window.open_file(filename, sublime.ADD_TO_SELECTION, -1); # NOTE -1 means add this to active group (a group is a 'panel' or 'window' in emacs parlance
			
			new_region = sublime.Region(first_sel.b, first_sel.b);
			new_view.sel().clear();
			new_view.sel().add(new_region);
			new_view.show(first_sel.a, show_surrounds=True, keep_to_left=True, animate=False);


