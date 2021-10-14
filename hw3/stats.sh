#!/bin/bash

# accepts as a command line argument a tweet file
if [[ $# -eq 0 ]]
then
	echo "Error: No tweet file given.";
	echo "Usage: ./stats.sh <test_file>";
	exit 1;
fi

# if the parameter does not represent a file
if [[ ! -f $1 ]]
then
	echo "Error: File '$1' does not exist.";
	echo "Usage: ./stats.sh <test_file>";
	exit 1;
fi

# print an error message if the input file is smaller than 10,000 lines
line_count=$(wc -l < $1);

if [[ $line_count -lt 10000 ]]
then
	echo "Error: File contains less than 10,000 lines.";
	exit 1;
fi

# print the number of lines in the file
echo $line_count;

# print the first line of the file (i.e. the header row)
echo $(head -1 $1);

# print the number of lines in the last 10,000 rows of the file that contain the string "potus" (case-insensitive)
potus=$(tail -10000 $1 | grep -ic 'potus');
echo $potus;

# of rows 100-200 (inclusive), how many lines contain the word "fake"
fake=$(sed -n -e '100,200p' $1 | grep -c '\bfake\b');
echo $fake;
