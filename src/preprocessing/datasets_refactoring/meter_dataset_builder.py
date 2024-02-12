from pandas import DataFrame
from datetime import datetime, timedelta
import random

from meter_enums import SynchronizationStatus, ReportStatus, MeterViewStatus

# Define Columns of dataset
COLUMN_0 = 'case_id_summary'
COLUMN_1 = 'case_id'
COLUMN_2 = 'event_id'
COLUMN_3 = 'date_time'
COLUMN_4 = 'activity'
COLUMN_5 = 'activity_key'
COLUMN_6 = 'activity_value'
# 0 = no violation, {i} = where i is an integer and corresponds to the predefined constraint c_i
# refer to documentation for explanation on the 11 violations
COLUMN_7 = 'violation'
# List of the defined columns
DATASET_COLUMNS = [COLUMN_1, COLUMN_2, COLUMN_3, COLUMN_4, COLUMN_5, COLUMN_6, COLUMN_7]

# Initial request made by customer -> 0 = deactivate, 1 = activate
ACTIVITY_1 = 'Request Consumption Display'
ACTIVITY_1_KEY = 'request status'

# Evaluate 1 minute cooldown rule
ACTIVITY_2 = 'Retrieve Customer\'s Last Request Time'
ACTIVITY_2_KEY = 'previous request timestamp'

# Evaluate 60 days data privacy rule
ACTIVITY_3 = 'Retrieve Customer\'s Registration Date'
ACTIVITY_3_KEY = 'customer registration timestamp'

# Evaluate number of customer requests -> period = in hours, count = number of times
ACTIVITY_4 = 'Retrieve Number of Customer Change Requests 24h'
ACTIVITY_4_KEY = 'change count in last 24hrs'

# Central System triggered synchronization with a status -> 0 = deactivate, 1 = activate
ACTIVITY_5 = 'Request Meter Synchronization'
ACTIVITY_5_KEY = 'synchronization status'

# status 1: Activate consumption display -> 0 = deactivate, 1 = activate
ACTIVITY_6 = 'Activate Consumption Display'
ACTIVITY_6_KEY = 'change status'

# status 0: Deactivate consumption display -> 0 = deactivate, 1 = activate
ACTIVITY_7 = 'Deactivate Consumption Display'
ACTIVITY_7_KEY = 'change status'

# Map status entry in logbook -> ALARM = deactivate, EVENT = activate
ACTIVITY_8 = 'Register Logbook Entry'
ACTIVITY_8_KEY = 'logbook entry status'

# Report status to Central System -> ALARM = deactivate, EVENT = activate
ACTIVITY_9 = 'Report Display Status'
ACTIVITY_9_KEY = 'report entry status'

# Central System confirmation registration of latest display status -> 0 = deactivated, 1 = activated
ACTIVITY_10 = 'Register Display Status'
ACTIVITY_10_KEY = 'registration status'

# Final Evaluation of Load Profile View on Meter
ACTIVITY_11 = 'View Consumption Display'
ACTIVITY_11_KEY = 'display view status'

# List of activities and keys for a complete trace simulating a DEACTIVATION REQUEST
CORRECT_TRACE_ACTIVITIES_D = [ACTIVITY_1, ACTIVITY_2, ACTIVITY_3, ACTIVITY_4, ACTIVITY_5, ACTIVITY_7,
                              ACTIVITY_8, ACTIVITY_9, ACTIVITY_10, ACTIVITY_11]

# add new dataset columns
dataset = {key: [] for key in DATASET_COLUMNS}


def add_trace(t_id: int,
              t_act: list[str],
              t_act_att: dict,
              timestamp: datetime,
              event_id: int) -> int:
    """
    Adds a trace to the dataset.
    :param t_id: Trace id.
    :param t_act: Event activities of the trace.
    :param t_act_att: Attributes (key, value) of each event activities of the trace.
    :param timestamp: The initial timestamp of the trace
    :param event_id: Unique id of the event.
    """
    curr_datetime = timestamp

    for activity, (key, value) in zip(t_act, t_act_att.items()):
        dataset[COLUMN_1].append(t_id)
        dataset[COLUMN_2].append(event_id)
        dataset[COLUMN_3].append(curr_datetime)
        dataset[COLUMN_4].append(activity)
        dataset[COLUMN_5].append(key)
        dataset[COLUMN_6].append(value)
        dataset[COLUMN_7].append(0)
        # @see method simulate_probability() for probabilities on upper bounds
        curr_datetime += timedelta(seconds=random.randint(0, 40))
        event_id += 1

    # return new counter index
    return event_id


