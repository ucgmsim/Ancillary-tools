

def all_variables(hammer_type, bore_dia, rod_length):
    """
    :param hammer_type:
    :param bore_dia:
    :param rod_length:
    :return: return variables in a tuple with order of Ce, Cb, Cr,Cs
    """
    Ce = get_Ce(hammer_type)
    Cr = get_Cr(int(rod_length))
    Cb = get_Cb(int(bore_dia))
    Cs = get_Cs()
    return Ce, Cb, Cr, Cs


def get_Ce(hammer_type):
    """
    Ce is the energy correction factor which depends mainly on the way that hammer is lifted and released.
    Some typical values are presented on the table below (after Skempton, 1986)
    :param location: spt location data
    :return: Ce value
    """
    if hammer_type in ['Auto']:
        # range 0.8 to 1.3
        Ce = 0.8
    else:
        # for doughnut hammer range 0.5 to 1.0
        Ce = 0.5
        # safety hammer ignored, it has range of 0.7 to 1.2
    return Ce



def get_Cb(bore_dia):
    """
    Cb is the bore-hole diameter correction factor and its is set according to the selected diameter from the drop
    down list.(Skempton, 1986)
    The borehole is either within range of 65-115, 150, or 200. if the diameter is not
    correctly recorded, assume they are 100 so that the Cb factor is 1. if diameter between 115 to 200 and not 150,
    assume its 150 so that Cb = 1.05
    :param borehole diameter
    :return: Cb
    """
    if bore_dia>= 65 and bore_dia<= 115:
        Cb = 1
        return Cb
    elif bore_dia == 150:
        Cb = 1.05
        return Cb
    elif bore_dia == 200:
        Cb = 1.15
        return Cb
    else:
        return 1.05#####


def get_Cr(rod_length):
    """
    Cr is the rod length correction factor which depends on the total length of the drill rod. The following values
    are from Youd et al.(2001)

    it is essentially the depth that has been drilled as recorded in Spt data
    :param rod_length:
    :return:Cr
    """
    if rod_length < 3:
        Cr = 0.75
    elif rod_length >= 3 and rod_length < 4:
        Cr = 0.8
    elif rod_length >= 4 and rod_length < 6:
        Cr = 0.85
    elif rod_length >= 6 and rod_length < 10:
        Cr = 0.95
    elif rod_length >= 10 and rod_length < 30:
        Cr = 1
    else:
        Cr = 1
    return Cr


def get_Cs():
    """
    Cs is the liner correction factor and its value depends on the sampler used to perform the test.
    The split spoon sampler may contain liner or not. The Cs value for the sampler with liners is 1.00
    while for samplers without liners value ranges from 1.10 to 1.30.
    (from Seed et al. 1984, equation by Seed et al. 2001)
    # equations for Split spoon sampler with room for liners.
    Cs = 1.1 for (N1)60 <= 10
    Cs = 1 + (N1)60/100 for 10 <= (N1)60<=30
    Cs = 1.3 for (N1)60 ?= 30

    Since the location data does not contain useful information to determine a correct Cs value, it is assumed to be 1
    Further update may be required if more information is provided in location data
    :return: Cs coefficient
    """
    Cs = 1
    return Cs
