This software was developed using **Python 3.8**.
The hardware was designed using **Kicad 7.0**.


# About

This repository provides the necessary resources to build a home amde multiplexor adaptor for the EmStat4 potentiostat (PalmSens, [text](https://www.palmsens.com/product/emstat4m/))

The schematic and gerber files can be found in Hardware folder of this repository.
An Graphical User Interface was built in python to operate this adaptor module, present in Application


![Multiplexer Adaptor for EmStat4](MuxAdaptor.PNG)



# Get Started




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