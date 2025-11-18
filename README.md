
# OpenMux Overview
OpenMux is an extension of the research conducted within the framework of the [OPTIRAS project](https://www.optiras.org/), particularly from the [Water Quality Group](https://inl.int/espina-research-group/) at the [International Iberian Nanotechnology Laboratory](https://inl.int/).
We aim to provide an open-source multiplexer adaptor for [EmStat4 LR/HR potentiostat](https://www.palmsens.com/product/emstat4m/) by combining hardware design with software integration. This innovation enhances experimental efficiency and scalability for researchers and engineers at an exceptionally low cost, paving the way for applications such as multiplexed electrochemical sensing, automated assay platforms, and integrated IoT-based field monitoring systems for environmental, biomedical, or industrial electrochemical analysis.

---

## About

This repository provides **OpenMux**, a homemade and cost-effective multiplexer adapter for the EmStat4 OEM module from Palmsens. 
The adapter is integrated with the potentiostat using the [**MethodScript**]([https://github.com/PalmSens](https://www.palmsens.com/methodscript/)) protocol provided by the manufacturer.

The system consists of two main modules:  

1. **Hardware Module** – the multiplexer adaptor itself (figure 1), whose schematics and PCB layout were developed using KiCad 7.0. Schematic, layout, and Gerber files can be found in the `Hardware/` folder (see schematic.pdf and layout.pdf for pictures).  
2. **Graphical User Interface (GUI)** – a graphical user interface (figure 2) to control the adaptor, implemented in Python 3.8. The GUI is located in the `Application/`  folder.


<div align="center">
  <img src="MuxAdaptor.PNG" alt="Multiplexer Adaptor for EmStat4" width="400"/>
  <p><em>Figure 1: OpenMux adapter for EmStat4</em></p>
</div>

<div align="center">
  <img src="GUI.PNG" alt="Graphical User Interface" width="400"/>
  <p><em>Figure 2: OpenMux GUI</em></p>
</div>


The application of OpenMux for electrochemical methods is described in the scientific literature [1].


## Who is this for?

- Electrochemists who want a cheap and modular, open platform for integrating sensors and data backends for:
   - Environmental or industrial monitoring applications
   - Scaling up sensor optimisation and/or preparation in the lab
  
---

## Costs

The approximate cost of the electronic components (excluding the PCB) is around **€40**. Key components include:

| Quantity | Component | Price | Link |
|----------|-----------|-------|------|
| 3x       | ADG1408YRUZ Multiplexer | €10 | [Digi-Key](https://www.digikey.pt/en/products/detail/analog-devices-inc/ADG1408YRUZ/1206709?msockid=3b4fa386dcfd658b16a1b206dd9a641a) |
| 3x       | Phoenix Terminal Block 8-pos | €1.60 | [Digi-Key](https://www.digikey.pt/en/products/detail/phoenix-contact/1984675/950853) |
| 3x       | Male Pin Header 12-pos | €0.14 | [Digi-Key](https://www.digikey.pt/en/products/detail/adam-tech/PH1-12-UA/9830395) |
| 3x       | Female Pin Header 12-pos | €0.49 | [Digi-Key](https://www.digikey.pt/en/products/detail/w%C3%BCrth-elektronik/61301211821/16608531) |

---

## Getting Started

1) Clone or download the repository 
```bash
git clone https://github.com/WaterQuality-INL/OpenMux.git
cd OpenMux
```

2) Hardware and production
- Gerber files for production: `Hardware/production/Mux_Module.zip`
- Schematics and PCB: in `Hardware/` (KiCad 7.x)
- Fabricate the PCB (JLCPCB, PCBWay, etc.), order components, and assemble.

3) Software requirements
- Python 3.8 or newer (3.8–3.11 recommended)
- OS: Windows, Linux, or macOS (GUI tested on Windows; Linux/macOS supported)
- The Application uses `MethodScript-firmware/` and `Icons/` folders; these must be present when running the packaged executable (see Packaging below).

4) Run the GUI (development)

Windows (cmd / PowerShell)
```bash
cd Application
python -m venv venv
venv\Scripts\activate.bat    # PowerShell: venv\Scripts\Activate.ps1
pip install -r requirements.txt
python EL_MUX.py
```

Linux / macOS
```bash
cd Application
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 EL_MUX.py
```

5) OPTIONAL: Packaging (creating an executable)

Alternatively, an executable file can also be created, allowing this application to run in computers where python is not installed.
```bash
cd Application
venv\Scripts\activate.bat
pyinstaller -w -p "venv\Lib\site-packages" -i Icons/group-30_116053.ico --onefile EL_MUX.py
```

Notes:
- The produced executable still depends on the folders `MethodScript-firmware/` and `Icons/`. Place `EL_MUX.exe` into `Application/` alongside those folders before running.
- After verifying the executable works, you can remove the `build/` and `dist/` directories.

---

## Troubleshooting

- If the GUI cannot find the EmStat4 device, verify the USB/serial connection and port name.
- Ensure the virtual environment is activated and dependencies installed.
- For packaging issues, build the executable on the target OS (pyinstaller builds are OS-specific).

---


## License

- Software (Application/) is licensed under MIT License.  
- Hardware (Hardware/) is licensed under CC BY 4.0.

---

## Contributors
- Samuel Silva*

Supervision:
- Álvaro Geraldes**

Contacts:
- Samuel Silva, samuel.silva@inl.int
- Álvaro Geraldes, alvaro.geraldes@inl.int

*Water Quality Group, **Systems Engineering Group, International Iberian Nanotechnology Laboratory (INL)

---

## Acknowledgement
To PalmSens for MethodScript

This work is an extension of the research funded by EEA (European Economic Area) Grants Portugal through the funded project PT-INN-0076—OPTIRAS.
 

---

## References

[1] Olesia Dudik, Renato L. Gil, Raquel B. Queirós. Critical assessment of different ion-to-electron transducers in modified screen-printed electrodes for potentiometric lithium sensing. Microchemical Journal 2025, 215, 114195, https://doi.org/10.1016/j.microc.2025.114195
