from .predict import predict
from .a_Model import ModelIt
from flask import request
from flask import render_template
from flaskexample import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2

username = 'sheldon'
host = 'localhost'
dbname = 'med_db'
pswd = '****'

engine = create_engine('postgresql://%s:%s@%s/%s'%(username, pswd, host, dbname))
if not database_exists(engine.url):
    create_database(engine.url)
csv_path = 'data/med_db.csv'
med_data = pd.read_csv(csv_path, index_col=0)
med_data.to_sql('med_data_table', engine, if_exists='replace')

con = None
con = psycopg2.connect(database = dbname, user = username, host=host, password=pswd)

@app.route('/')
@app.route('/home')
def home():
	return render_template("home.html")

						   
@app.route('/db_input')
def db_input():
    return render_template("db_input.html")

@app.route('/db_output')
def db_output():
    #pull 'chemical name' from input field and store it
    chemical_name = request.args.get('chemical_name')
    #just select the chemicals from the med database
    query = "SELECT chemical_name, n_hit FROM med_data_table WHERE UPPER(chemical_name) LIKE UPPER('%{}%')".format(chemical_name)
    
    query_results=pd.read_sql_query(query,con)
    print (query_results)
    meds = []
    for i in range(0,query_results.shape[0]):
        meds.append(dict(chemical_name=query_results.iloc[i]['chemical_name'], n_hit=query_results.iloc[i]['n_hit']))
    the_result = ModelIt(chemical_name,meds)
    return render_template("db_output.html", meds = meds, the_result = the_result)


@app.route('/pred_output')
def pred_output():
	smiles = request.args.get('SMILES')
	proba, res = predict(smiles)	
	if proba == -1:
		return render_template("error.html")
	return render_template("pred_output.html", proba=proba, res=res)

@app.route('/about')
def about():
	return render_template("about.html")

		
