Problem:

Create a mechanism to analyze the data from department of labor and calculate two metrics: **Top 10 Occupations** and **Top 10 States** for **certified** **H-1B** visa applications.

Approach:

1. Read the raw data from the csv file.
2. Preprocessing to get the structural data and remove the inference symbol.
3. Create two dictionaries which count the number of each category for the occupation and state.
4. Sort the dictionaries. Transfer the dictionary to list and count the percentage for each category.   
5. Write the text results into the output file.

Running Instruction:

The csv file "h1b_input" is in the `input` directory. Running the `run.sh` script. The two text results would be in the `output` folder.



