SMART_METER_PROMPT_1 = """
Task Overview:
- As an expert in process mining and NLP, your task is to analyze a descriptive text file ('descriptive_file') and an activities list ('activities_list') from event log datasets. Your objective is to extract business process constraints that are relevant to the activities listed.

Input Context:
- Descriptive File ('descriptive_file'): Focus on information and metrics relevant to business process requirements that relate to activities in the activities_list. Exclude any irrelevant details.
- Activities List ('activities_list'): Concentrate on the activities listed. Be aware that the 'descriptive_file' may use different terms or synonyms for these activities.

Work and Output Expectations:
-Analyze the 'activities_list' and use it to guide the extraction of relevant business process constraints from the 'descriptive_file'.
- Format each constraint with an identifier "c[i] = ", where [i] is an incremental number starting at 1.
- For each Constraint, detail the following:
    - Two process activities that are related.
    - The relationship between these activities (whether one directly follows the other or eventually follows).
    - The constraint conditions that the first activity must meet to perform the second activity without violating the compliance rules detailed in the 'descriptive_file'.
- Provide concise descriptions for each constraint or group of constraints, explaining the circumstances under which they apply or the reasons for their existence. Position these descriptions above the relevant constraints using this format:
\"\"\" 
# [description for a group of constraints] 
## [description for a single constraint] 
\"\"\"
- For each constraint, use the format:
    - c[i] = ({[activity_1]}, {[activity_2]}, {[relationship]}, {[constraint]})).
    - [activity_1] should be replaced with the first activity. 
	- [activity_2] should be replaced with the subsequent activity. 
	- [relationship] should be replaced with the term 'directly follows' or 'eventually follows' that states that the second activity either happens directly or eventually after the first one.
	- [constraint] should be replaced with the constraint conditions that should be adhered on [activity_1] in order to perform [activity_2] without violating process rules described in the descriptive_file. If there is more than one condition, separate them with 'AND'. If a condition entails value ranges or numerical metrics, make sure to convert the input text into a mathematical inequality format.
- Focus solely on outputting constraints in the specified format, accompanied by concise descriptions. Please avoid including descriptions of what you will perform.

Example:
descriptive_file:
\"\"\"
Employees must wear yellow and carmine vests while working on products! Managers are very strict on quality standards imposed by SLAs inside this document!
Before a product is shipped, it needs to undergo a quality check and reach a quality mark of at least 50 points. If a product reaches less than 50 points of quality but more than 40, range (40, 50), then it is sent to a deviance evaluation management facility. However, in case a product was not packed with a cardboard box, it will be sent to deviance evaluation management facility regardless of the quality points score.
After a product is shipped, there needs to be a waiting period of at least 24 hours in order to start tracking information on shipping development status.
If the production status during the action of producing a product results in an error, then no product quality verification is done and the product is sequentially sent for deviance evaluation. 
At the end of shifts, employees are not allowed to take their yellow vests home!
\"\"\"

activities_list:
Example of an activities_list that will be given to you:
\"\"\"
[plan product, produce product, verify product's quality standards, ship product, send to deviance evaluation, receive shipping updates]
\"\"\"

Expected Output:
\"\"\"
## Product needs to meet quality mark of at least 50 points and have a cardboard package before being shipped
c1 = ({verify product's quality standards}, {ship product}, {directly follows}, {quality mark >= 50 AND package = cardboard box}))

## After product is shipped, wait 1 day to track updates
c2 = ({ship product}, {receive shipping updates}, {directly follows}, {waiting period >= 24 hours}))

## Product to deviance evaluation for having less than 50 points of quality but more than 40
c3 = ({verify product's quality standards}, {send to deviance evaluation}, {directly follows}, {40 < quality points < 50}))

## Encountered an error during product production, send to deviation without analyzing quality
c4 = ({produce product}, {send to deviance evaluation}, {directly follows}, {error during production}))
\"\"\"

activities_list:
\"\"\"
['Request Consumption Display', "Retrieve Customer's Last Request Time", "Retrieve Customer's Registration Date", 'Get Number of Customer Change Requests 24h', 'Request Meter Synchronization', 'Activate Consumption Display', 'Deactivate Consumption Display', 'Register Logbook Entry', 'Report Display Status', 'Register Display Status', 'View Consumption Display']
\"\"\"

descriptive_file:
\"\"\"
For reasons of data protection law, the display of consumption time series, for example: load profile on the display via the call button, is only permitted in special cases. It must be possible to activate or deactivate the display of the consumption time series via the meter's WAN interface. The status is to be transmitted to the central system as ALARM or EVENT and entered in the logbook. In the basic setting of the meter, the display of the consumption time series must always be deactivated.
Whether the display of the consumption time series, for example: load profile is active or inactive, is decided by the customer. He informs the NB (via web portal, via the call center, letter, ...). A synchronization of the device setting with respect to the consumption time series display is usefully 1 - 2 times a day (Customer should not be able to change the setting for load profile display every minute).
When the consumption time series display is activated, the customer has the option to view the load profile for the last 60 days directly on the meter display. Unless it is in the course of a customer change to a new customer based on the plant. Then a 60-day deactivation of the consumption time series display for data protection reasons is necessary.

The customer wishes to activate the consumption time series display on the meter display and notify the NB or the customer wishes to deactivate the consumption time series display on the meter display and inform the NB about this.

When activated, the consumption time series is available on the meter display for customers.
When deactivated, the consumption time series is no longer visible on the meter display for customers.
In both cases, the meter reports its status to the central system as ALARM or EVENT ("CS Display OFF" or "CS Display ON") and entry in the logbook of the meter.
\"\"\"
"""