def gen_correct_trace(timestamp: datetime,
                      case_id: int,
                      event_id: int) -> int:
    # Generate random request type
    req_status = random.randint(0, 1)
    # Generate a random (last request) date within 30 days prior to the request date
    prev_req_date = timestamp - timedelta(minutes=random.uniform(0, 30 * 24 * 60))
    # Generate a random registration date between 5 and 4 years prior to current request
    cus_reg_date = timestamp - timedelta(days=random.uniform(4 * 365.25, 5 * 365.25))
    # Period should always be 24 hours due to constraints, count should be 1 if last req was within 24 hrs else 0.
    sync_list = 1 if (timestamp - timedelta(hours=24)) <= prev_req_date <= timestamp else 0
    # Evaluate whether the registration and report status is an EVENT or ALARM based on request status
    reg_status = ReportStatus.EVENT.name if req_status == 1 else ReportStatus.ALARM.name

    # List of activities and map of key-values (attributes) for a complete trace simulating a request
    if req_status == 1:
        trace_activities = [ACTIVITY_1, ACTIVITY_2, ACTIVITY_3, ACTIVITY_4, ACTIVITY_5, ACTIVITY_6,
                            ACTIVITY_8, ACTIVITY_9, ACTIVITY_10, ACTIVITY_11]
        trace_activities_att = {ACTIVITY_1_KEY: req_status,
                                ACTIVITY_2_KEY: prev_req_date,
                                ACTIVITY_3_KEY: cus_reg_date,
                                ACTIVITY_4_KEY: sync_list,
                                ACTIVITY_5_KEY: SynchronizationStatus.SYNCHRONIZED.name,
                                ACTIVITY_6_KEY: req_status,
                                ACTIVITY_8_KEY: reg_status,
                                ACTIVITY_9_KEY: reg_status,
                                ACTIVITY_10_KEY: req_status,
                                ACTIVITY_11_KEY: MeterViewStatus.DISPLAY_ON.name}
    else:
        trace_activities = [ACTIVITY_1, ACTIVITY_2, ACTIVITY_3, ACTIVITY_4, ACTIVITY_5, ACTIVITY_7,
                            ACTIVITY_8, ACTIVITY_9, ACTIVITY_10, ACTIVITY_11]
        trace_activities_att = {ACTIVITY_1_KEY: req_status,
                                ACTIVITY_2_KEY: prev_req_date,
                                ACTIVITY_3_KEY: cus_reg_date,
                                ACTIVITY_4_KEY: sync_list,
                                ACTIVITY_5_KEY: SynchronizationStatus.SYNCHRONIZED.name,
                                ACTIVITY_7_KEY: req_status,
                                ACTIVITY_8_KEY: reg_status,
                                ACTIVITY_9_KEY: reg_status,
                                ACTIVITY_10_KEY: req_status,
                                ACTIVITY_11_KEY: MeterViewStatus.DISPLAY_OFF.name}

    return add_trace(case_id, trace_activities, trace_activities_att, timestamp, event_id)


