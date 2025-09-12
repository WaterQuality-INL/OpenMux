import json

from tkinter import messagebox
from tkinter import filedialog

from costume_widgets import *


import serialcom


import threading
import pandas as pd
from tools.export2xl_tool import export_window


""" For OEM system and multiplexing module"""
from device import Emstat4
from ScriptEditor import MSEditor, MSEditorCrono
from CV_MUX_Editor import MSEditorCV



def connection():
    # Creates the window that opens when option connection is selected from the menu
    def refresh_listbox():
        # Identifies the available ports for communication
        port_list = serialcom.see_ports()
        my_listbox.delete(0, END)
        for i in range(0, len(port_list)):
            my_listbox.insert(0, port_list[i])

    def connect_port(e=None):
        # establishes the connection to the selected port
        port_name = my_listbox.get(ANCHOR)
        port_name = port_name.split(' ')
        portID = port_name[0]

        global channel, EMS4  # variable that tracks current connected port
        # channel = serialcom.connect_to(portID, int(bauds.get()))
        # global ser
        # ser = serial.Serial(portID, baudrate=int(bauds.get()), parity=serial.PARITY_ODD, timeout=1)
        channel = portID

        EMS4 = Emstat4(channel, timeout=5)

        if channel != "None":
            # if connection is established successfully to the desired port
            main_status.config(text="Connected to: " + portID)
            device_LED.set_led_status(True)
            close_top()
            # serialcom.read_port(channel)
        else:
            # if connection is not established successfully to the desired port
            main_status.config(text="Connection failed")
            device_LED.set_led_status(False)

        if e is not None:
            close_top()

    def scroll_function(event):
        if event.delta > 0:
            my_listbox.xview_scroll(-1, "unit")
        else:
            my_listbox.xview_scroll(1, "unit")

    def close_top():
        my_listbox.unbind_all('<MouseWheel>')
        top.grab_release()
        top.destroy()

    top = Toplevel()
    # top.attributes('-topmost', 'true')
    # top.geometry("400x400")
    top.resizable(False, False)
    top.transient(root)
    top.lift()
    top.protocol("WM_DELETE_WINDOW", close_top)
    top.grab_set()

    # creates the input for the bauds number
    f_properties = LabelFrame(top, text="Connection properties")
    f_properties.pack()
    l_bauds = Label(f_properties, text="Bauds")
    bauds = Entry(f_properties, fg="grey")
    bauds.insert(0, str(153600))
    l_bauds.grid(row=0, column=0)
    bauds.grid(row=0, column=1)

    # Create interactive display port window
    my_frame = LabelFrame(top, text="Ports")
    my_frame.pack()

    my_scrollbarX = Scrollbar(my_frame, orient=HORIZONTAL)
    my_scrollbarY = Scrollbar(my_frame, orient=VERTICAL)
    my_listbox = Listbox(my_frame, height=4, xscrollcommand=my_scrollbarX.set, yscrollcommand=my_scrollbarY.set)
    my_scrollbarY.config(command=my_listbox.yview)
    my_scrollbarX.config(command=my_listbox.xview)
    my_scrollbarY.pack(side=RIGHT, fill=Y)
    my_scrollbarX.pack(side=BOTTOM, fill=X)
    my_listbox.pack(fill=BOTH, expand=1)

    my_listbox.bind_all('<MouseWheel>', scroll_function)
    my_listbox.bind('<Return>', connect_port)

    # creates the buttons for interaction
    b_connect = Button(top, text="Connect", command=connect_port, bg="Azure2")
    b_refresh = Button(top, text="Refresh", command=refresh_listbox, bg="Azure2")
    b_close = Button(top, text="Close", command=close_top, bg="Azure2")
    b_connect.pack(fill=BOTH)
    b_refresh.pack(fill=BOTH)
    b_close.pack(fill=BOTH)

    # automatically updates the list of available ports
    refresh_listbox()


