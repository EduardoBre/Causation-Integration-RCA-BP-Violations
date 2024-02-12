import pandas as pd
from pandas import DataFrame
from datetime import datetime, timedelta


def add_trace_based_on_degree(activity_list: list[str],
                              activity_key_list: list[str],
                              row_id: int,
                              old_dataset: DataFrame,
                              new_dataset: dict,
                              new_dataset_columns: list[str],
                              event_index: int) -> int:
    """
    Helper function to add event logs based on the provided activity lists.
    :param activity_list: List of all the activities of the trace.
    :param activity_key_list: List of all the activity keys of the trace.
    :param row_id: Row index of the trace.
    :param old_dataset: Unformated dataset (input).
    :param new_dataset: Formated dataset (output).
    :param new_dataset_columns: List of names of columns for the formated dataset.
    :param event_index: Index to be used for unique event identification.
    :return: List of all the columns in the refactored dataset (output).
    """

    # add trace id, event id and timestamps
    time = datetime.strptime(old_dataset.iloc[row_id, 1], '%Y-%m-%d %H:%M:%S')
    case_id = old_dataset.iloc[row_id, 0]

    for i in range(len(activity_list)):
        # add trace id and event id
        new_dataset[new_dataset_columns[0]].append(case_id)
        new_dataset[new_dataset_columns[1]].append(event_index)
        event_index += 1

    # add date_time, height, moisture and roast degree
    for i in range(0, 3):
        # add time with 30 sec interval
        new_dataset[new_dataset_columns[2]].append(str(time))
        time = time + timedelta(seconds=30)

        # add activity, activity key and value
        new_dataset[new_dataset_columns[3]].append(activity_list[i])
        new_dataset[new_dataset_columns[4]].append(activity_key_list[i])
        new_dataset[new_dataset_columns[5]].append(old_dataset.iloc[row_id, i + 2])

    # add all roasting chambers
    for i in range(3, len(activity_list) - 2):
        # add time with 5 minutes interval
        new_dataset[new_dataset_columns[2]].append(str(time))
        time = time + timedelta(minutes=5)

        # add activity, activity key and value
        new_dataset[new_dataset_columns[3]].append(activity_list[i])
        new_dataset[new_dataset_columns[4]].append(activity_key_list[i])
        new_dataset[new_dataset_columns[5]].append(old_dataset.iloc[row_id, i + 2])

    counter = len(activity_list) - 2
    # add final measure and quality assessment
    for i in range(20, 22):
        # add time with 30 seconds interval
        new_dataset[new_dataset_columns[2]].append(str(time))
        time = time + timedelta(seconds=30)

        # add activity, activity key and value
        new_dataset[new_dataset_columns[3]].append(activity_list[counter])
        new_dataset[new_dataset_columns[4]].append(activity_key_list[counter])
        new_dataset[new_dataset_columns[5]].append(old_dataset.iloc[row_id, i])
        counter += 1

    return event_index


old_dataframe = pd.read_excel('original-coffee_data_categorical.xlsx')

# Define dataset column titles
COLUMN_1 = 'case_id'
COLUMN_2 = 'event_id'
COLUMN_3 = 'date_time'
COLUMN_4 = 'activity'
COLUMN_5 = 'activity_key'
COLUMN_6 = 'activity_value'
NEW_DATASET_COLUMNS = [COLUMN_1, COLUMN_2, COLUMN_3, COLUMN_4, COLUMN_5, COLUMN_6]

# Define dataset activities list based on roast degree
ACTIVITY_LIST_RD0 = [
    'Height Measure',
    'Moisture Measure',
    'Roast Degree Selection',
    'Roasting Chamber 1',
    'Roasting Chamber 1',
    'Roasting Chamber 1',
    'Roasting Chamber 2',
    'Roasting Chamber 2',
    'Roasting Chamber 2',
    'Roasting Chamber 3',
    'Roasting Chamber 3',
    'Roasting Chamber 3'
]

ACTIVITY_LIST_RD1 = ACTIVITY_LIST_RD0.copy()
ACTIVITY_LIST_RD1.extend([
    'Roasting Chamber 4',
    'Roasting Chamber 4',
    'Roasting Chamber 4'
])

ACTIVITY_LIST_RD2 = ACTIVITY_LIST_RD1.copy()
ACTIVITY_LIST_RD2.extend([
    'Roasting Chamber 5',
    'Roasting Chamber 5',
    'Roasting Chamber 5'
])

# add final measure and quality assessment to traces
VIOLATION_MEASURE = [
    'Final Measure',
    'Quality Assessment',
]
ACTIVITY_LIST_RD0.extend(VIOLATION_MEASURE)
ACTIVITY_LIST_RD1.extend(VIOLATION_MEASURE)
ACTIVITY_LIST_RD2.extend(VIOLATION_MEASURE)

# Define dataset activities key list based on roast degree
ACTIVITY_KEY_LIST_RD0 = [
    'height',
    'moisture',
    'roasting_degree',
    'RC1_Sensor_1',
    'RC1_Sensor_2',
    'RC1_Sensor_3',
    'RC2_Sensor_1',
    'RC2_Sensor_2',
    'RC2_Sensor_3',
    'RC3_Sensor_1',
    'RC3_Sensor_2',
    'RC3_Sensor_3'
]

ACTIVITY_KEY_LIST_RD1 = ACTIVITY_KEY_LIST_RD0.copy()
ACTIVITY_KEY_LIST_RD1.extend([
    'RC4_Sensor_1',
    'RC4_Sensor_2',
    'RC4_Sensor_3'
])

ACTIVITY_KEY_LIST_RD2 = ACTIVITY_KEY_LIST_RD1.copy()
ACTIVITY_KEY_LIST_RD2.extend([
    'RC5_Sensor_1',
    'RC5_Sensor_2',
    'RC5_Sensor_3'
])

# add final measure and quality assessment keys to traces
VIOLATION_KEYS_MEASURE = [
    'violation',
    'case_no'
]
ACTIVITY_KEY_LIST_RD0.extend(VIOLATION_KEYS_MEASURE)
ACTIVITY_KEY_LIST_RD1.extend(VIOLATION_KEYS_MEASURE)
ACTIVITY_KEY_LIST_RD2.extend(VIOLATION_KEYS_MEASURE)

# add new dataset columns
updated_ds = {key: [] for key in NEW_DATASET_COLUMNS}

# counter for event ids starting at 30000
event_counter: int = 30_000

# add event logs to the new dataset depending on the roast degree
for row_index in range(len(old_dataframe)):
    roasting_degree = old_dataframe.iloc[row_index, 4]
    if roasting_degree == 0:
        event_counter = add_trace_based_on_degree(ACTIVITY_LIST_RD0, ACTIVITY_KEY_LIST_RD0, row_index, old_dataframe,
                                                  updated_ds, NEW_DATASET_COLUMNS, event_counter)
    elif roasting_degree == 1:
        event_counter = add_trace_based_on_degree(ACTIVITY_LIST_RD1, ACTIVITY_KEY_LIST_RD1, row_index, old_dataframe,
                                                  updated_ds, NEW_DATASET_COLUMNS, event_counter)
    elif roasting_degree == 2:
        event_counter = add_trace_based_on_degree(ACTIVITY_LIST_RD2, ACTIVITY_KEY_LIST_RD2, row_index, old_dataframe,
                                                  updated_ds, NEW_DATASET_COLUMNS, event_counter)

# create dataframe and output it as .xlsx
df = DataFrame.from_dict(updated_ds, orient='columns')
df.to_excel('refactored-coffee_data_categorical.xlsx')
