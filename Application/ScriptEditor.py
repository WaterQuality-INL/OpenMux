from tkinter import *
from tkinter import ttk
from MS_MUX_channel_select import store_script, get_script


class MSEditor:
    def __init__(self):
        """ Mux module potentiostat (EmStat4) visual interface """
        self.c0 = None
        self.e1 = None
        self.e2 = None
        self.e3 = None
        self.master = None
        self.root = None

        # Pseudo parallel params
        self.channel_time = 1000  # (ms)
        self.sampling_time = 50  # (ms)

        # self.step_time = 100  # (ms) step time
        self.n_mux_channels = 1  # number of channels to be used, default to 1
        self.active_channels = [IntVar() for i in range(0, 8)]  # track channel states
        self.active_channels[0].set(1)  # Select at least one channel
        self.channel_id_list = [1]  # save id of the active channels

        # User parameters for potentiometry measurement
        self.run_time = self.channel_time * self.n_mux_channels  # (ms) total experiment time

    def open(self, master, global_editor_tracker: list):
        """ Opening UI for user inputs"""
        self.root = Toplevel()
        self.root.transient(master)
        self.root.lift()
        self.root.title('MS MUX Editor')
        self.root.iconbitmap(r'Icons/group-30_116053.ico')
        self.root.resizable(False, False)
        self.root.focus_set()
        self.root.grab_set()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.master = master

        global_editor_tracker[0] = self

        # Channel select and update variables
        f0 = LabelFrame(self.root, text="Channel Select")
        f0.pack(expand=1, fill=BOTH, pady=5, padx=5)

        for i in range(0, 8):
            # Checkbutton(f0, text=f"Channel {i+1}", variable=self.active_channels[i], command=self.update_run_time_event)\
            #     .grid(row=int(i/2), column=i-2*int(i/2))
            Checkbutton(f0, text=f"Channel {i + 1}", variable=self.active_channels[i])\
                .grid(row=int(i / 2), column=i - 2 * int(i / 2))

        # Window for potentiometry settings
        f1 = Frame(self.root)
        f1.pack(expand=1, fill=BOTH, pady=5, padx=5)

        # Potentiometer parameters
        Label(f1, text='Run time (s):').grid(row=1, column=0)
        self.e1 = Entry(f1, width=10)
        self.e1.insert(0, str(round(self.run_time/1000, 2)))
        self.e1.grid(row=1, column=1)
        # self.e1['state'] = DISABLED

        self.e1.bind('<Button-1>', self.reset_color)

        Label(f1, text='Channel time (s):').grid(row=2, column=0)
        self.e2 = Entry(f1, width=10)
        self.e2.insert(0, str(round(self.channel_time/1000, 4)))
        self.e2.grid(row=2, column=1)

        self.e2.bind('<Button-1>', self.reset_color)
        # self.e2.bind('<FocusOut>', self.update_run_time_event)

        Label(f1, text='Sampling time (ms):').grid(row=3, column=0)
        self.e3 = Entry(f1, width=10)
        self.e3.insert(0, str(self.sampling_time))
        self.e3.grid(row=3, column=1)

        self.e3.bind('<Button-1>', self.reset_color)

        b1 = Button(self.root, text='Submit', command=self.updateParams, bg="azure2")
        b1.pack(expand=1, fill=BOTH, pady=5, padx=5)

        self.root.bind("<Return>", self.updateParams)

    def updateParams(self, e=None):
        """Getting input values by user and writing to MS file"""
        self.release_focus()
        self.get_nchannel()
        try:
            i = 0  # to track which entry as the mistake
            self.run_time = int(float(self.e1.get()) * 1000)
            i = 1
            self.channel_time = int(float(self.e2.get()) * 1000)
            i = 2
            self.sampling_time = int(float(self.e3.get()))

            self.writeSingleMS()
            self.close()
        except ValueError:
            if i == 0:
                self.e1.configure(foreground='red')
            elif i == 1:
                self.e2.configure(foreground='red')
            elif i == 2:
                self.e2.configure(foreground='red')

    # def writeMS(self):
    #     """Update MS file from template"""
# 
    #     script = get_script('MethodScripts/PotentiometryPtGPIOAuto_template.mscr')
