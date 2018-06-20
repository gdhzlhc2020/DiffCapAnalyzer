import pandas as pd
import pandas.io.sql as pd_sql
import sqlite3 as sql

def update_database_newtable(df, upload_filename, database_name):

    #add df into sqlite database as table
    con = sql.connect(database_name)
    c = con.cursor()
    df.to_sql(upload_filename, con, if_exists="replace")
    return

def get_file_from_database(name, database):
	con = sql.connect(database)
	c = con.cursor()
	names_list = []
	for row in c.execute("""SELECT name FROM sqlite_master WHERE type='table'""" ): 
		names_list.append(row[0])
	if name in names_list: 
		# print('That file exists in the database')
		df_from_database = pd.read_sql_query("SELECT * FROM '%s'" % (name),con)
		con.close()
	else:
		print('That file does not exist in the database')
		df_from_database = None
	return df_from_database

def update_master_table(update_dic, database_name):
    """This updates the master table in the database based off of the information in the update dictionary"""
    if update_dic is not None:
        con = sql.connect(database_name)
        c = con.cursor()
        #add upload data filename in sql_master table
        c.execute('''INSERT INTO master_table('Dataset_Name', 'Raw_Data_Prefix','Cleaned_Data_Prefix', 'Cleaned_Cycles_Prefix') 
                     VALUES ('%s', '%s', '%s', '%s')
                  ''' % (update_dic['Dataset_Name'], update_dic['Raw_Data_Prefix'], update_dic['Cleaned_Data_Prefix'], update_dic['Cleaned_Cycles_Prefix']))
        # check if update_dic['Dataset_Name'] exists in master_table, if so, don't run the rest of the code. 
        #the above part updates the master table in the data frame
        con.commit()
        con.close()
        #display table in layout
        return 
    else:
        return [{}]

def init_master_table(database_name):
	con = sql.connect(database_name)
	c = con.cursor()
	mydf = pd.DataFrame({'Dataset_Name': [], 
                     	'Raw_Data_Prefix': [], 
                     	'Cleaned_Data_Prefix':[], 
                     	'Cleaned_Cycles_Prefix': []})
	mydf.to_sql('master_table', con, if_exists='replace')
	#my_df is the name of the table within the database

	con.close()
	return 