def load_xldata(file):
    """
    Loads the data from a excel file.
    :param
    filename: str
        string with the path to the desired file
    :return:
    xx: ndarray
        array with the frequencies
    yy: complex ndarray
        impedance array
    """
    df = pd.read_excel(io=file)

    # Getting only values as numpy array
    array = df.values

    volt = array[:, 0]
    curr = array[:, 1]

    flag = 'Not available!'

    add_data(xx=volt.tolist(), yy=curr.tolist(), flag=flag, filename=file.split('/')[-1].replace('.xlsx', ''))


def load_txtdata(file):
    with open(file, 'r') as data:
        data = data.read()

        # Getting flag
    try:
        flag, data = data.split('-tear-')
    except ValueError:
        flag = 'Not available!'

    volt = []
    curr = []
    for item in data.split('\n'):
        try:
            values = item.split('\t')
            volt.append(float(values[0]))
            curr.append(float(values[1]))
        except ValueError:
            pass
        except IndexError:
            pass

    add_data(xx=volt, yy=curr, flag=flag, filename=file.split('/')[-1].replace('.txt', ''))


def load_elchem(file):
    with open(file, 'r') as data:
        jsonStr = data.read()
    pyDic = json.loads(jsonStr)

    nCharts = len(pyDic['Charts'])
    for chart in pyDic['Charts']:
        add_chart()
        for line in chart['Lines']:
            # add lines to chart
            volt = line['x']
            curr = line['y']
            flag = line['tech']
            name = line['Name']
            add_data(xx=volt, yy=curr, flag=flag, filename=name)


def load_from_file():
    """ loads data from a CSV or space delimited file """
    file = filedialog.askopenfilename()

    if file != '':
        if file.find('.txt') != -1:
            load_txtdata(file)
        elif file.find('.xlsx') != -1:
            load_xldata(file)
        elif file.find('.elchem') != -1:
            load_elchem(file)
        else:
            messagebox.showerror('File type not valid', 'Only .txt or .xlsx or .elchem files can'
                                                        ' be loaded!')


def add_data(xx, yy, flag, filename):
    # TODO is this try/except block really needed
    try:
        Active_tab = update_tabs()
        # Extracting graph (axes) from tab
        voltam_graph = Active_tab.chart

        # Creating series in graphs (axes)
        voltam_series = ttm.NewSeries(voltam_graph, flag)
        line = voltam_series.add_coordinate_list(xx, yy)
        my_tree_menu.add_line(line, chart=Active_tab.chart, name=filename)
    except UnboundLocalError:
        print('Selected file not valid for data reading')


def add_chart():
    global char_num
    # Creating new tab
    char_num += 1
    Active_tab = my_notebook.add_costume_tab(label=f'Chart {char_num}')
    # Loading widget view to second tab and defining the working chart
    Active_tab.update_tree(my_tree_menu)
    my_tree_menu.add_chart(Active_tab.chart, 'Chart' + str(char_num))
    # Lifting New tab
    my_notebook.select(Active_tab.tab)
    return Active_tab


def update_tabs():
    """
    This function dchecks if new tabs need to be created and updates the variables tracking the tabs (Charts).
    tabs_list, Active_tab, and the treeview
    """
    try:
        Active_tab = my_notebook.get_costume_tab()
    except TclError:
        Active_tab = add_chart()

    return Active_tab


def start_comsInthread():
    global trun
    trun = threading.Thread(target=start_coms, args=(GLOBAL_EDITOR_TRACKER[0],))
    trun.start()
    # trun.join()