def gen_violation(timestamp: datetime,
                  case_id: int,
                  event_id: int,
                  violation: int) -> int:
    """
    Generates a trace up to the violation occurrence.
    :param timestamp: Initial timestamp of the first activity.
    :param case_id: Unique trace id.
    :param event_id: Unique event id.
    :param violation: The violation to be simulated.
    """

    # Template of a correct trace to avoid duplications
    if violation in [4, 6, 8, 10]:
        req_status = 1
    elif violation in [5, 7, 9, 11]:
        req_status = 0
    else:
        req_status = random.randint(0, 1)
    prev_req_date = timestamp - timedelta(minutes=random.uniform(0, 30 * 24 * 60))
    cus_reg_date = timestamp - timedelta(days=random.uniform(4 * 365.25, 5 * 365.25))
    sync_list = 1 if (timestamp - timedelta(hours=24)) <= prev_req_date <= timestamp else 0
    reg_status = ReportStatus.EVENT.name if req_status == 1 else ReportStatus.ALARM.name
    activity_list = [ACTIVITY_1, ACTIVITY_2]

    res: int = 0

    if violation == 1:
        # Violation: Customer should not be able to change the setting for load profile display every minute
        trace_activities_att = {ACTIVITY_1_KEY: req_status,
                                ACTIVITY_2_KEY: timestamp - timedelta(seconds=19)}
        res = add_trace(case_id, activity_list, trace_activities_att, timestamp, event_id)
    elif violation == 2:
        # Violation: Data protection reasons if new customer within last 60 days
        trace_activities_att = {ACTIVITY_1_KEY: req_status,
                                ACTIVITY_2_KEY: prev_req_date,
                                ACTIVITY_3_KEY: timestamp - timedelta(days=30)}
        activity_list.append(ACTIVITY_3)
        res = add_trace(case_id, activity_list, trace_activities_att, timestamp, event_id)
    elif violation == 3:
        # Violation: Synchronization should happen at most twice in a day
        trace_activities_att = {ACTIVITY_1_KEY: req_status,
                                ACTIVITY_2_KEY: prev_req_date,
                                ACTIVITY_3_KEY: cus_reg_date,
                                ACTIVITY_4_KEY: 3}
        activity_list.extend([ACTIVITY_3, ACTIVITY_4])
        res = add_trace(case_id, activity_list, trace_activities_att, timestamp, event_id)
    elif violation == 4:
        # Violation: Correct Synchronization value for activation (set correct value)
        trace_activities_att = {ACTIVITY_1_KEY: req_status,
                                ACTIVITY_2_KEY: prev_req_date,
                                ACTIVITY_3_KEY: cus_reg_date,
                                ACTIVITY_4_KEY: sync_list,
                                ACTIVITY_5_KEY: SynchronizationStatus.SYNCHRONIZED.name,
                                ACTIVITY_6_KEY: 0 if req_status == 1 else 0}
        activity_list.extend([ACTIVITY_3, ACTIVITY_4, ACTIVITY_5, ACTIVITY_6])
        res = add_trace(case_id, activity_list, trace_activities_att, timestamp, event_id)
    elif violation == 5:
        # Violation: Correct Synchronization value for deactivation (set correct value)
        trace_activities_att = {ACTIVITY_1_KEY: req_status,
                                ACTIVITY_2_KEY: prev_req_date,
                                ACTIVITY_3_KEY: cus_reg_date,
                                ACTIVITY_4_KEY: sync_list,
                                ACTIVITY_5_KEY: SynchronizationStatus.SYNCHRONIZED.name,
                                ACTIVITY_7_KEY: 0 if req_status == 1 else 0}
        activity_list.extend([ACTIVITY_3, ACTIVITY_4, ACTIVITY_5, ACTIVITY_7])
        res = add_trace(case_id, activity_list, trace_activities_att, timestamp, event_id)
    elif violation == 6:
        # Violation: The meter reports the correct status to the central system for activation
        trace_activities_att = {ACTIVITY_1_KEY: req_status,
                                ACTIVITY_2_KEY: prev_req_date,
                                ACTIVITY_3_KEY: cus_reg_date,
                                ACTIVITY_4_KEY: sync_list,
                                ACTIVITY_5_KEY: SynchronizationStatus.SYNCHRONIZED.name,
                                ACTIVITY_6_KEY: req_status,
                                ACTIVITY_8_KEY: ReportStatus.EVENT.name if req_status == 0 else ReportStatus.ALARM.name}
        activity_list.extend([ACTIVITY_3, ACTIVITY_4, ACTIVITY_5, ACTIVITY_6, ACTIVITY_8])
        res = add_trace(case_id, activity_list, trace_activities_att, timestamp, event_id)
    elif violation == 7:
        # Violation: The meter reports the correct status to the central system for deactivation
        trace_activities_att = {ACTIVITY_1_KEY: req_status,
                                ACTIVITY_2_KEY: prev_req_date,
                                ACTIVITY_3_KEY: cus_reg_date,
                                ACTIVITY_4_KEY: sync_list,
                                ACTIVITY_5_KEY: SynchronizationStatus.SYNCHRONIZED.name,
                                ACTIVITY_7_KEY: req_status,
                                ACTIVITY_8_KEY: ReportStatus.EVENT.name if req_status == 0 else ReportStatus.ALARM.name}
        activity_list.extend([ACTIVITY_3, ACTIVITY_4, ACTIVITY_5, ACTIVITY_7, ACTIVITY_8])
        res = add_trace(case_id, activity_list, trace_activities_att, timestamp, event_id)
    elif violation == 8:
        # Violation: The meter reports the correct status to the central system for activation
        trace_activities_att = {ACTIVITY_1_KEY: req_status,
                                ACTIVITY_2_KEY: prev_req_date,
                                ACTIVITY_3_KEY: cus_reg_date,
                                ACTIVITY_4_KEY: sync_list,
                                ACTIVITY_5_KEY: SynchronizationStatus.SYNCHRONIZED.name,
                                ACTIVITY_6_KEY: req_status,
                                ACTIVITY_8_KEY: reg_status,
                                ACTIVITY_9_KEY: ReportStatus.EVENT.name if req_status == 0 else ReportStatus.ALARM.name}
        activity_list.extend([ACTIVITY_3, ACTIVITY_4, ACTIVITY_5, ACTIVITY_6, ACTIVITY_8, ACTIVITY_9])
        res = add_trace(case_id, activity_list, trace_activities_att, timestamp, event_id)
    elif violation == 9:
        # Violation: The meter reports the correct status to the central system for deactivation
        trace_activities_att = {ACTIVITY_1_KEY: req_status,
                                ACTIVITY_2_KEY: prev_req_date,
                                ACTIVITY_3_KEY: cus_reg_date,
                                ACTIVITY_4_KEY: sync_list,
                                ACTIVITY_5_KEY: SynchronizationStatus.SYNCHRONIZED.name,
                                ACTIVITY_7_KEY: req_status,
                                ACTIVITY_8_KEY: reg_status,
                                ACTIVITY_9_KEY: ReportStatus.EVENT.name if req_status == 0 else ReportStatus.ALARM.name}
        activity_list.extend([ACTIVITY_3, ACTIVITY_4, ACTIVITY_5, ACTIVITY_7, ACTIVITY_8, ACTIVITY_9])
        res = add_trace(case_id, activity_list, trace_activities_att, timestamp, event_id)
    elif violation == 10:
        # Violation: When activated, the consumption time series is available on the meter display for customers
        trace_activities_att = {ACTIVITY_1_KEY: req_status,
                                ACTIVITY_2_KEY: prev_req_date,
                                ACTIVITY_3_KEY: cus_reg_date,
                                ACTIVITY_4_KEY: sync_list,
                                ACTIVITY_5_KEY: SynchronizationStatus.SYNCHRONIZED.name,
                                ACTIVITY_6_KEY: req_status,
                                ACTIVITY_8_KEY: reg_status,
                                ACTIVITY_9_KEY: reg_status,
                                ACTIVITY_10_KEY: req_status,
                                ACTIVITY_11_KEY: MeterViewStatus.DISPLAY_OFF.name}
        activity_list.extend([ACTIVITY_3, ACTIVITY_4, ACTIVITY_5, ACTIVITY_6, ACTIVITY_8, ACTIVITY_9,
                              ACTIVITY_10, ACTIVITY_11])
        res = add_trace(case_id, activity_list, trace_activities_att, timestamp, event_id)
    elif violation == 11:
        # Violation: When deactivated, the consumption time series is no longer visible on the meter display for
        # customers
        trace_activities_att = {ACTIVITY_1_KEY: req_status,
                                ACTIVITY_2_KEY: prev_req_date,
                                ACTIVITY_3_KEY: cus_reg_date,
                                ACTIVITY_4_KEY: sync_list,
                                ACTIVITY_5_KEY: SynchronizationStatus.SYNCHRONIZED.name,
                                ACTIVITY_7_KEY: req_status,
                                ACTIVITY_8_KEY: reg_status,
                                ACTIVITY_9_KEY: reg_status,
                                ACTIVITY_10_KEY: req_status,
                                ACTIVITY_11_KEY: MeterViewStatus.DISPLAY_ON.name}
        activity_list.extend([ACTIVITY_3, ACTIVITY_4, ACTIVITY_5, ACTIVITY_7, ACTIVITY_8, ACTIVITY_9,
                              ACTIVITY_10, ACTIVITY_11])
        res = add_trace(case_id, activity_list, trace_activities_att, timestamp, event_id)

    # Replace last violation entry the underlying violation number
    dataset[COLUMN_7][-1] = violation
    return res


