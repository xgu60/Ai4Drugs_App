from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
import numpy as np 
import pandas as pd 
from sklearn.externals import joblib

def predict(smiles):
	if smiles == "please enter SMILES here" or smiles == "":
		return -1, ""
	#compute features from smiles	
	try:		
		arr = np.zeros((1, ))
		compound = Chem.MolFromSmiles(smiles)
		fp = AllChem.GetMorganFingerprintAsBitVect(compound, 3, 4096)
		DataStructs.ConvertToNumpyArray(fp, arr)
	except:
		return -1, ""
		
	data_input = arr.reshape(1, -1)
	
	#load prestored model to do prediction
	model = joblib.load("model.pkl")
	proba = round(model.predict_proba(data_input)[0, 1], 2)	
	if proba > 0.25:
		res = "has"
	else:
		res = "has no"
	
	return proba, res


if __name__ == "__main__":	
	res = predict("CCCCOC(=O)C1=CC=C(C=C1)N")
	print (res)
