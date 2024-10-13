import sublime
import sublime_plugin
import re

resample_word_again = True;
next_option_index = 1;
options = [];

# a view is a panel?

# A View is a tab. Sublime allows for there to be multiple tabs into same buffer but
# it's not like a view in emacs/vim. It's literally just a another tab that you can drag to 
# another *panel* to view at the same time

# I don't understand what a sheet is... I think it just describes how a view/tab should display the buffer data

# emacs_highlight_mark_region = False;
emacs_mark_pos = None;


class emacs_copy_region(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("copy");
        #self.view.run_command("deselect");
        sel = self.view.sel()
        if sel:
            carets = [s.b for s in sel]
            sel.clear()
            for caret in carets:
                sel.add(caret)

class emacs_set_mark(sublime_plugin.TextCommand):
    def run(self, edit):
        global emacs_mark_pos;
        emacs_mark_pos = self.view.sel()[0].a;

        # global emacs_highlight_mark_region
        # emacs_highlight_mark_region = True;


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
        
        new_region = sublime.Region(first_sel.b, first_sel.a);
        self.view.sel().clear();
        self.view.sel().add(new_region);
        self.view.show(first_sel.a, show_surrounds=True, keep_to_left=True, animate=True);
        emacs_mark_pos = first_sel.b;



class luis_escape(sublime_plugin.TextCommand):
    def run(self, edit):
        window = sublime.active_window();
        window.run_command('cancel');

        # global emacs_highlight_mark_region;
        # emacs_highlight_mark_region = False;
        # window.active_view().erase_regions("emacs_mark_region");

        # Clear all selelections and keep carets
        sel = self.view.sel()
        if sel:
            carets = [s.b for s in sel]
            sel.clear()
            for caret in carets:
                sel.add(caret) 

"""
class on_text_command_modify(sublime_plugin.EventListener):
    def on_text_command(self, view, command_name, args):
        global emacs_highlight_mark_region;
        if emacs_highlight_mark_region and (command_name == "move" or command_name == "move_to" or command_name == "cursor_mark_swap"):
            args['extend'] = True;
"""

"""
class after_text_command_listen(sublime_plugin.EventListener):
    def on_post_text_command(self, view, command_name, args):
        global emacs_highlight_mark_region;
        if emacs_highlight_mark_region and (command_name == "move" or command_name == "move_to" or command_name == "cursor_mark_swap"):
            view.erase_regions("emacs_mark_region");
            mark_region = sublime.Region(view.sel()[0].a, emacs_mark_pos);
            view.sel().clear();
            view.sel().add(mark_region);
            #mark_regions = [];
            #mark_regions.append(mark_region);
            #view.add_regions("emacs_mark_region", mark_regions, "mark", "dot", sublime.DRAW_NO_FILL)
"""

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
        

        global emacs_mark_pos;
        if revert_to_original_sel :
            self.view.sel().clear();
            self.view.sel().add(sublime.Region(original_sel.end(), original_sel.begin()));
            emacs_mark_pos = original_sel.end();
        else : 
            # here we've selected something new, now make it so cursor is at top..
            new_sel = self.view.sel()[0];
            if (new_sel.begin() != new_sel.b):
                inverted_region = sublime.Region(new_sel.b, new_sel.a);
                self.view.sel().clear();
                self.view.sel().add(inverted_region);
                emacs_mark_pos = new_sel.b;
            self.view.show(self.view.sel()[0].b, show_surrounds=True, keep_to_left=True, animate=True);
        


class luis_focus_next_view(sublime_plugin.TextCommand):
    def run(self, edit):
        window = sublime.active_window();
        """
        group, view_index_in_group = window.get_view_index(window.active_view());
        
        num_views  = window.num_views_in_group(group);
        
        next_view_index = view_index_in_group + 1;
        if next_view_index == num_views:
            next_view_index = 0;
            
        next_view = window.views_in_group(group)[next_view_index];
        window.focus_view(next_view)
        """
        window.run_command('focus_to_right');
        
        active_sheet = window.active_sheet();
        active_view  = window.active_view();
        
        group, sheet_index_in_group = window.get_sheet_index(active_sheet);
        _, view_index_in_group = window.get_view_index(active_view);
        
        num_sheets = window.num_sheets_in_group(group);
        num_views  = window.num_views_in_group(group);
        
        print("In group %d (%d sheets, %d views), sheet idx %d, view idx %d\n" % (group, num_sheets, num_views, sheet_index_in_group, view_index_in_group));

class luis_close_view(sublime_plugin.TextCommand):
    def run(self, edit):
        window = sublime.active_window();
        view   = window.active_view();
        view.set_scratch(True);
        view.close();
        view.set_scratch(False);

class luis_vsplit(sublime_plugin.TextCommand):
    def run(self, edit):
        #transient_views = sublime.active_window().views(include_transient=True);
        #normal_views    = sublime.active_window().views(include_transient=False);
        window = sublime.active_window();
        window.run_command('clone_file', {"add_to_selection": True, "retain_viewport_position": True})
        
        """
        window = sublime.active_window();
        active_sheet = window.active_sheet();
        active_view  = window.active_view();
        group, sheet_index_in_group = window.get_sheet_index(active_sheet);
        _, view_index_in_group = window.get_view_index(active_view);
        
        window.open_file(active_view.file_name(), sublime.NewFileFlags.ADD_TO_SELECTION);
        
        num_sheets = window.num_sheets_in_group(group);
        num_views  = window.num_views_in_group(group);
        

        print("In group %d (%d sheets, %d views), sheet idx %d, view idx %d\n" % (group, num_sheets, num_views, sheet_index_in_group, view_index_in_group));
        """
        
        
        