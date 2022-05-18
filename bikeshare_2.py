import calendar
import datetime
import time
import pandas as pd

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}
month_filter, day_filter = None, None


def check_input(choice_type, choices):
    while True:
        choice = input(f"choices {choices}: ").strip()
        if choice == '0':
            return 'all'
        try:
            if choice_type == 'month':
                choice = calendar.month_name[int(choice)]
            else:
                choice = calendar.day_name[int(choice) - 1]
        except IndexError:
            print(f"Wrong input, {choice} isn't a {choice_type} no., you must enter a value in the mentioned choices!")
            continue
        except ValueError:
            print(f"Wrong input, {choice} isn't a number, you must enter a value in the mentioned choices!")
            continue
        return choice


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Enter city name that you want to explore their data from,')
    while True:
        city = input('choices (chicago, new york city, washington): ').strip().lower()
        if city not in CITY_DATA:
            print(f"Wrong input, {city} isn't a city name or isn't in the mentioned choices")
            continue
        break

    # get user input for month (all, january, february, ... , june)
    print("Enter a month no. that you want to explore in or type a '0' to explore in all months,")
    choices = "(0=all , 1=January , 2=February , 3=March , ... , 12=December)"
    month = check_input('month', choices)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print("Enter a day no. that you want to explore on or type a '0' to explore on all weekdays,")
    choices = "(0=all, 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday, 6=Saturday, 7=Sunday)"
    day = check_input('day', choices)
    print('-'*120)
    global month_filter, day_filter
    month_filter, day_filter = month, day
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

    # Cast 'Start Time' column type to date time and exclude the month and day names
    start_time = pd.to_datetime(df['Start Time'])
    df['Month'] = start_time.dt.month_name()
    df['Day'] = start_time.dt.day_name()
    df['Hour'] = start_time.dt.hour
    df['Start/End Time'] = df['Start Time'] + ' ' + df['End Time']
    if 'Birth Year' in df:
        df['Birth Year'] = df['Birth Year'].fillna(method='ffill').astype(int)
    # Filter by month of day names if they do not equal to 'all'
    if month != 'all':
        df = df[df['Month'] == month]
    if day != 'all':
        df = df[df['Day'] == day]
    return df


def display_most_common(df, common):
    """
    Displays the most common in the DataFrame by using the statistical function 'mode()'.

    Args:
        (DataFrame) df - dataframe
        (str) common - any column name in the dataframe
    """
    most_common = df[common].mode().tolist()
    print(f"The most common {common} of travel {'is' if len(most_common) == 1 else 'are'} {' '.join(map(str, most_common))}")


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print(f'\nCalculating The Most Frequent Times of Travel on {day_filter} weekdays & in {month_filter} months\n')
    start_time = time.time()

    # display the most common month
    display_most_common(df, 'Month')

    # display the most common day of week
    display_most_common(df, 'Day')

    # display the most common start hour
    display_most_common(df, 'Hour')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('f\nCalculating The Most Popular Stations and Trip on {day_filter} weekdays & in {month_filter} months\n')
    start_time = time.time()

    # display most commonly used start station
    display_most_common(df, 'Start Station')

    # display most commonly used end station
    display_most_common(df, 'End Station')

    # display most frequent combination of start station and end station trip
    display_most_common(df, 'Start/End Time')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print(f'\nCalculating Trip Duration on {day_filter} weekdays & in {month_filter} months\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = datetime.timedelta(seconds=float(df['Trip Duration'].sum()))
    print(f"The total travel time is {total_trip_duration}")

    # display mean travel time
    average_trip_duration = datetime.timedelta(seconds=float(df['Trip Duration'].mean()))
    print(f"The average travel time is {average_trip_duration}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def display_users_counts(df, state):
    """
    Displays users states in the DataFrame'.

    Args:
        (DataFrame) df - dataframe
        (str) state - any column name in the dataframe
    """
    print(f"The counts of {state} are :")
    user_states = df[state].value_counts().to_dict()
    for state, count in user_states.items():
        print(f"The count of {state} = {count}")


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print(f'\nCalculating User Stats on {day_filter} weekdays & in {month_filter} months\n')
    start_time = time.time()

    # Display counts of user types
    display_users_counts(df, 'User Type')
    print()

    if 'Gender' in df:
        # Display counts of gender
        display_users_counts(df, 'Gender')
        print()

    if 'Birth Year' in df:
        # Display earliest, most recent, and most common year of birth
        print(f"The earliest year of birth is {df['Birth Year'].min()}")
        print(f"The most recent year of birth is {df['Birth Year'].max()}")
        display_most_common(df, 'Birth Year')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def show_row_data(df):
    """
    Asks the user to display 5 rows of raw data in the DataFrame based on the user choice.

    Args:
        (DataFrame) df - dataframe
    """
    number_of_rows = 0
    while True:
        choice = input('Would you like to see 5 rows of the raw data? Enter (yes or no): ').strip().lower()
        if choice == 'yes':
            print(df.iloc[number_of_rows:number_of_rows + 5])
            number_of_rows += 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty:
            print(f'There is no data in {month} or on {day}')
            continue

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_row_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
