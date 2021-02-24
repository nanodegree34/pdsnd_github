import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - number of the month to filter by, or "all" to apply no month filter
        (str) day - number of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    city = input('Please enter the city for which you would like to see data \n - Chicago, Washington or New York \n')
    # make sure the input of the city is correct
    valid_cities = ['Chicago', 'chicago', 'Washington', 'washington', 'New York', 'new york']
    while city not in valid_cities:
        print('Please enter either Chicago, Washington or New York.\n')
        city = input('Please give the correct city name.\n')

    # get user input for the desired time filter
    time_filter_request = input('Would you like to filter the data by "month", "day", "both" or not at all? \nPlease type "none" for no time filter. \n')
    # make sure the input of the time filter is correct
    valid_time_filters = ['month','Month','Day','day','Both','both','None','none']
    if time_filter_request not in valid_time_filters:
        print('Your input does not match with the possible filter options. Therefore no filter will be applied.')

    # get user input for month as a number
    if time_filter_request == 'month' or time_filter_request == 'both':
        month = input('Which month between January and June would you like to select? \n- please give the month as a numerical value, i.e. January = 1, February = 2 etc. \n')
        # make sure the input for the month filter is correct
        valid_months = ['1','2','3','4','5','6']
        while month not in valid_months:
            print('Please enter a number between 1 and 6.\n')
            month = input('Which month would you like to select?\n')
    else:
        month = 'all'

    # get user input for day of week as a number
    if time_filter_request == 'day' or time_filter_request == 'both':
        day = input('Which day would you like to select? \n- please give the day of the week as a number with Monday=0, Sunday=6. \n')
        # make sure the input for the day filter is correct
        valid_days = ['0','1','2','3','4','5','6']
        while day not in valid_days:
            print('Please enter a number between 0 and 6.\n')
            day = input('Which day would you like to select?\n')
    else:
        day = 'all'

    print('-'*40)
    return city, month, day


def print_rawdata(df):
    """ Asks user whether he/she wants to see raw data and print 5 records each time """

    rawdata_request = input('Would you like to see individual trip data? (Y/N) \n')
    # variable 'counter' to select the corresponding records from the DataFrame
    counter = 0
    # select 5 records of the DataFrame, continue while the user enters 'y'
    while rawdata_request == 'Y' or rawdata_request == 'y':
        print(df.iloc[counter:counter+5])
        counter += 5
        rawdata_request = input('Would you like to see more? (Y/N)')
        if rawdata_request != 'Y' or rawdata_request != 'y':
            print('Ok, no more individual trip data will be shown.')

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    city = city.title()
    # load data file for the selected city into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # convert the column 'Start Time' to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from 'Start Time' to create new columns
    df['month'] = df['Start Time'].dt.month
    # The day of the week with Monday=0, Sunday=6
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    # filter by month based on the user input
    if month != 'all':
        # filter by month to create the new DataFrame
        df = df[df['month'] == int(month)]

    # filter by day of week based on the user input
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == int(day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    popular_month_text = calendar.month_name[popular_month]
    print('Most common month (in case you did not filter on month): {}'.format(popular_month_text))

    # display the most common day of week
    popular_dayofweek = df['day_of_week'].mode()[0]
    popular_dayofweek_text = calendar.day_name[popular_dayofweek]
    print('Most common day of week (in case you did not filter on day): ', popular_dayofweek_text)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most common start hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most common start station: ', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most common end station: ', common_end_station)

    # display most frequent combination of start station and end station trip
    df['start_end_station'] = df['Start Station'] + ' to ' + df['End Station']
    common_trip = df['start_end_station'].mode()[0]
    print('Most common combination of start and end station: ', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['duration'] = df['End Time'] - df['Start Time']
    total_travel_time = df['duration'].sum()

    print('The total travel time (based on the given filters) is ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    # display the total time in minutes with 3 decimal numbers
    mean_travel_time = '{:.3f}'.format(mean_travel_time/60)
    print('The mean travel time is {} minutes.'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count of users per user type: \n', user_types)

    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        print('Count of users, grouped by gender: \n', gender_counts)
    # Handle error in case there is no data for 'gender' in the selected file
    except KeyError:
        print('No gender data available')

    # Display earliest, most recent, and most common year of birth
    try:
        popular_birth_year = int(df['Birth Year'].mode())
        earliest_birth_year = int(df['Birth Year'].min())
        latest_birth_year = int(df['Birth Year'].max())
        print('The oldest user was born in {} and the youngest user was born in {}. \nThe most common year of birth of users is {}.'.format(earliest_birth_year, latest_birth_year, popular_birth_year))

    # Handle error in case there is no data for 'birth year' in the selected file
    except KeyError:
        print('No birth year data available')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_rawdata(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
