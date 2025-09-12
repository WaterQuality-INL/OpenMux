"""
Switching EmStat4 GPIO pins output values for MUX channel selection. Enabling pseudo parallel measurements.
Example code for implementation):

        # Switching channels
        for i, channel in enumerate(MUX_CHANNELs):
            change_channel(list(MUX_CHANNELs.values())[i-1], MUX_CHANNELs[channel])
"""

# Channel bitmap according to MUX ADG408 datasheet
MUX_CHANNELs = {'ch1': '0b0000',
                'ch2': '0b1000',
                'ch3': '0b0100',
                'ch4': '0b1100',
                'ch5': '0b0010',
                'ch6': '0b1010',
                'ch7': '0b0110',
                'ch8': '0b1110'}


def get_script(path='MethodScripts-firmware/PotentiometryPtGPIOAuto.mscr'):
    """Getting methodScript for 'set_gpio' cmd edting"""
    with open(path, 'r') as file:
        return file.read()


def store_script(script, path='MethodScripts-firmware/PotentiometryPtGPIOAuto_final.mscr'):
    """Saving edited method in methodScript file"""
    with open(path, 'w') as file:
        file.write(script)


def change_channel(new_mask, old_mask=None):
    """
    Changing GPIO levels to select channel in MUX"
    :param old_mask: str
        Previous bitmap e.g '0b1111' to be replaced with new 
    :param new_mask: str
        next bitmap. to update the new channel in the MUX module
    :return: 
    """""
    script = get_script()
    # s = script.replace(old_mask, new_mask)
    s = script.replace("0bXXXX", new_mask)
    store_script(s)

