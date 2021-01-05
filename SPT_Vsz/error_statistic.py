import argparse

"""Input File location"""
"""
# Edit File location by -> run -> Edit Configuration -> Parameters
parser = argparse.ArgumentParser()
parser.add_argument("--output_path", "-o", default="outputs/output.csv", help="Input path to save the output csv file")
# args variables
args = parser.parse_args()
output_path = args.output_path"""


with open('outputs/invalid_locations.txt', 'r') as log:
    lines = log.readlines()
    both_error_log_max = 0
    both_error_log_span = 0
    both_error_log_single = 0
    zero_value_log = 0
    max_depth_log = 0
    depth_span_log = 0
    single_depth_log = 0
    entire_data_too_deep_log = 0
    fail2count = 0

    for line in lines:
        print(line)
        CombinedName, ErrorName = line.split(",")
        print(ErrorName)
        if "zero value spt test and Depth-span-less-than-5" in ErrorName:
            both_error_log_span += 1
        elif "zero value spt test and Max-depth-less-than-5" in ErrorName:
            both_error_log_max += 1
        elif "zero value spt test and single-depth" in ErrorName:
            both_error_log_single += 1
        elif "zero value spt test" in ErrorName:
            zero_value_log += 1
        elif "Max-depth-less-than-5" in ErrorName:
            max_depth_log += 1
        elif "Depth-span-less-than-5" in ErrorName:
            depth_span_log += 1
        elif "single-depth" in ErrorName:
            single_depth_log += 1
        elif "Entire dataset exceed 29m depth" in ErrorName:
            entire_data_too_deep_log += 1
        else:
            fail2count += 1
    TotalError = both_error_log_single + both_error_log_max + both_error_log_span + zero_value_log + max_depth_log + depth_span_log + single_depth_log + entire_data_too_deep_log
    print("fail to count = {}".format(fail2count))
    print("{} data entries are invalid".format(TotalError))
    print("{} are due to max depth less than 5 m and zero value spt test".format(both_error_log_max))
    print("{} are due to depth span less than 5 m and zero value spt test".format(both_error_log_span))
    print("{} are due to single value depth and zero value spt test".format(both_error_log_single))
    print("{} are due to zero value spt test".format(zero_value_log))
    print("{} are due to depth span less than 5 m".format(depth_span_log))
    print("{} are due to maximum depth is below 5 m".format(max_depth_log))
    print("{} are due to single depth result".format(single_depth_log))
    print("{} are due to entire dataset exceed 29 m depth".format(entire_data_too_deep_log))
