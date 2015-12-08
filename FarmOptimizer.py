
##we want to build and optimize matrix Hour_Schedule, which is a planting schedule of some size dependant on the user's inputs.

##each row will have a finite number of possible movements, so it might be good to generate all of them 
##initially (not initially, but when we touch that row we can just grab all the possibilities. it may even end up fixing other entries. ) and 
##weed out the ones that don't fit the constraints(an array of arrays). Next time we touch the row, we'll already have the possibilities and don't have to calculate them again. 
##this would look like a python array of python arrays of np arrays, so that we can append an unknown number of nparrays depending on the row.

import numpy as np
from copy import deepcopy
def FarmOpt(User_Schedule, Crop_Hours, Week_Flexibility, Beds_Flexibility, Available_Hours):
	if sum(Week_Flexibility) == 0:
		print "your schedule isn't flexible, so I can't rearrange it, but here's what your labour hours will be:", Process_User_Schedule(User_Schedule, Crop_Hours, Week_Flexibility)
		print "would you like to try changing the number of beds?"
	else: 
		print optimizer(User_Schedule, Week_Flexibility, Beds_Flexibility)

def optimizer(User_Schedule, Week_Flexibility, Beds_Flexibility):
	farm_death, Hour_Schedule = Process_User_Schedule(User_Schedule, Crop_Hours, Week_Flexibility)
	#initiate array for daughter points
	crops = len(User_Schedule)
	all_daughter_rows = []
	for i in range(0, crops):
		all_daughter_rows.append([])
	#here's the loop that finds bad stuff and optimizes
	better = True
	while better:
		#find the first thing to try to fix
		worst_entry =  np.argmax(farm_death)
		worst_column = Hour_Schedule[:, worst_entry]
		worst_column_copy = deepcopy(worst_column)
		found_flexible_bad = False
		while found_flexible_bad == False:
			worst_in_column = np.argmax(worst_column_copy)
			#make sure its week can be moved
			check_wk_flexibility =  Week_Flexibility[worst_in_column]
			if check_wk_flexibility > 0:
				problem_row = User_Schedule[worst_in_column]
				found_flexible_bad = True

			elif check_wk_flexibility == 0:
				print "that one wasn't flexible. trying again"
				worst_column_copy[worst_in_column] = -1 
				#will go to the next worst entry in the column of Hour_Schedule, 
				#and check its week flexibility. It might be useful to turn check flexibility into a loop. 

		better = False
		# if something:
		# better = False
	print"ok, here's where the problem is, and I can try to fix it:"
	return "problem row", problem_row, "wk flex", check_wk_flexibility 

def Process_User_Schedule(User_Schedule, Crop_Hours, Week_Flexibility):
	#initialize the labor schedule array
	Hour_Schedule = np.zeros(User_Schedule.shape);
	#find the locations of the nonzero entries of User_Schedule
	Not0_User_Schedule = np.transpose(np.nonzero(User_Schedule))
	#create Hour_Schedule, the labor assignment in hours
	for location in Not0_User_Schedule:
		entry = User_Schedule[location[0],location[1]]  #number of beds assigned at location
		#create a row of scheduled hours for the crop at hand
		scheduled_hours =  entry * Crop_Hours[location[0], :]
		number_weeks = np.nonzero(scheduled_hours)[0][-1] + 1
		#add this row to Hour_Schedule
		Hour_Schedule[location[0],location[1]:location[1]+number_weeks] += scheduled_hours[0:number_weeks]
	#find the total hours assigned to each week
	weekly_sum = Hour_Schedule.sum(axis =0)
	#how many extra hours are assigned
	farm_death = weekly_sum - Available_Hours
	
	return farm_death, Hour_Schedule

if __name__  == "__main__":
	#User_Schedule =np.genfromtxt('farmeroptinputmatrix.csv', delimiter = ',', skiprows = 1)[:,1:]
	#Crop_Hours = np.genfromtxt('farmeroptinputmatrix.csv', delimiter = ',', skiprows = 1)[:,1:]

	User_Schedule = np.array([[0,2,0,0,0], [1, 1, 0, 0, 0], [0, 0, 1, 0, 0]])
	Crop_Hours = np.array([[.5, .5, .5, 0, 0], [1, 1.5, 0, 0, 0], [2, 2, 2, 0, 0]])
	Week_Flexibility = np.array([[1], [0], [2]]) 
	Beds_Flexibility = np.array([[0], [3], [1]])
	Available_Hours = np.array([[2, 2, 3, 4, 2]])
	FarmOpt(User_Schedule, Crop_Hours, Week_Flexibility, Beds_Flexibility, Available_Hours)
	


	