from tkinter import *
from tkinter import ttk
from MS_MUX_channel_select import store_script, get_script


class MSEditorCV:
    def __init__(self):
        """ Mux module potentiostat (EmStat4) visual interface """
        self.c0 = None
        self.param1 = None
        self.param2 = None
        self.param3 = None
        self.param4 = None
        self.param5 = None
        self.param6 = None
        # equilibration time
        self.param7 = None
        self.param8 = None
        self.master = None
        self.root = None

        # tracking the method editor
        # self.global_editor_tracker = global_editor_tracker
        # Pseudo parallel params
        # self.channel_time = 1000  # (ms)
        # self.sampling_time = 50  # (ms)

        # self.step_time = 100  # (ms) step time
        self.n_mux_channels = 1  # number of channels to be used, default to 1
        self.active_channels = [IntVar() for i in range(0, 8)]  # track channel states
        self.active_channels[0].set(1)  # Select at least one channel
        self.channel_id_list = [1]  # save id of the active channels

        # User parameters for potentiometry measurement
        # self.run_time = self.channel_time * self.n_mux_channels  # (ms) total experiment time
        self.e_begin = 0  # mV
        self.e_v1 = -500  # mV
        self.e_v2 = 500  # mV
        self.e_step = 10  # mV
        self.sr = 50  # mV/s
        self.scans = 5
        # equilibration
        self.eq_pot = 0  # mV
        self.eq_time = 1  # s

    def open(self, master, global_editor_tracker: list):
        """ Opening UI for user inputs"""
        self.root = Toplevel()
        self.root.transient(master)
        self.root.lift()
        self.root.title('CV_MS MUX Editor')
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
            Checkbutton(f0, text=f"Channel {i + 1}", variable=self.active_channels[i])\
                .grid(row=int(i / 2), column=i - 2 * int(i / 2))

        f2 = LabelFrame(self.root, text="Equilibration time")
        f2.pack(expand=1, fill=BOTH, pady=5, padx=5)

        f1 = LabelFrame(self.root, text="CV parameters")
        f1.pack(expand=1, fill=BOTH, pady=5, padx=5)

        # Potentiometer parameters
        Label(f1, text='E begin (mV):').grid(row=1, column=0)
        self.param1 = Entry(f1, width=10)
        self.param1.insert(0, str(self.e_begin))
        self.param1.grid(row=1, column=1)
        # self.e1['state'] = DISABLED

        self.param1.bind('<Button-1>', self.reset_color)

        Label(f1, text='E vertex 1 (mV)').grid(row=2, column=0)
        self.param2 = Entry(f1, width=10)
        self.param2.insert(0, str(self.e_v1))
        self.param2.grid(row=2, column=1)

        self.param2.bind('<Button-1>', self.reset_color)
        # self.e2.bind('<FocusOut>', self.update_run_time_event)

        Label(f1, text='E vertex 2 (mV)').grid(row=3, column=0)
        self.param3 = Entry(f1, width=10)
        self.param3.insert(0, str(self.e_v2))
        self.param3.grid(row=3, column=1)

        self.param3.bind('<Button-1>', self.reset_color)

        Label(f1, text='E step (mV)').grid(row=4, column=0)
        self.param4 = Entry(f1, width=10)
        self.param4.insert(0, str(self.e_step))
        self.param4.grid(row=4, column=1)

        self.param4.bind('<Button-1>', self.reset_color)

        Label(f1, text='Scan Rate (mV/s)').grid(row=5, column=0)
        self.param5 = Entry(f1, width=10)
        self.param5.insert(0, str(self.sr))
        self.param5.grid(row=5, column=1)

        self.param5.bind('<Button-1>', self.reset_color)

        Label(f1, text='Nº scans').grid(row=6, column=0)
        self.param6 = Entry(f1, width=10)
        self.param6.insert(0, str(self.scans))
        self.param6.grid(row=6, column=1)

        self.param6.bind('<Button-1>', self.reset_color)

        Label(f2, text='Eq. Potential (mV)').grid(row=0, column=0)
        self.param7 = Entry(f2, width=10)
        self.param7.insert(0, str(self.eq_pot))
        self.param7.grid(row=0, column=1)

        self.param7.bind('<Button-1>', self.reset_color)

        Label(f2, text='Eq. Time (s)').grid(row=1, column=0)
        self.param8 = Entry(f2, width=10)
        self.param8.insert(0, str(self.eq_time))
        self.param8.grid(row=1, column=1)

        self.param8.bind('<Button-1>', self.reset_color)

        b1 = Button(self.root, text='Submit', command=self.updateParams, bg="azure2")
        b1.pack(expand=1, fill=BOTH, pady=5, padx=5)

        self.root.bind("<Return>", self.updateParams)

    def updateParams(self, e=None):
        """Getting input values by user and writing to MS file"""
        self.release_focus()
        self.get_nchannel()
        try:
            i = 0  # to track which entry as the mistake
            self.e_begin = int(float(self.param1.get()))  # mV
            i = 1
            self.e_v1 = int(float(self.param2.get()))  # mV
            i = 2
            self.e_v2 = int(float(self.param3.get()))  # mV
            i = 3
            self.e_step = int(float(self.param4.get()))  # mV
            i = 4
            self.sr = int(float(self.param5.get()))  # mV/s
            i = 5
            self.scans = int(float(self.param6.get()))
            i = 6
            self.eq_pot = int(float(self.param7.get()))
            i = 7
            self.eq_time = int(float(self.param8.get()))

            self.writeSingleMS()
            self.close()
        except ValueError:
            if i == 0:
                self.param1.configure(foreground='red')
            elif i == 1:
                self.param2.configure(foreground='red')
            elif i == 2:
                self.param3.configure(foreground='red')
            elif i == 3:
                self.param4.configure(foreground='red')
            elif i == 4:
                self.param5.configure(foreground='red')
            elif i == 5:
                self.param6.configure(foreground='red')
            elif i == 6:
                self.param7.configure(foreground='red')
            elif i == 7:
                self.param8.configure(foreground='red')

    def writeSingleMS(self):
        script = get_script('MethodScripts-firmware/MS_Single_meas_CV_MUX_TEMPLATE.mscr')

        script = script.replace('E_BEGIN', f'{self.e_begin}')
        script = script.replace("E_V1", f'{self.e_v1}')
        script = script.replace("E_V2", f'{self.e_v2}')
        script = script.replace("E_STEP", f'{self.e_step}')
        script = script.replace("SR", f'{self.sr}')
        script = script.replace("SCANS", f'{self.scans}')

        script = script.replace("VDC", f'{self.eq_pot}')
        script = script.replace("EQTIME", f'{self.eq_time}')

        script = script.replace("NCHANNELS", f'{self.n_mux_channels}')
        script = script.replace("IDCHANNELS", f'{self.n_mux_channels-1}')
        array_to_MS = ""
        for i, channel in enumerate(self.channel_id_list):
            array_to_MS += f"array_set u {i}i {channel}i\n"
        script = script.replace("ARRAY_USER_CHANNELS", f'{array_to_MS[0:-1]}')

        store_script(script, "MethodScripts-firmware/Teste_file.mscr")

    def reset_color(self, e):
        """Reset entry color on click by user"""
        self.param1.configure(foreground='black')
        self.param2.configure(foreground='black')
        self.param3.configure(foreground='black')
        self.param4.configure(foreground='black')
        self.param5.configure(foreground='black')
        self.param6.configure(foreground='black')

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

    def close(self):
        self.root.grab_release()
        self.root.destroy()