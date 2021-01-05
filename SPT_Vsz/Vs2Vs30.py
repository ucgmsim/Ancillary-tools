from Ancillary_tools.CPT_Vsz_Vs30 import calculations


def convert(spt_at_this_location, location):
    latitude = location["NZTM_Y"]
    longitude = location["NZTM_X"]
    depth_at_i = spt_at_this_location["Depth"]
    vs_at_i = spt_at_this_location["Vs"]
    Vsz, max_depth = calculations.compute_vsz_from_vs(vs_at_i, depth_at_i)
    Vs30 = calculations.vsz_to_vs30(Vsz, depth_at_i)
    return latitude, longitude, Vs30
