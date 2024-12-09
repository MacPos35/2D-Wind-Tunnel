import pandas as pd 
 
tsv_file='Cp_near.tsv'
 
# reading given tsv file
csv_table=pd.read_table(tsv_file,sep='\t')
 
# converting tsv file into csv
csv_table.to_csv('Cp_near.csv',index=False)