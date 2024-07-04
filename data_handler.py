import pandas as pd

class DataHandler:
    def __init__(self, filepath):
        self.filepath = filepath
        self.state_data = None

    # This functions loads the data from the csv file, drops the unused columns, 
    # removes duplicates and missing values 
    def load_data(self):
        self.state_data = pd.read_csv(self.filepath)
        self._drop_unused_columns()
        self._drop_duplicates_and_na()
        return self.state_data
    
# This function drops the unused columns from the dataset, specifically drops FIPS Code.
    def _drop_unused_columns(self):
        if self.state_data is not None:
            self.state_data = self.state_data.drop(columns=['FIPS Code'])
            
# This function removes the duplicates if existed in the dataset
    def _drop_duplicates_and_na(self):
        if self.state_data is not None:
            self.state_data.drop_duplicates(keep='last', inplace=True)
            self.state_data.dropna(inplace=True)
            
# Filters the data on the given start date, end date and states.
    def filter_data(self, start_date=None, end_date=None, states=None):
        if self.state_data is None:
            return None

        state_data_filtered = self.state_data.copy()

        if start_date and end_date:
            state_data_filtered['Date'] = pd.to_datetime(state_data_filtered[['Year', 'Month']].assign(DAY=1))
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
            state_data_filtered = state_data_filtered[(state_data_filtered['Date'] >= start_date) & (state_data_filtered['Date'] <= end_date)]
        
        if states:
            state_data_filtered = state_data_filtered[state_data_filtered['State/Area'].isin(states)]
        
        return state_data_filtered