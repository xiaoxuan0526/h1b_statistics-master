import sys
import csv

csv.field_size_limit(2000000000)

# get path
input_path = sys.argv[1]
output_path_occupation= sys.argv[2]
output_path_state = sys.argv[3]

# Read data, then each item would represent one line in csv file
csv_File = open(input_path, 'r')
reader =csv.reader(csv_File)

occupation_dict = {}
state_dict = {}

# Raw data cleaning(decompose and integrate)
reader_index_exception = -1
reader_index = -1
for item in reader:
    reader_index += 1

    # Get the string of all the headers
    if reader_index == 0:
        header = item[0]  
        for i in range(1,len(item)):
            header += ","     # The words in text files would be separated into two table cells by comma in csv file
            header += item[i]

        # Split the string of headers into a list
        header = header.split(sep=";")

        # Get the index of headers related to the goal of this project
        case_status_index = header.index('CASE_STATUS')
        occupation_index = header.index('SOC_NAME')
        state_index = header.index('WORKSITE_STATE')
        visa_class_index = header.index('VISA_CLASS')

    # Get cases
    elif len(item) > 0: #not null row
        # Get the string of content of cases
        case_info_string_raw = item[0]
        for i in range(1,len(item)):
            case_info_string_raw += ","  # The words in text files would be separated into two table cells by comma in csv file
            case_info_string_raw += item[i]

        # Rrmove the interference symbols(" and ') from the string
        case_info_string_raw = case_info_string_raw.replace('\'','')
        case_info_string_clean = case_info_string_raw.replace('\"','')

        # Decompose the string to separate cases
        case_info_list = case_info_string_clean.split(sep=";")
        
        # Some cases were merged by "\n", decompose them into multiple cases
        new_case_info_list = []
        if len(case_info_list) == len(header):
            new_case_info_list.append(case_info_list)   
        if len(case_info_list) > len(header):
            case_info_list_temp = case_info_string_clean.split(sep="\n")
            for case in case_info_list_temp:
                new_case_info_list.append(case.split(sep=";"))

        # Filt out H-1B cases that are certified. Create two dictionaries count the number for each occupation and state
        
        for case_info in new_case_info_list: 
            if case_info[case_status_index] == 'CERTIFIED' and 'H-1B' in case_info[visa_class_index] :
                if case_info[occupation_index] in occupation_dict.keys():
                    occupation_dict[case_info[occupation_index]] += 1
                else:
                    occupation_dict[case_info[occupation_index]] = 1

                if case_info[state_index] in state_dict.keys():
                    state_dict[case_info[state_index]] += 1
                else:
                    state_dict[case_info[state_index]] = 1

# The codes above can also be abstracted as a function to count the top classes for any attribute. 


# Define a function which sort the two dictionaries by NUMBER_CERTIFIED_APPLICATIONS and then alphabetically by TOP_OCCUPATIONS
# And then count percentage
def GetTop10(dict):
    sorted_dict = sorted(dict.items(), key=lambda x: (-x[1],x[0]))
    sorted_results = []
    for item in sorted_dict:
        item = list(item)
        item.append(format(item[1]/sum(dict.values()),'.1%'))
        item[1] = str(item[1])

        new_item = item[0]
        for i in range(1, len(item)):
            new_item += ";" 
            new_item += item[i]
        
        sorted_results.append(new_item)

    if len(sorted_results) <= 10:
        return sorted_results
    else:
        return sorted_results[0:10]

occupation_results = GetTop10(occupation_dict)
state_results = GetTop10(state_dict)


# Write the results into output file
def WriteOutput(output_path, attribute_results, header_names):
    output_file = open(output_path,'w')
    output_file.write(header_names+'\n')
    for one_category in attribute_results:
        output_file.write(one_category + "\n")   
    output_file.close()

WriteOutput(output_path_occupation, occupation_results, 'TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE')
WriteOutput(output_path_state, state_results, 'TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE')
    















    
    








