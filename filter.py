import sublime, sublime_plugin

def filter(v, e, needle):
    # get non-empty selections
    regions = [s for s in v.sel() if not s.empty()]

    # if there's no non-empty selection, filter the whole document
    if len(regions) == 0:
        regions = [ sublime.Region(0, v.size()) ]

    for region in reversed(regions):
        lines = v.split_by_newlines(region)

        for line in reversed(lines):
            if not needle in v.substr(line):
                v.erase(e, v.full_line(line))

class FilterCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        def done(needle):
            e = self.view.begin_edit()
            filter(self.view, e, needle)
            self.view.end_edit(e)

        cb = sublime.get_clipboard()
        sublime.active_window().show_input_panel("Filter file for lines containing: ", cb, done, None, None)