This software was developed using **Python 3.8**.
The hardware was designed using **Kicad 7.0**.


# About

This repository provides a cheap tool, the OpenMux, a homemade super cheap multiplexor adaptor for the EmStat4 potentiostat ([PalmSens](https://www.palmsens.com/product/emstat4m/)). The adptor was integrated with the potentiostat using MethodScript protocol provided by the manufacturer.

This tool is composed by two modules, the hardware module an Graphical interface to work with.

The schematic and gerber files can be found in Hardware folder of this repository.
An Graphical User Interface was built in python to operate this adaptor module, present in Application folder


![Multiplexer Adaptor for EmStat4](MuxAdaptor.PNG)
![GUI](GUI.PNG)


# Costs

The costs for the elctrical components are arround 40€ :) :
- 3x 10€ (ADG1408YRUZ, [Muxtiplexers](https://www.digikey.pt/en/products/detail/analog-devices-inc/ADG1408YRUZ/1206709?msockid=3b4fa386dcfd658b16a1b206dd9a641a)); 
- 3x 1.60€ (Phoenix therminal block 8pos, [Therminals](https://www.digikey.pt/en/products/detail/phoenix-contact/1984675/950853)); 
- 3x 0.14€ (Pin header 12pos, [Male Pin header](https://www.digikey.pt/en/products/detail/adam-tech/PH1-12-UA/9830395))
- 3x 0.49€ (Pin header 12pos, [Female Pin header](https://www.digikey.pt/en/products/detail/w%C3%BCrth-elektronik/61301211821/16608531))



# Get Started

1º Download the repository

2º Build the adaptor (OpenMux)
 - Send the gerber files for fabrication at any PCB manufacturer (JLCPCB, PCBway, ...)
 - Oder the components and assembel

3º Install the software to run the Graphical application (The Emstat alone can be used with this environment, play whit it while you to wait for the PCB's to arrive )

4º Mount the OpenhMux adaptor onto the EmStat4

5º Launch the application and connect the modified device to the computer via USB




# Hardware
The schematics and pcb design were developed using Kicad. The gerber files for production are located in Hardware/production/Mux_Module.zip, and were generated using Kicad fabrication toolkit plugin.



# Running the Application

1. Create a Python virtual environment inside the `Application` directory:

```bash
...\OpenMux> cd Application
...\Application> python -m venv venv
```

2. Initialize the virtual environment:

```bash
...\Application> venv\Scripts\activate.bat
```

3. Install the dependencies:

```bash
(venv) ...\Application> pip install -r requirements.txt
```

4. Start the application:

```bash
(venv) ...\Application> python EL_MUX.py
```


# Building an Executable

1. Activate the Python environment:
```bash
...\Application> venv\Scripts\activate.bat
```

2. Run the pyinstaller command:

```bash
(venv) ...\Application> pyinstaller -w -p "venv\Lib\site-packages" -i Icons\group-30_116053.ico --onefile EL_MUX.py
```

This will generate:

A .spec file

Two additional directories: build/ and dist/

The dist/ directory contains the EL_MUX.exe (executable).
⚠️ Note: This executable still depends on the following folders:

MethodScript-firmware/

Icons/

Therefore, move EL_MUX.exe to the Application/ directory and ensure those folders are present there. Afterward, the build/ and dist/ directories are safe to be deleted.