"""
Contains helper functions to construct instructions
"""

from pycqed.utilities.general import int_to_bin


def trigg_cw(channel):
    cw = ['0']*7
    cw[channel-1] = '1'
    cw = ''.join(cw)
    return cw


def qwg_cw_trigger(codeword,
                   trigger_channel=1, cw_channels=[2, 3, 4]):

    cw = int_to_bin(codeword, w=len(cw_channels), lsb_last=False)
    cw_marker = ['0']*7
    for i, cw_bit in enumerate(cw):
        cw_marker[cw_channels[i]-1] = cw_bit
    cw_marker = ''.join(cw_marker)

    trigger = trigg_cw(trigger_channel)
    instr = 'trigger {}, 1\n'.format(cw_marker)
    instr += 'wait 1\n'

    cw_ready_trigg = bin_add_cw_w7(trigger, cw_marker)
    instr += 'trigger {}, 2\n'.format(cw_ready_trigg)
    instr += 'wait 2\n'

    return instr


def trigg_ch_to_instr(channel, duration):
    """
    Specify a trigger channel to be triggered and returns the appropriate
    qumis instruction
        channel:  int  between 1 and 7
        duration: int  duration in clocks, >1
    """
    cw = trigg_cw(channel)

    instr = 'trigger {}, {} \n'.format(cw, duration)
    instr += 'wait {}\n'.format(duration)
    return instr


def bin_add_cw_w7(a, b):
    """
    Width 7 binary addition of two codeword strings
    """
    c = (int(a, 2) + int(b, 2))
    return '{0:07b}'.format(c)