def simulate_probability(ceiling: int) -> None:
    """
    Monte Carlo simulation to estimate the percentage of exceeding 5 minutes of a trace as stated in the SLAs.
    :param ceiling: The upper limit of the random int.
    """
    total_trials = 100_000
    exceed_count = 0

    for _ in range(total_trials):
        total_seconds = sum(random.randint(0, ceiling) for _ in range(11))
        if total_seconds > 300:
            exceed_count += 1

    print(
        f"With an upper limit of {ceiling}, "
        f"the probability of exceeding 300 seconds is about {exceed_count / total_trials * 100:.2f}%")


# counter for event ids starting at 22401
event_counter: int = 22_401

# Generate 20,000 correct traces
NUM_TRACES_TO_GENERATE = 20_000
for i in range(NUM_TRACES_TO_GENERATE):
    # generate random date between 2014 and 2024
    random_date = datetime(2024, 12, 31, 23, 59, 59) - timedelta(minutes=random.uniform(0, 365.25 * 24 * 60))
    event_counter = gen_correct_trace(random_date, i, event_counter)

# Generate 200 traces for each violation
NUM_VIOLATIONS_TO_GENERATE = 200
for i in range(1, 12):
    for index in range(NUM_VIOLATIONS_TO_GENERATE):
        # generate random date between 2014 and 2024
        random_date = datetime(2024, 12, 31, 23, 59, 59) - timedelta(minutes=random.uniform(0, 365.25 * 24 * 60))
        event_counter = gen_violation(random_date, NUM_TRACES_TO_GENERATE + index + i * NUM_VIOLATIONS_TO_GENERATE,
                                      event_counter, i)

df = DataFrame.from_dict(dataset, orient='columns')
df.to_excel('smart_meter_3-5_logs.xlsx')
