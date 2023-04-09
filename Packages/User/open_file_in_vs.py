import sublime
import sublime_plugin
import re


class open_file_in_vs(sublime_plugin.TextCommand):
	def run(self, edit):
		filename = self.view.file_name()
		if filename is None:
			return

		print(filename)

		cursor_pos = self.view.sel()[0].a
		[cursor_y, cursor_x]  = self.view.rowcol(cursor_pos)
		linenum_str = str(cursor_y + 1)
		sublime.set_clipboard(linenum_str)

		cmd = "devenv /edit " +  filename
		# cmd = "devenv"
		self.view.window().run_command("exec", {"shell_cmd": cmd, "quiet": True})
		self.view.window().run_command("hide_panel", {"cancel": True}) # hide output panel that opens with ever you call "exec" (Is there a more direct way of doing this?)
