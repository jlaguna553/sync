from f_actions import *


class Content(object, Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.up = Text(self.root,
                       width=100,
                       height=10)
        self.up.pack()
        self.up.delete('1.0', END)
        self.up.config(state=DISABLED)
        self.up_progress = ttk.Progressbar(orient="horizontal",
                                           length=200,
                                           mode="indeterminate")
        self.up_progress.pack()
        self.button_up_start = Button(text='Sitio => Web',
                                      command=None)
        self.button_up_start.pack()
        self.button_up_stop = Button(text='Stop',
                                     command=None)
        self.button_up_stop.pack()
        self.down = Text(self.root,
                         width=100,
                         height=10)
        self.down.pack()
        self.down.delete('1.0', END)
        self.down.config(state=DISABLED)
        self.down_progress = ttk.Progressbar(orient="horizontal",
                                             length=200,
                                             mode="indeterminate")
        self.down_progress.pack()
        self.button_down_start = Button(text='Web => Sitio',
                                        command=None)
        self.button_down_start.pack()
        self.button_down_stop = Button(text='Stop',
                                       command=None)
        self.button_down_stop.pack()
        self.f_up_messages('Cargar los archivos necesarios subida')
        self.f_down_messages('Cargar los archivos necesarios bajada')

    def f_up_messages(self, msg=''):
        self.up.config(state='normal')
        self.up.delete('1.0',END)
        self.up.insert("1.0", msg)
        self.up.config(state=DISABLED)

    def f_down_messages(self, msg=''):
        self.down.config(state='normal')
        self.down.delete('1.0',END)
        self.down.insert("1.0", msg)
        self.down.config(state=DISABLED)

    def f_up_progress(self):
        pass
