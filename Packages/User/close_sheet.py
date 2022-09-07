import sublime
import sublime_plugin

#NOTE normally if we have one sheet open sublime will close that tab but I don't want it to close that tab
#since I don't use tabs at all... it's just annoying for me
class close_active_sheet(sublime_plugin.TextCommand):
	def run(self, edit):
		#print("close active sheet");
		window = sublime.active_window();
		selected_sheets = window.selected_sheets();
		
		if len(selected_sheets) > 1:
			active_sheet = window.active_sheet();
			active_sheet.close();