def start_coms(editor):
    # TODO fix: When all tabs are destroyed and run is pressed in overlay mode. There is no tab to plot data
    global ABORT
    # Disabling button start while measuring
    b_start['state'] = DISABLED
    b_stop['state'] = NORMAL
    # active_channels = [chan for i, chan in enumerate(list(MM.MUX_CHANNELs.values())) if i in MSE.channel_id_list]
    print(f"GLOBAL_MAX_CURRENT = {MAX_CURR[0]*1000} mA")
    current_LED.set_led_status(True)
    # Looping the number of channels selected
    try:
        EMS4.openSerial()

        Active_tab = update_tabs()
        # Defining Plots and series
        voltam_graph = Active_tab.chart
        series_channel = []
        for i, idc in enumerate(editor.channel_id_list):
            voltam_series = ttm.NewSeries(voltam_graph, f"channel {idc+1}")
            my_tree_menu.add_line(voltam_series.line, chart=Active_tab.chart, name=f"Channel {idc+1}")
            series_channel.append(voltam_series)
        # EMS4 = Emstat4(channel)

        # pb.reset(int(MSE.run_time / MSE.channel_time))

        # Finishing previous operation
        EMS4.abort_and_sync()
        EMS4.send_script('MethodScripts-firmware/Teste_file.mscr')
        if isinstance(editor, MSEditorCV):
            voltam_graph.change_labels("WE Potential (V)", "Current (A)")
            for _ in series_channel:
                print("New channel")
                line = ""
                while line != "*\n":  # waiting for equilibration time
                    line = EMS4.readline()
                line = ""
                while line != "*\n":
                    if ABORT:
                        print("Aborting...")
                        EMS4.abort_and_sync()
                        break
                    line = EMS4.readline()

                    point = EMS4.parseline(line)
                    print(line)
                    print(point)
                    if point is not None:
                        series_channel[int(point[2][0])].add_coordinates(point[0], point[1] * 1000)
        else:
            line = ""
            while line != "*\n":
                if ABORT:
                    print("Aborting...")
                    EMS4.abort_and_sync()
                    break

                line = EMS4.readline()

                point = EMS4.parseline(line)

                if point is not None:
                    print(point)
                    # if point.__len__() == 3:
                    if isinstance(editor, MSEditor):
                        # Display Potentiometry
                        voltam_graph.change_labels("WE Potential (mV)", "Current (A)")
                        series_channel[int(point[2][0])].add_coordinates(point[1], point[0] * 1000)
                    # elif point.__len__() == 4:
                    elif isinstance(editor, MSEditorCrono):
                        # Display Chrono
                        voltam_graph.change_labels("Time (s)", "Current (A)")
                        if point[1] >= MAX_CURR[0] or -point[1] <= -MAX_CURR[0]:
                            current_LED.set_led_status(False)
                            EMS4.abort_and_sync()
                            print("Aborting...")
                            break
                        else:
                            series_channel[int(point[3][0])].add_coordinates(point[2], point[1])
        EMS4.closeSerial()
        # pb.complete()
        ABORT = False
    except NameError as e:
        # TODO check if the curves end with the same length when thread is killed
        if type(e) == NameError:
            connection()
        print(e)

    b_start['state'] = NORMAL
    b_stop['state'] = DISABLED


def stop_coms():
    # Tells the microcontroller to stop
    b_stop['state'] = DISABLED
    if trun.is_alive():
        global ABORT
        ABORT = True

        b_stop['state'] = DISABLED


def config_update(opt):
    """
    Updates the byte related to the config var from the platform.
    :param opt: str
        option to be added or removed
    """
    global config
    if opt == 'mp' and mp.get():
        # Enabling electrode protection during measure
        config += 0b00010000
    elif opt == 'mp' and not mp.get():
        # Disabling electrode protection during measure
        config -= 0b00010000
    elif opt == 'pp' and pp.get():
        # Enabling electrode protection during precondition
        config += 0b00000001
    elif opt == 'pp' and not pp.get():
        # Disabling electrode protection during precondition
        config -= 0b00000001


def export_to():
    export_window(root, my_tree_menu)
    pass


def good_bye():
    if messagebox.askokcancel("Quit", "Do you want to quit this program?\nAny unsaved data will be lost!"):
        root.destroy()


def save_elchem():
    dic4json = my_tree_menu.get_data4jason()
    jsonStr = json.dumps(dic4json)

    filename = filedialog.asksaveasfilename(title='Save to file',
                                            filetypes=(('Elchem data file', '*.elchem'), ('All files', "*.*")))

    filename = filename.replace(".elchemdata", '') + '.elchemdata'

    with open(filename, 'w') as file:
        file.write(jsonStr)


