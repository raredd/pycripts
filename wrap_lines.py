import sublime, sublime_plugin

class WrapLinesExCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        wrap_column = 0

        if self.view.settings().get('word_wrap') == False:
            # wrapping is disabled, do nothing
            return

        if self.view.settings().get('wrap_width') == 0:
            # compute wrap column from viewport width
            wrap_column = int(self.view.viewport_extent()[0] / self.view.em_width())
        else:
            wrap_column = self.view.settings().get('wrap_width')

        e = self.view.begin_edit()
        rewrap(self.view, e, wrap_column)
        self.view.end_edit(e)

def rewrap(v, e, column):
    # 0-indexed current line
    current_line_no = 0

    # RHS expression is line count, can change whenever we create a new one
    while current_line_no < v.rowcol(v.size())[0] + 1:
        # where current line drawing starts
        current_line_coords = v.text_to_layout(v.text_point(current_line_no, 0))

        # rightmost character drawn in current viewport
        textpos = v.layout_to_text((v.em_width() * (column), current_line_coords[1]))

        # physical line boundaries as absolute text positions
        current_line = v.line(textpos)

        if textpos < current_line.b:
            # the current line spans multiple rows, so insert a newline at the wrap column

            textpos = v.layout_to_text((v.em_width() * (column), current_line_coords[1]))
            next_line_indent = v.text_to_layout(textpos+1)[0]

            # TODO why -1?
            next_line_indent_chars = int(next_line_indent/(v.em_width()))-1
            # determine how to indent the following line based on how wide the wrapping indents and what the current tab/spaces settings are
            if v.settings().get('translate_tabs_to_spaces') and v.settings().get('use_tab_stops'):
                next_line_indent_chars = next_line_indent_chars / v.settings().get('tab_size')
                next_line_indent_string = '\t' * next_line_indent_chars
            else:
                next_line_indent_string = ' ' * next_line_indent_chars

            # insert newline and spacing at wrap column (sublime hides actual line endings from editor, therefore it's always LF)
            v.insert(e, textpos, '\n' + next_line_indent_string)
        else:
            # only continue to the next line if we didn't edit the current line
            current_line_no = current_line_no + 1