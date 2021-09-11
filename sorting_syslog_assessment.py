#!/usr/bin/env python3
import re
import os
import csv
from collections import Counter

Error_Count = {}
Per_user = {}
templist_error = []
templist_info = []

# Creates two dictionaries for errors and count and errors and info per user
with open('syslog.txt') as syslog:
    for error_msg in syslog:
        if "ERROR" in error_msg:
            start = error_msg.index('ERROR') + 6
            end = error_msg.index('(') - 1 
            start2 = error_msg.index('(') + 1
            end2 = error_msg.index(')')
            result = error_msg[start:end]
            result2 = error_msg[start2:end2]
            templist_error.append(result)
            templist_info.append(result2 + ' ERROR')
        if "INFO" in error_msg:
            start = error_msg.index('(') + 1
            end = error_msg.index(')')
            result = error_msg[start:end]
            templist_info.append(result + ' INFO')
    # Counts
    Error_Count = Counter(templist_error)
    Per_user = Counter(templist_info)


# Per_user dictionary needs to be changed to the format needed for the table
Error_Count_List = list(Error_Count.items())
Per_user_list = Per_user.items()
Per_user_list_sorted = sorted(Per_user_list)
Per_user_list_temp = []
Per_user_list2 = {}

# Removes 'INFO' and 'ERROR and creates a list with the format, User, error count, info count
for line in Per_user_list_sorted:
    amount_info = line[1]
    user_info = line[0]
    amount_error = line[1]
    user_error = line[0]
    if 'ERROR' in user_info:
        Per_user_list_temp.append(user_error[:-6])
        Per_user_list_temp.append(amount_error)
    if 'INFO' in user_info:
        Per_user_list_temp.append(amount_info)


# Iterates through the new list and adds a 0 to the INFO count for any user without an INFO count
# Also adds new lines characters

loop_counter = 0
Per_user_list_temp2 = []

for line in Per_user_list_temp:
    loop_counter += 1
    if loop_counter > 0 and loop_counter % 3 == 0 and type(line) == int:
        Per_user_list_temp2.append(line)
        Per_user_list_temp2.append('\n')
        continue
    if loop_counter > 0 and loop_counter % 3 == 0 and type(line) == str:
        Per_user_list_temp2.append(0)
        Per_user_list_temp2.append('\n')
        Per_user_list_temp2.append(line)
        loop_counter =- 1
    else:
        Per_user_list_temp2.append(line)
Per_user_list_temp2.append(0)

# Two csv files to be generated from the arrays
with open('Error_Count.csv', 'w') as error_csv:
    for key in Error_Count.keys():
        error_csv.write('%s, %s\n'%(key,Error_Count[key]))


with open('User_Counts.csv', 'w') as user_csv:
    user_csv.write(','.join(str(item) for item in Per_user_list_temp2))





  
        
 
   
      
   

