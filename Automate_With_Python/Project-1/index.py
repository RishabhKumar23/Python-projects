#NOTE - Table Extraction - Extract Tables from Websites
import pandas as ps

#to read html file => paste website link here
file = ps.read_csv('https://www.football-data.co.uk/mmz4281/2122/E0.csv')

file.rename(columns={
    #select whatever column yoou want to change
    
    # "col_name": "new_col_name",
    # "col_name": "new_col_name",
    
})
# print(len(file))

