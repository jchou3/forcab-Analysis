"""
This class will build the dataset for the inputted 
raw data. The data built will simply be the raw data 
transformed into a manner such that we can run it through 
more preprocessing steps. 

One big assumption is that inputted data is of the same format 
as the yellow_trip_2022-06.csv in terms of columns and feature names.

"""
# Importing libraries
import pandas as pd

class DataBuilder():
    # the constructor
    def __init__(self,demand_data:pd.DataFrame,zones_list:list,month:str) -> None:
        """
        The constructor.

        inputs:
        - demand_data: a pandas dataframe containing the raw data of trips
        - zones_list: a list of the taxi zones
        - month: a string indicating the month.

        outputs:
        - None
        """
        # Setting up the global variables
        self.demand_data = demand_data
        self.zones = zones_list
        self.month = month

        # A dictionary that indicates the number of days in the given month
        days = {'Jan':31,'Feb':28,'March':31,'April':30,'May':31,'June':31,'July':31,
                'Aug':31,'Sept':30,'Oct':31,'Nov':30,'Dec':31}
        
        # Getting the maximum number of days
        self.max_days = days[month]
    
    # Function to split the datetime 
    def split_datetime(self) -> pd.DataFrame:
        """
        split_datetime

        A function to split the raw data datetime into month, day, year, and hour.

        inputs:
        - None

        outputs:
        - a pandas dataframe with Month, Day, Year, and Hour as columns
        """
        # Making a copy of the data
        data_copy = self.demand_data.copy()

        # Splitting the datetime up into Month, Day, Year, Hour
        data_copy['Month'] = data_copy['tpep_pickup_datetime'].str.split(' ').str[0].str.split('-').str[1]
        data_copy['Day'] = data_copy['tpep_pickup_datetime'].str.split(' ').str[0].str.split('-').str[2]
        data_copy['Year'] = data_copy['tpep_pickup_datetime'].str.split(' ').str[0].str.split('-').str[0]
        data_copy['Hour'] = data_copy['tpep_pickup_datetime'].str.split(' ').str[1].str.split(':').str[0]

        # Dropping all other columns
        data_copy = data_copy[['Month','Day','Year','Hour']]

        # Converting the datatypes for the columns into ints
        data_copy['Month'] = data_copy['Month'].astype('int')
        data_copy['Day'] = data_copy['Day'].astype('int')
        data_copy['Hour'] = data_copy['Hour'].astype('int')

        # Returning the data
        return data_copy

    # Getting the demand for each zone for each day and each hour
    def get_demand(self,zone_data: pd.DataFrame) -> dict:
        """
        get_demand

        A function to get the demand data for a given zone's data

        input:
        - zone_data: a pandas dataframe for the zone

        output:
        - a dictionary with (day,(hour,demand)) pairs.
        """
        # Getting the demand
        demand_dict = {}

        # Iterating through every day and every hour to get the demand
        for day in range(1,self.max_days + 1):
            # Getting the dataframe with the specific day
            day_demand_df = zone_data[zone_data['Day'] == day]

            # Creating the dictionary for the day
            day_demand_dict = {} # (hour,demand)
            for hour in range(0,24):
                day_demand_dict[hour] = len(day_demand_df[day_demand_df['Hour'] == hour])
            
            # Putting the day demand data into the dictionary
            demand_dict[day] = day_demand_dict

        # returning the demand
        return demand_dict

    # Creating a function for creating the dataset
    def create_dataset(self) -> pd.DataFrame:
        """
        create_dataset

        A function to create the final dataset

        inputs:
        - None
        outputs:
        - a pandas dataframe that outlines the final dataset
        """
        final_dataset = None

        # Iterating through each zone
        for zone in self.zones:
            zone_data = self.demand_data[self.demand_data['PULocationID'] == zone] # get the zone data

            # Getting the demand of the zone per hour per day
            demand = self.get_demand(self.split_datetime(zone_data))

            # Creating the final dataset for the specified zone
            examples = [] # a matrix of the examples

            for day in range(1,self.max_days+1):
                for hour in range(0,24):
                    example = [zone,self.month,day,'2022',hour,demand[day][hour]]
                    examples.append(example)

            zone_df = pd.DataFrame(examples,columns=['Zone','Month','Day','Year','Hour','Total Demand'])

            # Adding zone_df to the final_dataset
            if final_dataset is None:
                final_dataset = zone_df
            else:
                final_dataset = final_dataset.append(zone_df,ignore_index=True)

        # Returning the final dataset
        return final_dataset

# Having a tester for this class
if __name__ == '__main__':
    # Getting the raw data and setting up the zones
    demand_data = pd.read_csv('data/yellow_tripdata_2022-06.csv',index_col=0)
    zones = list(range(1,264))

    # Creating the DataBuilder object
    data_builder = DataBuilder(demand_data,zones,month='June')

    # Getting the final_dataset
    final_dataset = data_builder.create_dataset()
    
    # Saving the final_dataset as a csv
    final_dataset.to_csv('../data/transformed_preliminary_data.csv',index=False)