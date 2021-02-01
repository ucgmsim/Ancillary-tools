"""
Author: Sirui Wang
Last edit: 1/18/2021
contact email: sirui_wang@outlook.com
"""

from collections.abc import Iterable


def bore_hole_filter(bore_dia):
    try:
        bore = int(bore_dia)
        return bore
    except ValueError:
        """if the borehole diameter in the data is not valid, assumes the bore_hole diameter to be 100, So that Cb 
        borehole correction factor is 1. 
        """
        return 100


def multi_depth_filter(depth):
    ID = None
    if isinstance(depth, Iterable):
        if max(depth) <= 5:
            ID = "Max-depth-less-than-5"
            # Data Error due to SPT test too shallow, depth too shallow, not representative
            return False, ID
        elif max(depth) - min(depth) <= 5:
            ID = "Depth-span-less-than-5"
            # Data Error due to SPT test to varied enough, not representative
            return False, ID
        else:
            return True, ID
    else:
        ID = "single-depth"
        # Data Error due to only having 1 SPT test result, not representative
        return False, ID


def zero_value_filter(NValues):
    if isinstance(NValues, Iterable):
        if any(NValues == 0):
            # When spt result in 0, the Vs Correlation Fails, hence ignore any value that is 0
            return False
        else:
            return True
    else:
        if NValues == 0:
            return False
        else:
            return True


def detailed_data(locations, spt, key):
    data_hammer_type = locations.HammerType.at[key]
    data_bore_dia = locations.BoreholeDiameter.at[key]
    data_rod_length = spt["Depth"]
    Ns = spt["NValue"]
    borehole_dia_invalid = bore_hole_filter(data_bore_dia)
    depth_validity, depth_failure_ID = multi_depth_filter(data_rod_length)
    zero_value = zero_value_filter(Ns)
    # depth_failure_ID shows more detailed failure reason
    validate = [depth_validity, depth_failure_ID, zero_value]
    return validate, Ns, data_hammer_type, borehole_dia_invalid, data_rod_length


def remove_invalid_data(log, key, spt_locations_data, spt_df):
    validate, NValues, data_hammer_type, borehole_dia, rod_length = detailed_data(spt_locations_data, spt_df, key)
    depth_valid, depth_failure_ID, zero_value = validate
    valid_to_continue = True
    spt_locations_data.BoreholeDiameter.at[key] = borehole_dia
    if not zero_value and not depth_valid:
        log.write((str(key)) + ',' + "zero value spt test and {}".format(depth_failure_ID) + '\n')
        valid_to_continue = False
    elif not depth_valid:
        log.write((str(key) + ',' + depth_failure_ID + '\n'))
        valid_to_continue = False
    elif not zero_value:
        log.write((str(key)) + ',' + "zero value spt test" + '\n')
        valid_to_continue = False
    if valid_to_continue:
        spt_df.query("Depth <= 29", inplace=True)
        if spt_df is None:
            log.write((str(key)) + ',' + "Entire dataset exceed 29m depth" + '\n')
            valid_to_continue = False
    if valid_to_continue:
        return spt_df


