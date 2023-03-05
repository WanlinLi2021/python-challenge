import csv
from pathlib import Path
import datetime



# convert string to a datetime format
def to_datetime_format(date_str):
    date_time_obj = datetime.datetime.strptime(date_str, '%b-%Y')
    return date_time_obj.date()

# convert datetime to a string
def date_to_string(date_time):
    return date_time.strftime('%b') + '-' + date_time.strftime('%Y')

# print and write text of result
def print_write_result(result,output_file):
    with open(output_file,'a') as f:
        f.write(result + "\n" + "\n")
        print(result)


def main(budget_path, output_file):
    # initiate a dictionary for budget data
    budget_dct = {}
    # Write CSV file in dictionary
    with open(budget_path,"r") as f:
        f_reader = csv.DictReader(f,delimiter=",")
        for row in f_reader:
            #print(to_datetime_format(row['Date']),row['Profit/Losses'])   
            budget_dct[to_datetime_format(row['Date'])] = int(row['Profit/Losses'])   # convert strings to date format and integer format separately

    # sort dictionary by key
    budget_sorted = dict(sorted(budget_dct.items(), key = lambda item: item[0]))

    # Calculate changes
    previous = list(budget_sorted.values())[:-1]
    current = list(budget_sorted.values())[1:]
    change = [y-x for y, x in zip(current, previous)]

    

    # write header
    header = "Financial Analysis \n \n---------------------------- \n"
    print_write_result(header,output_file)

    # Total Months
    month_num = f"Total Months: {len(budget_sorted)}"
    print_write_result(month_num,output_file)

    # Tatal 
    total = f"Total: ${sum(budget_sorted.values())}"
    print_write_result(total,output_file)

    # Average Change
    mean_change = f"Average  Change: ${round(sum(change)/len(change),2)}"
    print_write_result(mean_change,output_file)

    # Greatest Increase in Profits
    increase = max(change)
    index = change.index(increase)
    date_time = list(budget_sorted.keys())[index + 1]
    str_date_time = date_to_string(date_time)
    increase_text = f"Greatest Increase in Profits: {str_date_time} (${increase})"
    print_write_result(increase_text,output_file)

    # Greatest Decrease in Profits
    decrease = min(change)
    index = change.index(decrease)
    date_time = list(budget_sorted.keys())[index + 1]
    str_date_time = date_to_string(date_time)
    decrease_text = f"Greatest Decrease in Profits: {str_date_time} (${decrease})"
    print_write_result(decrease_text,output_file)

if __name__ == "__main__":
    # input path
    budget_path = Path("./Resources/budget_data.csv")
    # output path
    output_file = Path("./budget_report.txt")
    main(budget_path, output_file)