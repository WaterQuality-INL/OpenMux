# OpenMux Overview
OpenMux is an extension of the research conducted within the framework of the [OPTIRAS project](https://www.optiras.org/), particularly from the [Water Quality Group](https://inl.int/espina-research-group/) at the [International Iberian Nanotechnology Laboratory](https://inl.int/).
We aim to provide an open-source multiplexer adaptor for [EmStat4 LR/HR potentiostat](https://www.palmsens.com/product/emstat4m/) by combining hardware design with software integration. This innovation enhances experimental efficiency and scalability for researchers and engineers alike, paving the way for applications such as multiplexed electrochemical sensing, automated assay platforms, and integrated IoT-based field monitoring systems for environmental, biomedical, or industrial electrochemical analysis.

---

# About

This repository provides **OpenMux**, a homemade and cost-effective multiplexer adaptor for the EmStat4 OEM module from Palmsens. 
The adaptor is integrated with the potentiostat using the [**MethodScript**]([https://github.com/PalmSens](https://www.palmsens.com/methodscript/)) protocol provided by the manufacturer.

The system consists of two main modules:  

1. **Hardware Module** – the multiplexer adaptor itself (figure 1), whose schematics and PCB layout were developed using KiCad 7.0. Hardware schematics and Gerber files can be found in the `Hardware/` folder.  
2. **Graphical User Interface (GUI)** – a graphical user interface (figure 2) to control the adaptor, implemented in Python 3.8. The GUI is located in the `Application/`  folder.


<div align="center">
  <img src="MuxAdaptor.PNG" alt="Multiplexer Adaptor for EmStat4" width="400"/>
  <p><em>Figure 1: OpenMux adaptor for EmStat4</em></p>
</div>

<div align="center">
  <img src="GUI.PNG" alt="Graphical User Interface" width="400"/>
  <p><em>Figure 2: OpenMux GUI</em></p>
</div>


The application of OpenMux for electrochemical methods is described in the scientific literature [1].


---

# Costs

The approximate cost of the electronic components (excluding the PCB) is around **€40**. Key components include:

| Quantity | Component | Price | Link |
|----------|-----------|-------|------|
| 3x       | ADG1408YRUZ Multiplexer | €10 | [Digi-Key](https://www.digikey.pt/en/products/detail/analog-devices-inc/ADG1408YRUZ/1206709?msockid=3b4fa386dcfd658b16a1b206dd9a641a) |
| 3x       | Phoenix Terminal Block 8-pos | €1.60 | [Digi-Key](https://www.digikey.pt/en/products/detail/phoenix-contact/1984675/950853) |
| 3x       | Male Pin Header 12-pos | €0.14 | [Digi-Key](https://www.digikey.pt/en/products/detail/adam-tech/PH1-12-UA/9830395) |
| 3x       | Female Pin Header 12-pos | €0.49 | [Digi-Key](https://www.digikey.pt/en/products/detail/w%C3%BCrth-elektronik/61301211821/16608531) |

---



# Getting Started

1. **Download the repository**  

2. **Build the OpenMux adaptor**  
   - Send the Gerber files for fabrication to any PCB manufacturer (e.g., JLCPCB, PCBWay).  
   - Order the components and assemble the board.  

3. **Install the software**  
   - The OpenMux is not necessary to start using the GUI (whitout the multiplexing features). Just start it, connect the potentiostat to the computer and press play.

4. **Mount the OpenMux adaptor** onto the EmStat4.  

5. **Launch the GUI** and connect the modified device to your computer via USB.

---




# Hardware

The schematics and PCB design were developed using **KiCad**.  

- Gerber files for production can be found in:  `Hardware/production/Mux_Module.zip`
- These files were generated using the **KiCad Fabrication Toolkit** plugin.  

---



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

Therefore, move EL_MUX.exe to the Application/ directory and ensure those folders are present there. Afterwards, the build/ and dist/ directories are safe to be deleted.

---

# License

- Software (Application/) is licensed under MIT License.  
- Hardware (Hardware/) is licensed under CC BY 4.0.

---

# Contributors
- Samuel Silva*

Supervision:
- Álvaro Geraldes**

Contacts:
- Samuel Silva, samuel.silva@inl.int
- Álvaro Geraldes, alvaro.geraldes@inl.int
  
* Water Quality Group, ** Systems Engineering Group, International Iberian Nanotechnology Laboratory (INL)

---

# Acknowledgement
To PalmSens for MethodScript
To OPTIRAS project

---

# References

[1] Olesia Dudik, Renato L. Gil, Raquel B. Queirós. Critical assessment of different ion-to-electron transducers in modified screen-printed electrodes for potentiometric lithium sensing. Microchemical Journal 2025, 215, 114195, https://doi.org/10.1016/j.microc.2025.114195