def set_prefs():
    pass


root = Tk()
root.title('Elchem')
root.iconbitmap(r'Icons/group-30_116053.ico')
root.geometry('800x500')
root.state('zoomed')
root.protocol("WM_DELETE_WINDOW", good_bye)

# ser = None
EMS4: Emstat4

GLOBAL_EDITOR_TRACKER = [None]
MSE = MSEditor()
CVMSE = MSEditorCV()
MSE_Chrono = MSEditorCrono()

channel = "None"  # tracks the current serial port connected to the program
Active_technic = "None"  # tracks the current electrochemical technic and its parameters
Active_control = "None"  # tracks which actions are currently on going on the serial communication control panel
# Active_read = False
gain = bytes([6])
config = 0b00000000
trun: threading.Thread
ABORT = False
MAX_CURR = [0.150] # A. Max current

#
# Creates the main Menu
my_menu = Menu(root)

root.config(menu=my_menu)


mp = BooleanVar()
pp = BooleanVar()


""" Control panel """
# Creates the control buttons to control the serial communication
main_frame = Frame(root, bg="white")
main_frame.pack(side=LEFT, fill=BOTH)

# calculating icon size
main_frame.update()
total_height = main_frame.winfo_height()
n_icons = 10
icon_height = int(total_height/n_icons*0.55)
pady_split = int(icon_height*0.65)
pady_ = int(icon_height*0.20)
padx_ = int(icon_height*0.2)

f_control = Frame(main_frame, bg="white", width=main_frame.winfo_width())
f_control.pack(side=TOP, fill=BOTH, expand=True)

b_start = IconWidget(f_control, path=r"Icons\button_start.jpg", command=start_comsInthread, bg="white", size=(icon_height, icon_height))
b_start.pack(side=TOP, pady=pady_, padx=padx_)
ttm.ToolTip(widget=b_start, tip_text="Run")

b_stop = IconWidget(f_control, path=r"Icons\button_stop.jpg", command=stop_coms, bg="white", size=(icon_height, icon_height))
b_stop.pack(side=TOP, pady=(pady_, pady_split), padx=padx_)
b_stop['state'] = DISABLED
ttm.ToolTip(widget=b_stop, tip_text="Stop")

b_add_tap = IconWidget(f_control, path=r"Icons\button_tab.jpg", command=add_chart, bg="white", size=(icon_height, icon_height))
b_add_tap.pack(side=TOP, pady=(pady_, pady_split), padx=padx_)
ttm.ToolTip(widget=b_add_tap, tip_text="Add new tab")

b_conn = IconWidget(f_control, path=r"Icons\button_conn.jpg", command=connection, bg="white", size=(icon_height, icon_height))
b_conn.pack(side=TOP, pady=(pady_, pady_split), padx=padx_)
ttm.ToolTip(widget=b_conn, tip_text="Connect device")

b_chrono = IconWidget(f_control, path=r"Icons\chronoamperometry.jpg", command=lambda: MSE_Chrono.open(root, MAX_CURR, GLOBAL_EDITOR_TRACKER), bg="white", size=(icon_height, icon_height))
b_chrono.pack(side=TOP, pady=pady_, padx=padx_)
ttm.ToolTip(widget=b_chrono, tip_text="Edit Chronoamperometry")

b_poten = IconWidget(f_control, path=r"Icons\potentiometry.jpg", command=lambda: MSE.open(root, GLOBAL_EDITOR_TRACKER), bg="white", size=(icon_height, icon_height))
b_poten.pack(side=TOP, pady=(pady_, pady_split), padx=padx_)
ttm.ToolTip(widget=b_poten, tip_text="Edit Potentiometry")

