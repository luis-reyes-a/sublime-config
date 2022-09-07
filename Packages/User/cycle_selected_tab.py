import sublime
import sublime_plugin

class cycle_selected_tab(sublime_plugin.TextCommand):
	def run(self, edit):
		#print ("cycle selected tab");
		window = sublime.active_window();
		#sheets = window.sheets();
		selected_sheets = window.selected_sheets();
		
		"""
		print("Normal sheets:");
		index = 0;
		for sheet in sheets:
			print("Sheet(%d) at index %d for file %s" % (sheet.id(), index, sheet.file_name()));
			index += 1;
		
		print("\nSelected sheets:");
		index = 0;
		for sheet in selected_sheets:
			print("Sheet(%d) at index %d for file %s" % (sheet.id(), index, sheet.file_name()));
			index += 1;
		"""
			
		active_sheet = window.active_sheet();
		"""
		_, active_sheet_index = window.get_sheet_index(active_sheet);
		print("\nActive sheet(%d) with index %d for file %s\n" % (active_sheet.id(), active_sheet_index, active_sheet.file_name()));
		"""
		
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
			
		
		