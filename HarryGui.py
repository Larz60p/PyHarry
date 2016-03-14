#
#    HarryGui.py version 1.0.0
#
#    This file is part of PyHarry.py.
#
#    Copyright (c) 2016 - Larry McCaig (A.K.A. Larz60+)
#
#    Licensed under GNU GENERAL PUBLIC LICENSE
#
import tkinter as tk
import tkinter.ttk as ttk
import HarryHelp


class HarryGui(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.hlp = HarryHelp.HarryHelp()
        self.grid()
        self.parent = parent

        self.window_stacking_depth = 0
        self.tcs = None
        self.tcs_initial = 0
        self.tcs_choice = [('Modules', 0), ('Topics', 1),
                           ('Keywords', 2), ('Symbols', 3), ('License', 4)]
        self.tcs_val = tk.IntVar()
        self.tcs_val.set(self.tcs_initial)
        self.radio_item = self.tcs_choice[self.tcs_initial][0]
        self.radio_mode = self.tcs_initial
        self.texf = None
        self.treeframe = None
        self.textframe = None
        self.tree = None

        self.doc_win = None
        self.src_win = None
        self.doc_yscroll = None
        self.src_yscroll = None

        self.txwin = tk.IntVar()
        self.txwin.set(0)
        self.x = 0
        self.y = 0
        self.textrows = 20
        self.width = 5
        self.value_matrix = None

    def tcs_choice_made(self):
        """
        When a new
        :return: No return value
        """
        self.radio_item, self.radio_mode = self.tcs_choice[self.tcs_val.get()]
        self.tree.heading('#0', text=self.radio_item, anchor='w')
        if self.radio_item == 'License':
            self.tree.delete(*self.tree.get_children())
            self.doc_win.delete('1.0', tk.END)
            self.doc_win.insert(tk.END, self.hlp.getLicense())
            self.hide_txtwin(self.src_win, self.src_yscroll)
        else:
            self.loadtree()

    def create_widgets(self, x=0, y=0, textrows=20):
        x, y = self.add_main_win(x, y)
        x, y = self.add_reftype(x, y)
        x, y = self.add_text_win_selector(x, y)
        x, y = self.add_treeview(x, y, textrows)
        self.add_text_windows_frame(x, y, textrows)
        self.add_doc_text_window(textrows)
        self.add_src_text_window(textrows)
        x, y = self.text_win_followup(x, textrows)
        self.add_bottom_frame(x, y)

    def add_main_win(self, x, y):
        top = self.winfo_toplevel()
        top.title('PyHarry v1.0.0 016 Larz60+ (L. McCaig)')
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        l1 = tk.Label(self, text='  PyHarry - Local Python Reference Ver. 1.0.0', font=('-weight bold', 16))
        l1.grid(row=x, column=y, columnspan=self.width, sticky='ew')
        x += 1
        y = 0

        # Separator Line
        sl1 = tk.Frame(self, bg='Black', relief=tk.SUNKEN)
        sl1.grid(row=x, column=y, columnspan=self.width, sticky='nsew')
        x += 1
        y = 0
        return x, y

    def add_reftype(self, x, y):
        # tcs acrynomn for tree_content_selector
        self.tcs = tk.Frame(self, relief=tk.RAISED)
        self.tcs.grid(row=x, column=y, columnspan=self.width)
        rcol = 0
        for content, mode in self.tcs_choice:
            b = tk.Radiobutton(self.tcs, text=content, variable=self.tcs_val,
                               value=mode, command=self.tcs_choice_made)
            b.grid(row=0, column=rcol, sticky='w')
            rcol += 1
        x += 1
        y = 0

        # Separator Line
        sl1 = tk.Frame(self, bg='Black', relief=tk.SUNKEN)
        sl1.grid(row=x, column=y, columnspan=self.width, sticky='nsew')
        x += 1
        y = 0
        return x, y

    def add_text_win_selector(self, x, y):
        self.texf = tk.Frame(self, relief=tk.RAISED)
        self.texf.grid(row=x, column=y, columnspan=self.width)
        txtbuf1sel = tk.Radiobutton(self.texf, text='Documentation',
                                    variable=self.txwin, value=0,
                                    command=self.display_text)
        txtbuf1sel.grid(row=0, column=0, sticky='w')
        txtbuf2sel = tk.Radiobutton(self.texf, text='Source Code',
                                    variable=self.txwin,
                                    value=1, command=self.display_text)
        txtbuf2sel.grid(row=0, column=1, sticky='w')
        x += 1
        y = 0

        # Separator Line
        sl1 = tk.Frame(self, bg='Black', relief=tk.SUNKEN)
        sl1.grid(row=x, column=y, columnspan=self.width, sticky='nsew')
        x += 1
        y = 0
        return x, y

    def add_treeview(self, x, y, textrows):
        tree_height = textrows + 3
        self.treeframe = tk.Frame(self, relief=tk.RAISED)
        self.treeframe.grid(row=x, rowspan=textrows, column=y, sticky='nsw')
        # print('x: {}, y: {}'.format(x, y))
        self.tree = ttk.Treeview(self.treeframe, height=tree_height)
        self.tree.grid(row=0, rowspan=textrows, column=0, columnspan=2, sticky='nsw')

        treescrolly = tk.Scrollbar(self.treeframe, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=treescrolly)
        treescrolly.grid(row=0,  rowspan=textrows,  column=2, sticky='ns')
        self.tree.heading('#0', text='Modules', anchor='w')
        self.tree.bind('<Double-1>', self.item_selected)
        y += 2
        return x, y

    def add_text_windows_frame(self, x, y, textrows):
        # Two windows (so far) One for ducumentation, another for
        #  source code. Both are built within the same frame, and are
        #  made visible on demand by changing the stacking order with Raise
        #  and lower

        # The frame remains constant. The text windows are each exactly the same
        #   physical size, but will vary in size logically.. The variable
        #   self.window_stacking_depth is incremented once for each
        #   window in the stack, and is used to rotate (using lift and lower) the
        #   desired window to the top of the stack. This means that the window
        #   remains in memory, but the convenience is worth the overhead. The window
        #   content changes only when a new subject is selected. This allows very
        #   fast rotation through the cached windows.

        self.textframe = tk.Frame(self, relief=tk.RAISED)
        self.textframe.grid(row=x, rowspan=textrows, column=y, sticky='nsew')

    def add_doc_text_window(self, textrows):
        # This is the documentation text window:
        self.doc_win = tk.Text(self.textframe, bg='#CEF6EC', wrap=tk.WORD, bd=2)
        self.doc_win.grid(row=0, rowspan=textrows, column=0,
                          padx=2, pady=2, sticky='nw')
        self.doc_yscroll = tk.Scrollbar(self.textframe, orient=tk.VERTICAL,
                                        command=self.doc_win.yview)
        self.doc_yscroll.grid(row=0,  rowspan=textrows,  column=1, sticky='ns')
        self.doc_win.configure(yscroll=self.doc_yscroll.set)
        # Don't forget to increment stacking depth, won't work without.
        self.window_stacking_depth += 1

    def add_src_text_window(self, textrows):
        # This is the documentation text window:
        self.src_win = tk.Text(self.textframe, bg='#F5F6CE', wrap=tk.WORD, bd=2)
        self.src_win.grid(row=0, rowspan=textrows, column=0,
                          padx=2, pady=2, sticky='nw')
        self.src_yscroll = tk.Scrollbar(self.textframe, orient=tk.VERTICAL,
                                        command=self.src_win.yview)
        self.src_yscroll.grid(row=0,  rowspan=textrows,  column=1, sticky='ns')
        self.src_win.configure(yscroll=self.src_yscroll.set)
        # Don't forget to increment stacking depth, won't work without.
        self.window_stacking_depth += 1
        # Don't forget to increment stacking depth, won't work without.
        self.window_stacking_depth += 1

        self.hide_txtwin(self.src_win, self.src_yscroll)

    def text_win_followup(self, x, textrows):
        x += textrows
        y = 0

        # Separator Line
        sl2 = tk.Frame(self, bg='Black', relief=tk.SUNKEN)
        sl2.grid(row=x, column=y, columnspan=self.width, sticky='nsew')
        x += 1
        y = 0

        return x, y

    def add_bottom_frame(self, x, y):
        f2 = tk.Frame(self, relief=tk.FLAT)
        f2.grid(row=x, column=y, columnspan=self.width, sticky='nsew')
        quit_app = tk.Button(f2, text='Quit', command=self.quit)
        quit_app.grid(row=0, column=0, sticky='w')

        l2 = tk.Label(f2, text="Author - Larz60+ - 2016")
        l2.grid(row=0, column=1, sticky='w')
        # x += 1
        # y = 0
        # return x, y

    @staticmethod
    def hide_txtwin(win, scroll):
        win.lower()
        scroll.lower()

    @staticmethod
    def show_txtwin(win, scroll):
        win.lift()
        scroll.lift()

    def display_text(self):
        wintype = self.txwin.get()
        if wintype == 0:
            self.hide_txtwin(self.src_win, self.src_yscroll)
        else:
            self.show_txtwin(self.src_win, self.src_yscroll)

    def loadtree(self):
        self.value_matrix = None
        # print('self.radio_item: {}'.format(self.radio_item))
        self.tree.delete(*self.tree.get_children())
        if self.radio_item == 'Modules':
            self.value_matrix = self.hlp.getModuleList()
        elif self.radio_item == 'Topics':
            self.value_matrix = self.hlp.getTopicsList()
        elif self.radio_item == 'Keywords':
            self.value_matrix = self.hlp.getKeywordList()
        elif self.radio_item == 'Symbols':
            self.value_matrix = self.hlp.getSymbolList()
        if self.value_matrix is not None:
            self.value_matrix.sort()
            for item in self.value_matrix:
                self.tree.insert('', 'end', text=item, open=False)

    def item_selected(self, event):
        # code inspect will give error on event as unused
        # ... Don't remove it it's used under the covers
        # if you do, system will crash
        self.hide_txtwin(self.src_win, self.src_yscroll)
        curitem = self.tree.focus()
        x = self.tree.item(curitem)

        self.hlp.getHelp(x['text'])
        self.doc_win.delete('1.0', tk.END)
        self.doc_win.tag_configure('tag-center', justify='center')
        if self.hlp.mhelp is not None:
            # Insert Title as first line
            self.doc_win.insert('end', 'Documentation for {}\n\n'.format(x['text']), 'tag-center')
            self.doc_win.insert(tk.END, self.hlp.mhelp)
        else:
            # Insert Title as first line
            self.doc_win.insert('end', 'Documentation not available for {}\n\n'.format(x['text']), 'tag-center')
        self.src_win.delete('1.0', tk.END)
        self.hlp.getSource(x['text'])
        self.src_win.tag_configure('tag-center', justify='center')
        if self.hlp.source is not None:
            self.src_win.insert('end', 'Source Code for {}\n\n'.format(x['text']), 'tag-center')
            self.src_win.insert(tk.END, self.hlp.source)
        else:
            self.src_win.insert('end', 'Source Code not available for {}\n\n'.format(x['text']), 'tag-center')