# 
    #     # script = script.replace('PARAMS_HERE', f'{self.sampling_time}m {self.channel_time}m')
    #     script = script.replace('SAMPLING_HERE', f'{self.sampling_time}m')
    #     script = script.replace('TIME_HERE', f'{self.channel_time}m')
    #     store_script(script, path='MethodScripts/PotentiometryPtGPIOAuto.mscr')

    def writeSingleMS(self):
        script = get_script('MethodScripts-firmware/MS_Single_meas_Potentiometry_MUX_TEMPLATE.mscr')

        script = script.replace('STIME', f'{self.sampling_time}')
        script = script.replace('RTIME', f'{self.run_time}')
        script = script.replace("ITIME", f'{self.channel_time}')
        script = script.replace("XTIME", f'{self.channel_time}')
        script = script.replace("NCHANNELS", f'{self.n_mux_channels}')
        script = script.replace("IDCHANNELS", f'{self.n_mux_channels-1}')
        array_to_MS = ""
        for i, channel in enumerate(self.channel_id_list):
            array_to_MS += f"array_set u {i}i {channel}i\n"
        script = script.replace("ARRAY_USER_CHANNELS", f'{array_to_MS[0:-1]}')

        store_script(script, "MethodScripts-firmware/Teste_file.mscr")

    def reset_color(self, e):
        """Reset entry color on click by user"""
        self.e1.configure(foreground='black')
        self.e2.configure(foreground='black')
        self.e3.configure(foreground='black')

    def release_focus(self, e=None):
        self.master.focus_set()

    def get_nchannel(self):
        # self.n_mux_channels = int(self.c0.get())
        # self.update_run_time()
        sum = 0
        self.channel_id_list = []  # reset list
        # Check which channels were selected by user, and add them to the list of active channels
        for i, item in enumerate(self.active_channels):
            sum += item.get()
            if item.get():
                self.channel_id_list.append(i)
        self.n_mux_channels = sum

    def update_run_time(self):
        self.channel_time = int(float(self.e2.get()) * 1000)
        self.e1.delete(0, END)
        self.e1.insert(0, self.channel_time*self.n_mux_channels/1000)

    def update_run_time_event(self, e=None):
        # self.e1['state'] = NORMAL
        self.get_nchannel()
        self.update_run_time()
        # self.e1['state'] = DISABLED

    def close(self):
        self.root.grab_release()
        self.root.destroy()


class MSEditorCrono:
    def __init__(self):
        """ Mux module potentiostat (EmStat4) visual interface """
        self.c0 = None
        self.e1 = None
        self.e2 = None
        self.e3 = None
        self.e4 = None
        self.e5 = None
        self.root = None
        self.master = None
        self.GLOBAL_CURR_MAX = None


        # Pseudo parallel params
        self.channel_time = 1000  # (ms)
        self.sampling_time = 50  # (ms)

        # self.step_time = 100  # (ms) step time
        self.n_mux_channels = 1  # number of channels to be used, default to 1
        self.active_channels = [IntVar() for i in range(0, 8)]  # track channel states
        self.active_channels[0].set(1)  # Select at least one channel
        self.channel_id_list = [1]  # save id of the active channels

        # User parameters for potentiometry measurement
        self.run_time = self.channel_time * self.n_mux_channels  # (ms) total experiment time

        self.pot = 0.0  # mV

    def open(self, master, GLOBAL_CURR_MAX, global_editor_tracker: list, use_as_widget=False):
        """ Opening UI for user inputs"""
        if use_as_widget:
            self.root = master
        else:
            self.root = Toplevel()
            self.root.transient(master)
            self.root.lift()
            self.root.title('MS MUX Editor')
            self.root.iconbitmap(r'Icons/group-30_116053.ico')
            self.root.resizable(False, False)
            self.root.focus_set()
            self.root.grab_set()
            self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.master = master
        self.GLOBAL_CURR_MAX = GLOBAL_CURR_MAX

        global_editor_tracker[0] = self

        # Channel select and update variables
        f0 = LabelFrame(self.root, text="Channel Select")
        f0.pack(expand=1, fill=BOTH, pady=5, padx=5)

        for i in range(0, 8):
            # Checkbutton(f0, text=f"Channel {i+1}", variable=self.active_channels[i], command=self.update_run_time_event)\
            #     .grid(row=int(i/2), column=i-2*int(i/2))
            Checkbutton(f0, text=f"Channel {i + 1}", variable=self.active_channels[i])\
                .grid(row=int(i / 2), column=i - 2 * int(i / 2))

        # Window for potentiometry settings
        f1 = Frame(self.root)
        f1.pack(expand=1, fill=BOTH, pady=5, padx=5)

        # Potentiometer parameters
        Label(f1, text='Run time (s):').grid(row=1, column=0)
        self.e1 = Entry(f1, width=10)
        self.e1.insert(0, str(round(self.run_time/1000, 2)))
        self.e1.grid(row=1, column=1)
        # self.e1['state'] = DISABLED

        self.e1.bind('<Button-1>', self.reset_color)

        Label(f1, text='Channel time (s):').grid(row=2, column=0)
        self.e2 = Entry(f1, width=10)
        self.e2.insert(0, str(round(self.channel_time/1000, 4)))
        self.e2.grid(row=2, column=1)

        self.e2.bind('<Button-1>', self.reset_color)
        # self.e2.bind('<FocusOut>', self.update_run_time_event)

        Label(f1, text='Sampling time (ms):').grid(row=3, column=0)
        self.e3 = Entry(f1, width=10)
        self.e3.insert(0, str(self.sampling_time))
        self.e3.grid(row=3, column=1)

        self.e3.bind('<Button-1>', self.reset_color)

        Label(f1, text='Potential (mV):').grid(row=4, column=0)
        self.e4 = Entry(f1, width=10)
        self.e4.insert(0, str(self.pot))
        self.e4.grid(row=4, column=1)

        self.e4.bind('<Button-1>', self.reset_color)

        Label(f1, text='Max Current (mA):').grid(row=5, column=0)
        self.e5 = Entry(f1, width=10)
        self.e5.insert(0, str(self.GLOBAL_CURR_MAX[0]*1000))
        self.e5.grid(row=5, column=1)

        self.e5.bind('<Button-1>', self.reset_color)

        b1 = Button(self.root, text='Submit', command=self.updateParams, bg="azure2")
        b1.pack(expand=1, fill=BOTH, pady=5, padx=5)

        self.root.bind("<Return>", self.updateParams)

    def updateParams(self, e=None):
        """Getting input values by user and writing to MS file"""
        self.release_focus()
        self.get_nchannel()
        try:
            i = 0  # to track which entry as the mistake
            self.run_time = int(float(self.e1.get()) * 1000)
            i = 1
            self.channel_time = int(float(self.e2.get()) * 1000)
            i = 2
            self.sampling_time = int(float(self.e3.get()))
            i = 3
            self.pot = int(float(self.e4.get()))
            i = 4
            self.GLOBAL_CURR_MAX[0] = float(self.e5.get())/1000

            self.writeSingleMS()
            self.close()
        except ValueError:
            if i == 0:
                self.e1.configure(foreground='red')
            elif i == 1:
                self.e2.configure(foreground='red')
            elif i == 2:
                self.e2.configure(foreground='red')
            elif i == 3:
                self.e4.configure(foreground='red')
            elif i == 4:
                self.e5.configure(foreground='red')

    # def writeMS(self):
    #     """Update MS file from template"""
