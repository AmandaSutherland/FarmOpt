
##we want to build and optimize matrix X, which is a planting schedule of some size dependant on the user's inputs.

import numpy as np
from scipy.optimize import minimize
def FarmOpt(X0, Crop_Hours, Week_Flexibility, Beds_Flexibility, Available_Hours):
	#user-input planting schedule information
	X0 = np.array([[0,2,0,0,0], [1, 1, 0, 0, 0], [0, 0, 1, 0, 0]])
	Crop_Hours = np.array([[.5, 0, .5, 0, 0], [1, 1.5, 0, 0, 0], [2, 2, 2, 0, 0]])
	Available_Hours = np.array([20, 60, 80, 40, 20])
	#initialize the labor schedule array
	X = np.zeros(X0.shape);

	#find the locations of the nonzero entries of X0
	tnzX0 = np.transpose(np.nonzero(X0))

	#give the value and location of the nonzero entries of X0
	for index in tnzX0:
		entry = X0[index[0],index[1]]
		#print entry  #number of beds
		print "index" , index  #[crop, week]

		#process a row of crop_hours for the crop at hand
		scheduled_hours =  entry * Crop_Hours[index[0], :]
		number_weeks = np.nonzero(scheduled_hours)[0][-1] + 1
		#add these hours to X
		X[index[0],index[1]:index[1]+number_weeks] += scheduled_hours[0:number_weeks]

	weekly_sum = X.sum(axis =0)
	farm_death = weekly_sum - Available_Hours
	print "farm death is", farm_death

if __name__  == "__main__":
	X0 = np.array([[0,2,0,0,0], [1, 1, 0, 0, 0], [0, 0, 1, 0, 0]])
	Crop_Hours = np.array([[.5, .5, .5, 0, 0], [1, 1.5, 0, 0, 0], [2, 2, 2, 0, 0]])
	Week_Flexibility = np.array([[1], [0], [2]])
	Beds_Flexibility = np.array([[0], [3], [1]])
	Available_Hours = np.array([[20, 60, 80, 40, 20]])
	FarmOpt(X0, Crop_Hours, Week_Flexibility, Beds_Flexibility, Available_Hours)