b_cv = IconWidget(f_control, path=r"Icons\cv.jpg", command=lambda: CVMSE.open(root, GLOBAL_EDITOR_TRACKER), bg="white", size=(icon_height, icon_height))
b_cv.pack(side=TOP, pady=(pady_, pady_split), padx=padx_)
ttm.ToolTip(widget=b_poten, tip_text="Edit CV")

b_load = IconWidget(f_control, path=r"Icons\Load_data.jpg", command=load_from_file, bg="white", size=(icon_height, icon_height))
b_load.pack(side=TOP, pady=pady_, padx=padx_)
ttm.ToolTip(widget=b_load, tip_text="Load data")

b_save = IconWidget(f_control, path=r"Icons\save_data.jpg", command=save_elchem, bg="white", size=(icon_height, icon_height))
b_save.pack(side=TOP, pady=pady_, padx=padx_)
ttm.ToolTip(widget=b_save, tip_text="Save data")

b_xl = IconWidget(f_control, path=r"Icons\export_xl.jpg", command=export_to, bg="white", size=(icon_height, icon_height))
b_xl.pack(side=TOP, pady=(pady_, pady_split), padx=padx_)
ttm.ToolTip(widget=b_xl, tip_text="Export to excel")

b_settings = IconWidget(f_control, path=r"Icons\settings.jpg", command=set_prefs, bg="white", size=(icon_height, icon_height))
b_settings.pack(side=BOTTOM, pady=pady_, padx=padx_)
ttm.ToolTip(widget=b_xl, tip_text="Export to excel")


make_unique = BooleanVar()


""" Notebook """
# Creates the frame and tabs for data visualization in top
f_tabframe = Frame(root, padx=10, bg="whitesmoke")
f_tabframe.pack(side=LEFT, fill=BOTH, expand=True)

my_notebook = CostumeNoteBook(master=f_tabframe)
my_notebook.pack(side=LEFT, anchor="n", fill=BOTH, expand=True)

char_num = 1
Active_tab = my_notebook.add_costume_tab(label=f'Chart {char_num}')

""" TreView and details """
aux_frame = Frame(root, bg="white")
aux_frame.pack(fill=BOTH, expand=True)

para_label = Label(aux_frame, text='Select a line', bg="white", width=int(root.winfo_width()*0.02))

my_tree_menu = ttm.DetailsTree(aux_frame, para_label)
my_tree_menu.add_chart(Active_tab.chart, 'Chart'+str(char_num))



# Adding rigth mouse menu to treeView
tree_menu = ttm.RightMouse(my_tree_menu.tree)
tree_menu.add_item('Hide all',  my_tree_menu.hide_all)
tree_menu.add_item('Show all',  my_tree_menu.show_all)
tree_menu.add_item('Hide',  my_tree_menu.hide_line)
tree_menu.add_item('Show',  my_tree_menu.show_line)
tree_menu.add_item('Move line up', my_tree_menu.move_line_up)
tree_menu.add_item('Move line down', my_tree_menu.move_line_down)
tree_menu.add_item('Rename', my_tree_menu.rename_line)
tree_menu.add_item('Clear peaks', my_tree_menu.clear_peaks)
tree_menu.add_item('Delete', my_tree_menu.delete_line)


# Loading the widget view to the first tab
Active_tab.update_tree(my_tree_menu)


# Displaying the measure parameters
# f_control3 = LabelFrame(aux_frame, text='Parameters', bg="white")
# para_label = Label(f_control3, text='None', bg="white", width=22)
para_label.pack(side=TOP, fill=X)


# Creates a label that tells the user relevant information
main_status = Label(aux_frame, text="Connected to: None", bd=1, fg="grey", relief=SUNKEN)
main_status.pack(fill=X, side=BOTTOM, padx=padx_)

""" GLOBAL MAX CURRENT led"""
current_LED = StatusLED(aux_frame, status=True, text="Current")
current_LED.pack(side=BOTTOM, fill=X, padx=padx_)

device_LED = StatusLED(aux_frame, status=False, text="Device ready")
device_LED.pack(side=BOTTOM, fill=X, padx=padx_)


root.mainloop()