SMART_METER_PROMPT_2 = """
Task Overview:
- As an expert in process mining and NLP, your task is to analyze a descriptive text file ('descriptive_file') and an activities list ('activities_list') from event log datasets. Your objective is to extract business process constraints that are relevant to the activities listed.

Input Context:
- Descriptive File ('descriptive_file'): Focus on information and metrics relevant to business process requirements that relate to activities in the activities_list. Exclude any irrelevant details.
- Activities List ('activities_list'): The activities_list describes a business process model that is represented through a unique format containing a numerated series (starting at 1) of pairs of two activities or one activity and one node. Each pair is separated by the symbol “->”; this symbol represents a “directly follows” relationship.  Each node is classified as a {XORi} or {ANDi} type, indicating different branching behaviors in the process flow, and “i” is a number starting from 1 and being incremented by 1 every time a new node is defined; each node type has their own count. The start of the model is represented as {START} and the end as {END}.

Work and Output Expectations:
-Analyze the 'activities_list' and use it to guide the extraction of relevant business process constraints from the 'descriptive_file'.
- Format each constraint with an identifier "c[i] = ", where [i] is an incremental number starting at 1.
- For each Constraint, detail the following:
    - Two process activities that are related.
    - The relationship between these activities (whether one directly follows the other or eventually follows).
    - The constraint conditions that the first activity must meet to perform the second activity without violating the compliance rules detailed in the 'descriptive_file'.
- Provide concise descriptions for each constraint or group of constraints, explaining the circumstances under which they apply or the reasons for their existence. Position these descriptions above the relevant constraints using this format:
\"\"\"
# [description for a group of constraints]
## [description for a single constraint]
\"\"\"
- For each constraint, use the format:
    - c[i] = ({[activity_1]}, {[activity_2]}, {[relationship]}, {[constraint]})).
    - [activity_1] should be replaced with the first activity. 
	- [activity_2] should be replaced with the subsequent activity. 
	- [relationship] should be replaced with the term 'directly follows' or 'eventually follows' following the syntax explanation provided in the beforementioned "Input Context" section and the data provided in the descriptive_file. For example, activity_1 'directly follows' activity_2 if there is an entry “1. activity_1 -> activity_2” or if activity_1 directly follows a node and the node directly follows activity_2 such as “1. activity_1 -> {XOR1}, 2. {XOR1} -> activity_2”. For the term 'eventually follows', activity_1 'eventually follows' activity_3 if there are entries like in this example, "1. activity_1 -> activity_2, 2. activity_2 -> activity_3".
	- [constraint] should be replaced with the constraint conditions that should be adhered on [activity_1] in order to perform [activity_2] without violating process rules described in the descriptive_file. If there is more than one condition, separate them with 'AND'. If a condition entails value ranges or numerical metrics, make sure to convert the input text into a mathematical inequality format.
- Focus solely on outputting constraints in the specified format, accompanied by concise descriptions. Please avoid including descriptions of what you will perform.

Example:
descriptive_file:
\"\"\"
Employees must wear yellow and carmine vests while working on products! Managers are very strict on quality standards imposed by SLAs inside this document!
Before a product is shipped, it needs to undergo a quality check and reach a quality mark of at least 50 points. If a product reaches less than 50 points of quality but more than 40, range (40, 50), then it is sent to a deviance evaluation management facility. However, in case a product was not packed with a cardboard box, it will be sent to deviance evaluation management facility regardless of the quality points score.
After a product is shipped, there needs to be a waiting period of at least 24 hours in order to start tracking information on shipping development status.
If the production status during the action of producing a product results in an error, then no product quality verification is done and the product is sequentially sent for deviance evaluation. Products sent to deviance evaluation are examined and then sent for product discard.
At the end of shifts, employees are not allowed to take their yellow vests home!
\"\"\"

activities_list:
Example of an activities_list that will be given to you:
\"\"\"
1. {START} -> 'plan product'
2. 'plan product' -> 'produce product'
3. 'produce product' -> {XOR1}
4. {XOR1} -> 'verify product's quality standards'
5. {XOR1} -> 'send to deviance evaluation'
6. 'verify product's quality standards' -> {XOR2}
7. {XOR2} -> 'ship product'
8. {XOR2} -> 'send to deviance evaluation'
9. 'ship product' -> 'receive shipping updates'
10. 'send to deviance evaluation' -> 'send to product discard'
11. 'receive shipping updates' -> {END}
12. 'send to product discard' -> {END}
\"\"\"

Expected Output:
## Product needs to meet quality mark of at least 50 points and have a cardboard package before being shipped
c1 = ({verify product's quality standards}, {ship product}, {directly follows}, {quality mark >= 50 AND package = cardboard box}))

## After product is shipped, wait 1 day to track updates
c2 = ({ship product}, {receive shipping updates}, {directly follows}, {waiting period >= 24 hours}))

## Product to deviance evaluation for having less than 50 points of quality but more than 40
c3 = ({verify product's quality standards}, {send to deviance evaluation}, {directly follows}, {40 < quality points < 50}))

## Encountered an error during product production, send to deviation without analyzing quality
c4 = ({produce product}, {send to deviance evaluation}, {directly follows}, {production_status = ERROR}))

## Encountered an error during product production, send to deviation without analyzing quality
c5 = ({produce product}, {product discard}, {eventually follows}, {production_status = ERROR}))

activities_list:
\"\"\"
1. {START} -> 'Request Consumption Display'
2. 'Retrieve Customer's Last Request Time' -> {XOR1}
3. {XOR1} -> {END}
4. {XOR1} -> 'Retrieve Customer's Registration Date'
5. 'Retrieve Customer's Registration Date' -> {XOR2}
6. {XOR2} -> {END}
7. {XOR2} -> 'Get Number of Customer Change Requests 24h'
8. 'Retrieve Number of Customer Change Requests 24h' -> {XOR3}
9. {XOR3} -> {END}
10. {XOR3} -> 'Request Meter Synchronization'
11. 'Retrieve Number of Customer Change Requests 24h' -> {XOR4}
12. {XOR4} -> 'Activate Consumption Display'
13. {XOR4} -> 'Deactivate Consumption Display'
14. 'Activate Consumption Display' -> 'View Consumption Display'
15. 'Deactivate Consumption Display' -> 'View Consumption Display'
16. 'Activate Consumption Display' -> {AND1}
17. 'Deactivate Consumption Display' -> {AND1}
18. {AND1} -> 'Register Logbook Entry'
19. {AND1} -> 'Report Display Status'
20. 'Report Display Status' -> 'Register Display Status'
21. 'Register Display Status' -> {END}
22. 'View Consumption Display' -> {END}
23. 'Register Logbook Entry' -> {END}
24. 'Report Display Status' -> {END}
\"\"\"

descriptive_file:
\"\"\"
For reasons of data protection law, the display of consumption time series, for example: load profile on the display via the call button, is only permitted in special cases. It must be possible to activate or deactivate the display of the consumption time series via the meter's WAN interface. The status is to be transmitted to the central system as ALARM or EVENT and entered in the logbook. In the basic setting of the meter, the display of the consumption time series must always be deactivated.
Whether the display of the consumption time series, for example: load profile is active or inactive, is decided by the customer. He informs the NB (via web portal, via the call center, letter, ...). A synchronization of the device setting with respect to the consumption time series display is usefully 1 - 2 times a day (Customer should not be able to change the setting for load profile display every minute).
When the consumption time series display is activated, the customer has the option to view the load profile for the last 60 days directly on the meter display. Unless it is in the course of a customer change to a new customer based on the plant. Then a 60-day deactivation of the consumption time series display for data protection reasons is necessary.

The customer wishes to activate the consumption time series display on the meter display and notify the NB or the customer wishes to deactivate the consumption time series display on the meter display and inform the NB about this.

When activated, the consumption time series is available on the meter display for customers.
When deactivated, the consumption time series is no longer visible on the meter display for customers.
In both cases, the meter reports its status to the central system as ALARM or EVENT ("CS Display OFF" or "CS Display ON") and entry in the logbook of the meter.
\"\"\"
"""