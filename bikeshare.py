import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower()
        if city in CITY_DATA:
            break
        print('That\'s not a valid city. Please choose Chicago, New York City, or Washington.')

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month? January, February, March, April, May, June, or "all"?\n').lower()
        if month == 'all' or month in MONTHS:
            break
        print('That\'s not a valid month. Please choose a month from January to June, or "all".')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day? Please type a day name (e.g. Monday), or "all"?\n').lower()
        if day == 'all' or day in DAYS:
            break
        print('That\'s not a valid day. Please type a full day name, or "all".')

    print('-'*40)
    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month_index = MONTHS.index(month) + 1
        df = df[df['month'] == month_index]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month:', MONTHS[common_month - 1].title())

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day of week:', common_day)

    # TO DO: display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most common start hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station:', common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station:', common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    common_trip = df['trip'].mode()[0]
    print('Most frequent combination of start and end station trip:', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time: {} seconds ({:.2f} hours)'.format(total_travel_time, total_travel_time / 3600))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time: {:.2f} seconds ({:.2f} minutes)'.format(mean_travel_time, mean_travel_time / 60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    if 'User Type' in df.columns:
        print('Counts of user types:')
        print(df['User Type'].value_counts().to_string())
    else:
        print('No user type data available for this city.')

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print('\nCounts of gender:')
        print(df['Gender'].value_counts().to_string())
    else:
        print('\nNo gender data available for this city.')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nEarliest year of birth:', int(df['Birth Year'].min()))
        print('Most recent year of birth:', int(df['Birth Year'].max()))
        print('Most common year of birth:', int(df['Birth Year'].mode()[0]))
    else:
        print('\nNo birth year data available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Displays 5 rows of raw data at a time, upon user request."""

    row_index = 0

    while True:

        show_data = input('\nWould you like to see 5 rows of raw data? Enter yes or no.\n').lower().strip()

        while show_data not in ['yes', 'no']:
            print('Invalid input. Please enter yes or no.')
            show_data = input('\nWould you like to see 5 rows of raw data? Enter yes or no.\n').lower().strip()

        if show_data == 'no':
            break

        print(df.iloc[row_index:row_index + 5])

        row_index += 5

        if row_index >= len(df):
            print('\nNo more data to display.')
            break
    

def main():
    while True:

        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Empty Dataframe Check
        if df.empty:
            print('\nNo data found for the selected filters. Please try again.\n')
            continue

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        # Restart input validation
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower().strip()

            if restart in ['yes', 'no']:
                break

            print('Invalid input. Please enter yes or no.')

        if restart == 'no':
            break


if __name__ == "__main__":
	main()