# 
    #     script = get_script('MethodScripts/PotentiometryPtGPIOAuto_template.mscr')
# 
    #     # script = script.replace('PARAMS_HERE', f'{self.sampling_time}m {self.channel_time}m')
    #     script = script.replace('SAMPLING_HERE', f'{self.sampling_time}m')
    #     script = script.replace('TIME_HERE', f'{self.channel_time}m')
    #     store_script(script, path='MethodScripts/PotentiometryPtGPIOAuto.mscr')

    def writeSingleMS(self):
        script = get_script('MethodScripts-firmware/MS_Single_meas_Chrono_MUX_TEMPLATE.mscr')

        script = script.replace('POTEN', f'{self.pot}')
        script = script.replace('STIME', f'{self.sampling_time}')
        script = script.replace('RTIME', f'{self.run_time}')
        script = script.replace("ITIME", f'{self.channel_time}')
        script = script.replace("XTIME", f'{self.channel_time}')
        script = script.replace("NCHANNELS", f'{self.n_mux_channels}')
        script = script.replace("IDCHANNELS", f'{self.n_mux_channels-1}')
        array_to_MS = ""
        for i, channel in enumerate(self.channel_id_list):
            array_to_MS += f"array_set u {i}i {channel}i\n"
        script = script.replace("ARRAY_USER_CHANNELS", f'{array_to_MS[0:-1]}')

        store_script(script, "MethodScripts-firmware/Teste_file.mscr")

    def reset_color(self, e):
        """Reset entry color on click by user"""
        self.e1.configure(foreground='black')
        self.e2.configure(foreground='black')
        self.e3.configure(foreground='black')
        self.e4.configure(foreground='black')

    def release_focus(self, e=None):
        self.master.focus_set()

    def get_nchannel(self):
        # self.n_mux_channels = int(self.c0.get())
        # self.update_run_time()
        sum = 0
        self.channel_id_list = []  # reset list
        # Check which channels were selected by user, and add them to the list of active channels
        for i, item in enumerate(self.active_channels):
            sum += item.get()
            if item.get():
                self.channel_id_list.append(i)
        self.n_mux_channels = sum

    def update_run_time(self):
        self.channel_time = int(float(self.e2.get()) * 1000)
        self.e1.delete(0, END)
        self.e1.insert(0, self.channel_time*self.n_mux_channels/1000)

    def update_run_time_event(self, e=None):
        # self.e1['state'] = NORMAL
        self.get_nchannel()
        self.update_run_time()
        # self.e1['state'] = DISABLED

    def close(self):
        self.root.grab_release()
        self.root.destroy()
