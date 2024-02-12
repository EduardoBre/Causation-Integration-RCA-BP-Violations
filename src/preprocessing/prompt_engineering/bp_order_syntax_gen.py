BP_ORDER_LIST = []
START_ID = '{START}'
END_ID = '{END}'
DF_ID = ' -> '


def add_start_df_activity(activity: str) -> None:
    """
    Adds a pair of START_ID --(directly follows)--> activity.
    :param activity: The activity which proceeds the start of the business process.
    """
    s = START_ID + DF_ID + f"'{activity}'"
    BP_ORDER_LIST.append(s)


def add_activity_df_end(activity: str) -> None:
    """
    Adds a pair of activity --(directly follows)--> END_ID.
    :param activity: The activity that directly follows the end of the business process.
    """
    s = f"'{activity}'" + DF_ID + END_ID
    BP_ORDER_LIST.append(s)


def add_activity_df_xor(activity: str, xor_id: int) -> None:
    """
    Adds a pair of activity --(directly follows)--> XOR[xor_id].
    :param activity: The activity that directly follows the referenced XOR.
    :param xor_id: The number of the referenced XOR.
    """
    s = f"'{activity}'" + DF_ID + f"{{XOR{xor_id}}}"
    BP_ORDER_LIST.append(s)


def add_xor_df_activity(activity: str, xor_id: int) -> None:
    """
    Adds a pair of XOR[xor_id] --(directly follows)--> activity.
    :param activity: The activity that directly follows the referenced XOR.
    :param xor_id: The number of the referenced XOR.
    """
    s = f"{{XOR{xor_id}}}" + DF_ID + f"'{activity}'"
    BP_ORDER_LIST.append(s)


def add_activity_df_and(activity: str, and_id: int) -> None:
    """
    Adds a pair of activity --(directly follows)--> AND[and_id].
    :param activity: The activity that directly follows the referenced AND.
    :param and_id: The number of the referenced AND.
    """
    s = f"'{activity}'" + DF_ID + f"{{AND{and_id}}}"
    BP_ORDER_LIST.append(s)


def add_and_df_activity(activity: str, and_id: int) -> None:
    """
    Adds a pair of AND[and_id] --(directly follows)--> activity.
    :param activity: The activity that directly follows the referenced AND.
    :param and_id: The number of the referenced AND.
    """
    s = f"{{AND{and_id}}}" + DF_ID + f"'{activity}'"
    BP_ORDER_LIST.append(s)


def add_activity_df_activity(activity_1: str, activity_2: str) -> None:
    """
    Adds a pair of activity --(directly follows)--> activity.
    :param activity_1: The activity which leads the other of the business process.
    :param activity_2: The activity which proceeds the other of the business process.
    """
    s = f"'{activity_1}'" + DF_ID + f"'{activity_2}'"
    BP_ORDER_LIST.append(s)


def add_xor_df_end(xor_id: int) -> None:
    """
    Adds a pair of XOR[xor_id] --(directly follows)--> END_ID.
    :param xor_id: The XOR number that follows the end of the process.
    """
    s = f"{{XOR{xor_id}}}" + DF_ID + END_ID
    BP_ORDER_LIST.append(s)


def print_complete_syntax() -> None:
    """
    Prints the complete syntax and deletes current state.
    """
    print('--- START OF ORDER SYNTAX --')
    for counter, pair in enumerate(BP_ORDER_LIST, start=1):
        print(f"{counter}. " + pair)
    BP_ORDER_LIST.clear()
    print('--- END OF ORDER SYNTAX --')


# Create Order Syntax for prompt example:
add_start_df_activity('plan product')
add_activity_df_activity('plan product', 'produce product')
add_activity_df_xor('produce product', 1)
add_xor_df_activity("verify product's quality standards", 1)
add_xor_df_activity('send to deviance evaluation', 1)
add_activity_df_xor("verify product's quality standards", 2)
add_xor_df_activity("ship product", 2)
add_xor_df_activity('send to deviance evaluation', 2)
add_activity_df_activity('ship product', 'receive shipping updates')
add_activity_df_end('receive shipping updates')
print_complete_syntax()

# Create Order Syntax for Coffee Roasting Process:
add_start_df_activity('Height Measure')
add_activity_df_activity('Height Measure', 'Moisture Measure')
add_activity_df_activity('Moisture Measure', 'Roast Degree Selection')
add_activity_df_activity('Roast Degree Selection', 'Roasting Chamber 1')
add_activity_df_activity('Roasting Chamber 1', 'Roasting Chamber 2')
add_activity_df_activity('Roasting Chamber 2', 'Roasting Chamber 3')
add_activity_df_xor('Roasting Chamber 3', 1)
add_xor_df_activity('Roasting Chamber 4', 1)
add_xor_df_activity('Final Measure', 1)
add_activity_df_xor('Roasting Chamber 4', 2)
add_xor_df_activity('Roasting Chamber 5', 2)
add_xor_df_activity('Final Measure', 2)
add_activity_df_activity('Final Measure', 'Quality Assessment')
add_activity_df_end('Quality Assessment')
print_complete_syntax()

# Create Order Syntax for Coffee Roasting Process:
add_start_df_activity('Request Consumption Display')
add_activity_df_xor("Retrieve Customer's Last Request Time", 1)
add_xor_df_end(1)
add_xor_df_activity("Retrieve Customer's Registration Date", 1)
add_activity_df_xor("Retrieve Customer's Registration Date", 2)
add_xor_df_end(2)
add_xor_df_activity('Retrieve Number of Customer Change Requests 24h', 2)
add_activity_df_xor('Retrieve Number of Customer Change Requests 24h', 3)
add_xor_df_end(3)
add_xor_df_activity('Request Meter Synchronization', 3)
add_activity_df_xor('Retrieve Number of Customer Change Requests 24h', 4)
add_xor_df_activity('Activate Consumption Display', 4)
add_xor_df_activity('Deactivate Consumption Display', 4)
add_activity_df_activity('Activate Consumption Display', 'View Consumption Display')
add_activity_df_activity('Deactivate Consumption Display', 'View Consumption Display')
add_activity_df_and('Activate Consumption Display', 1)
add_activity_df_and('Deactivate Consumption Display', 1)
add_and_df_activity('Register Logbook Entry', 1)
add_and_df_activity('Report Display Status', 1)
add_activity_df_activity('Report Display Status', 'Register Display Status')
add_activity_df_end('Register Display Status')
add_activity_df_end('View Consumption Display')
add_activity_df_end('Register Logbook Entry')
add_activity_df_end('Report Display Status')
print_complete_syntax()
