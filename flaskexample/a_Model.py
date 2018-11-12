def ModelIt(fromUser  = 'Default', meds = []):
	meds_num = len(meds) 
	if fromUser == 'Default':
		return "Please check your input."
	elif meds_num == 0:
		return "Cannot find your compound in our database, please use the prediction function to get the estimation!"	
	elif meds_num == 1:
		return "You got the exact match."
	else:
		return "Please be more specific for your search."