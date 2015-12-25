##This function takes in the user inputs and calculates the current assigned work.
import numpy as np
def farmsum(User_Schedule, Crop_Hours, Available_Hours):
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
	
	return weekly_sum, farm_death, Hour_Schedule

if __name__  == "__main__":
	#User_Schedule =np.genfromtxt('farmeroptinputmatrix.csv', delimiter = ',', skiprows = 1)[:,1:]
	#Crop_Hours = np.genfromtxt('farmeroptinputmatrix.csv', delimiter = ',', skiprows = 1)[:,1:]

	User_Schedule = np.array([[0,2,0,0,0], [1, 1, 0, 0, 0], [0, 0, 1, 0, 0]]) # Num of crop beds
	Crop_Hours = np.array([[.5, .5, .5, 0, 0], [1, 1.5, 0, 0, 0], [2, 2, 2, 0, 0]]) # Labor per week
	Available_Hours = np.array([2, 2, 3, 4, 2]) # Available hours per week
	print farmsum(User_Schedule, Crop_Hours, Available_Hours)
	
