
##we want to build and optimize matrix Hour_Schedule, which is a planting schedule of some size dependant on the user's inputs.

import numpy as np
from scipy.optimize import minimize
def FarmOpt(User_Schedule, Crop_Hours, Week_Flexibility, Beds_Flexibility, Available_Hours):
	
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
		#if there is no week flexibility, we will not try to 
		#optimize by moving things around. We should output just farm_death, 
		#and ask the user if they want to try optimization using the bed flexibility.
		if sum(Week_Flexibility) == 0: 
			print "Week flexibility is zero, do you want to try changing the number of beds?"
		return farm_death, Hour_Schedule

	
	#Process_User_Schedule(User_Schedule, Crop_Hours)	

	def optimizer(User_Schedule, Week_Flexibility, Beds_Flexibility):
		farm_death, Hour_Schedule = Process_User_Schedule(User_Schedule, Crop_Hours, Week_Flexibility)

		better = True
		while better is True:
			#find the first thing to try to fix
			worst_entry =  np.argmax(farm_death)
			worst_column = Hour_Schedule[:, worst_entry]
			problem_row = User_Schedule[np.argmax(worst_column)]
			
			check_wk_flexibility =  Week_Flexibility[np.argmax(worst_column)]
			if check_wk_flexibility > 0:
				print "yay moveable"
			elif check_wk_flexibility == 0:
				pass

			better = False
			# if something:
			# 	better = False

		print "done?"
		return 


	print optimizer(User_Schedule, Week_Flexibility, Beds_Flexibility)

if __name__  == "__main__":
	#User_Schedule =np.genfromtxt('farmeroptinputmatrix.csv', delimiter = ',', skiprows = 1)[:,1:]
	#Crop_Hours = np.genfromtxt('farmeroptinputmatrix.csv', delimiter = ',', skiprows = 1)[:,1:]

	User_Schedule = np.array([[0,2,0,0,0], [1, 1, 0, 0, 0], [0, 0, 1, 0, 0]])
	Crop_Hours = np.array([[.5, .5, .5, 0, 0], [1, 1.5, 0, 0, 0], [2, 2, 2, 0, 0]])
	Week_Flexibility = np.array([[1], [0], [2]])
	Beds_Flexibility = np.array([[0], [3], [1]])
	Available_Hours = np.array([[2, 2, 3, 4, 2]])
	FarmOpt(User_Schedule, Crop_Hours, Week_Flexibility, Beds_Flexibility, Available_Hours)
	


	