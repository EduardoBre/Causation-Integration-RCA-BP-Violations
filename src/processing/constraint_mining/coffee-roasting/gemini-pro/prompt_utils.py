COFFEE_ROASTING_PROMPT_1 = """
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
['Height Measure', 'Moisture Measure', 'Roast Degree Selection', 'Roasting Chamber 1', 'Roasting Chamber 2', 'Roasting Chamber 3', 'Roasting Chamber 4', 'Roasting Chamber 5', 'Final Measure']
\"\"\"

descriptive_file:
\"\"\"
<!--
For further explanation please refer to the PDF handbook documentation regarding the Coffee Roasting Process.
->

# Coffee Roasting Handbook 1st Edition Exclusive!

# About our Coffee:

To achieve excellence, we roast our coffee on a weekly basis directly in our coffeehouse. However, there are two primary things to know about our coffee roasting process: where we get our beans and how we roast them.
We import green coffee beans from the coffee-growing regions of the world, which are generally between the Tropic of Cancer and the Tropic of Capricorn, where conditions are ideal for coffee cherries to grow. We have established good connections with great importers and farmers to get the absolute best coffee that benefits everyone involved, from the farmer to the importer to the coffee drinker in our coffee house.
The coffees we source are, at a minimum, Fair Trade certified. The goal of Fair Trade is to create partnerships and terms of trade that will be financially and ethically beneficial to producers in developing countries. In simpler terms, this means the beans we roast are bought at a fair price that allows the hardworking people growing the coffee to make a living off their wages and not be exploited.
Additionally, we will refer to one of the many coffees we offer as “direct trade.” While there is no international certification for direct trade, as there is with Fair Trade, the general concept of direct trade is that our importers purchase beans directly from individual farmers. Fair Trade beans are typically purchased through coops, where several farmers deliver their beans, which are then combined for sale, so there is no direct traceability of the beans back to a particular farm. This obviously doesn’t match the exceptionally high regard we have for our customers. Therefore, with direct trade we are able to pinpoint to you the specific farmer who produced the beans. These beans are typically of the highest quality and the exceptional farmers end up receiving a higher percentage of the price you pay for your coffee in our great coffeehouse.
Once the beans arrive at the coffeehouse in 100-pound bags and boxes, we then roast them on-demand in our roasting room. We use what is referred to as a roasting chamber, as opposed to a drum roaster used by most other coffee roasters. We believe there are some unique advantages to our chamber roasting process. The chamber roasting process, also known as hot air roasting, uses forced hot air to agitate and roast coffee beans. The perfectly controlled stifling air flows over a tilted bed and circulates through the beans, roasting each bean evenly. This hot air reaches very high temperatures.
We believe this method of roasting creates one of the best coffees you will ever taste for a few reasons. First, it has a unique method of removing the chaff that the coffee beans shed as they heat. This is important because coffee beans are so absorbent if the chaff remained in the chamber during the roast, as it does in drum roasters, it would soak up some of that unwanted flavor.
Another reason is its efficiency in heat transference. Our machines can reach higher temperatures in half of the time of many drum roasters, which is absolutely essential to ensuring a smooth cup of coffee with the least amount of acidity possible. Before the roasting process can indeed extract the essential flavors of a given coffee bean, the natural moisture needs to be extracted. The longer it takes to do this the more time it allows for acids to build up and block the real flavor of the bean and potentially cause stomach irritation. So, by reaching a higher temperature faster we minimize acid buildup and genuinely highlight the bean's natural flavors. Naturally, the moisture is handled by our exceptional roasting chambers and although it is always measured, it does not change anything for us since we can’t directly manipulate the moisture level.
Just like corn in Indiana, coffee is a seasonal crop so you may notice different coffees during various times of the year. This is because we are committed to providing the freshest and tastiest cup of coffee, which means sometimes a particular type of bean just is not in season.
We provide brief descriptions of each bean and blend on the bags. Our goal is to present highly drinkable coffee through blends and single origins.

# Controls and Basic Settings:

## Power Switch: 
The power switch is the upper-left knob on the main power system visible in the control panel. It turns stiffly, as it is a mechanical timer. The on position is fully clockwise, and the off position is fully anticlockwise. Its primary function is a safety switch; it will automatically switch off the roaster if not manually reset periodically. The switch can also function as a timer, in which case it operates as follows:
-> 9 o'clock: 10 minutes
-> 12 o'clock: 20-minutes
-> 3 o'clock: 30-minutes
Before charging the roaster with green beans, turn the switch fully on. Alternatively, set it to run for a little longer than the predicted time for the roast. If the roaster stops during the process, immediately turn the switch back on.

## Heater Control: 
The knob at the bottom-left of the control panel steplessly adjusts the heater current from entirely off to fully on. As the heaters warm and cool, their resistance changes slightly, which causes the current to drift away somewhat from the intended setting. Thus, it is necessary to readjust the electrical current back to the desired setting a few minutes after changing the setting to obtain a precise heat level.

## Ammeter: The ammeter is on the upper left of the control panel. It measures the electrical current flowing through the heaters. Each mark on the meter corresponds to 0.5-Ampere. One can convert the displayed electrical current to the consumed power with the formula P=I*E, where P is the power (watts), I is the current intensity (amperes), and E is the electromotive force (volts). Alternatively, use an energy monitor such as a KIll-a-Watt®.

## Blower Control: The blower is multi-purpose; it moves air through the roaster, removes chaff from the roasting chamber, and can cool the roasted beans. The knob at the bottom-right of the control panel steplessly adjusts the blower level. There are two versions of this control. On some models, the blower is always on. On other models, the blower stays off from the lowest setting to about 3.8, at which point it begins to turn. Although the dial has higher graduations, it does not turn past 8.

## Thermometer: The bean temperature displayed on the thermometer is a relative value, not the actual bean temperature. The BT indicated by thermometers on all roasters varies, mainly depending on the probe’s placement and the batch size. It is advisable to correlate the displayed temperature to the actual bean temperature at known points. The appendix contains a table to record corrected values for future reference. The temperature displayed via the ET port, on the other hand, is accurate. For our use case, using heat sensors inside the roasting chambers is the best option. In fact, we have 3 different heat sensors inside each temperature sensor.

## Electrical circuit Breaker: 
The circuit breaker is at the roaster’s back, next to the power cord. It shuts down the roaster if there is a failure causing an excessive current draw. If the roaster does not operate, reset the breaker by depressing the button. If the breaker opens again, the roaster needs repair.

# Roasting process:
We roast our own coffee in the coffeehouse on a weekly basis. There are two primary things to know about our coffee roasting: the roasting degrees, the height of the coffee trays, and the oven temperatures.

## Roasting Degrees:

Coffee roasting is one of the most influential factors of coffee taste. Roasting transforms green beans into the aromatic and flavorful coffee that wakes our senses in the morning. However, roasting beans at various levels achieves more than merely darkening the beans; it also changes many of the beans’ physical attributes as well.

## Height of Coffee Trays:

Every coffee pile in a tray has a different height measured in mm (millimeters). Obviously, the higher the pile, the more heat an oven would require to achieve the desired roasting degree. The reverse effect happens on lower piles, which would require less oven heat. Therefore, the height of our coffee in the trays is a factor of most importance to the successful accomplishment of our excellent coffee roasting process and thus needs to be considered whenever analyzing the result of a roasting process!

## Oven Temperatures:

In total, our facility possesses 5 ovens, and each oven is equipped with 3 state-of-the-art heat sensors. For our use case, it is obviously essential to analyze the highest and lowest temperatures recorded by the heat sensors. The lowest recordable temperature is 0° and the highest is 1000°. The sensors themselves were handcrafted by our own engineers who not only have years of background in the coffee roasting industry but also wanted to outdo themselves and create a unique temperature sensor specifically for our niche! If any damages or malfunctions are to be experienced, then it is crucial that the upper management is notified without any delays! Insulating the Roasting Chamber is also an option: Some owners add a layer of heat-proof insulation around the exterior of the roasting chamber. This insulation allows the Quest to retain more heat, increasing capacity and the speed of heating. However, the downside is that if the user wishes to dump heat when a roast is getting too hot, it will be slower.

## Roasting Guidelines:

In general, we first distinguish between three roasting degrees: light, medium, and dark. Secondly, we have to acknowledge the coffee pile height in the tray as that plays a big role in the temperature of the roasting ovens which is the third and last constraint that needs to be abided by. Due to logistics, the moisture levels are recorded as metrics but they are not relevant for the violation analysis since there are no feasible measures to change the moisture levels of the coffee beans. Similarly, the amount of time a coffee batch spends inside each of the roasting chambers can not be changed: Each roasting chamber takes 5 minutes. Therefore, moisture levels and timestamps are not really relevant for the final measure analysis.

For better understanding, we describe temperature rules with boundary temperatures t_min and t_max and distinguish between:
-> open brackets, e.g., (t_min, t_max), this means that the boundary temperatures ARE NOT included in the rules.
-> closed brackets, e.g., [t_min, t_max], this means that the boundary temperatures ARE included in the rules.

-> Light Roast:
Goes through roasting ovens 1,2 and 3.
Light roasts are light brown with no oil on the bean surface, with a toasted grain taste and noticeable acidity. A common misconception is that Light Roasts don’t have as much caffeine as their darker, bolder counterparts. However, the truth is precisely the opposite! As beans roast, the caffeine slowly cooks out of the beans. Therefore, because lightly roasted beans cook for a shorter time and at a lower temperature, they retain more caffeine from the original green coffee bean. Other roasters refer to a Light Roast as Light City Roast, New England Roast, or Cinnamon Roast.

We first distinguish between a tray height of less than 180mm and higher or equal to 180mm:

--> Coffee tray height lower than 180mm:
We inherently can not allow the temperature of roasting oven 1 to go below 120° or above 400°. Roasting oven 2 should maintain its temperature as [220°, 500°]. The final product will present a good quality if the highest temperatures of roasting oven 3 remain at 550°.

--> Coffee tray height of at least 180mm:
Roasting oven 1 should follow the temperature rule [140°, 420°]. Afterward, it is not allowed for roasting oven 2 to go above 520° or below 240°. Finally, the product will not pass the quality standard if roasting oven 3 fails to maintain its temperatures below 571°.


-> Medium Roast:
Goes through roasting ovens 1,2,3 and 4.
Medium roasts are medium brown to brown with no oil on the surface, although darker roasts in this group may appear slightly shiny. They are balanced, exhibiting significant flavor and aroma. Medium Roast coffees are brown and have a thicker body than a Light Roast. Unlike Light, Medium starts to take on a bit of the taste from the roasting process, losing some of the bright floral flavors typical of a Light Roast. Instead, they carry a much more balanced flavor with a medium amount of caffeine. A Medium is roasted until just before the second crack.
For a successful medium roast of coffee beans, the following technical requirements should be followed:

--> Coffee tray height of at most 170mm:
Temperatures of roasting 1 should follow [170°,450°].
Temperatures of roasting 2 should follow [270°,550°].
Temperatures of roasting 3 should follow [370°,650°].
Temperatures of roasting 4 should not exceed 550°.

--> Coffee tray height of at least 170mm:
Temperatures of roasting 1 should avoid (0°,180°) and (460°,1000°).
Temperatures of roasting 2 should avoid (0°,290°) and (570°,1000°).
Temperatures of roasting 3 should avoid (0°,390°) and (670°,1000°).
Temperatures of roasting 4 should reach at most 560°.


-> Dark Roast:
Dark roasts are dark brown to almost black, coffee beans roasted until they exude oils and therefore have an oil sheen glowing on the surface. The roasting process’s flavor overwhelms the beans’ flavor, and the coffee from some beans may taste spicy, bitter, or smoky.	To be considered Dark, beans roast to a temperature of anything higher than 440° or essentially to the end of the second crack. If beans roast much hotter than 780°, the coffee will start to taste more and more of charcoal and will not pass the final quality check. This roasting degree is the only one that requires the use of a roasting oven 5. If the coffee pile on the tray reaches 175mm and beyond, then the roasting oven 5 should not have its temperatures exceed 580°. Similarly, for coffee piles smaller than 175mm, roasting oven 5 should not go beyond 560°.
Many other big-batch roasters cut corners by roasting larger quantities faster at extremely high temperatures for a short amount of time but it is vital for us to still respect a new pattern of roasting beginning at oven chamber 1 if the coffee pile is at least 175mm high then roasting oven 1 should not exceed 580° and the lowest temperature allowed would be 220°, similarly for roasting oven 2 the temperatures reach at most 680° and go no lower than 320°. Continuing the process, if roasting oven 3 goes above 780° or if roasting oven 4 exceeds 680°, the final product will be rejected! The same outcome will happen if roasting oven 3 fails to maintain at least 421° or if roasting oven 4 goes lower than 320°.
However, for piles of other heights, roasting oven 1 should remain between 200° and 560° including both temperatures. These piles of other sizes can also accept temperatures of at least 300° and up to 660° for roasting chamber 2, however, if they surpass 760° or if the temperature drops below 400° at roasting oven 3, then the final product will undoubtedly be rejected. Finally, please respect that in order to achieve the first crack in the coffee beans, oven chamber 4 should go as high as 680° but not drop below 320°.


# Additional Information

## Increasing Capacity by painting the drum
Some Quest owners–to increase the maximum batch capacity or alter the roast environment’s thermal dynamics–paint the roasting drum’s exterior with high-heat matte black spray paint. Doing so causes the drum to efficiently absorb and conduct more infrared heat to the roast chamber independent of airflow speed (convection). Increasing the drum’s ability to absorb infrared heat increases the batch capacity, and heat changes are faster, even for large batch sizes (EG. <10 minutes, 300g roasts on an 400° M3).

## Coffee Bean Cooling
The supplied rectangular bean collector placed in the chaff collector cools the beans. This works but has several drawbacks. First, it is slow. Second, there is no air circulation through the roasting chamber with the bean collector inserted into the chaff collector. Use an external cooler instead, such as the optional one from the manufacturer or make one. Make a small box with a muffin fan in it and set the bean collector on top. The flow of ambient air through the beans is much more efficient than the Quests’ inbuilt cooling function.
\"\"\"
"""


COFFEE_ROASTING_PROMPT_2 = """
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
1. {START} -> 'Height Measure'
2. 'Height Measure' -> 'Moisture Measure'
3. 'Moisture Measure' -> 'Roast Degree Selection'
4. 'Roast Degree Selection' -> 'Roasting Chamber 1'
5. 'Roasting Chamber 1' -> 'Roasting Chamber 2'
6. 'Roasting Chamber 2' -> 'Roasting Chamber 3'
7. 'Roasting Chamber 3' -> {XOR1}
8. {XOR1} -> 'Roasting Chamber 4'
9. {XOR1} -> 'Final Measure'
10. 'Roasting Chamber 4' -> {XOR2}
11. {XOR2} -> 'Roasting Chamber 5'
12. {XOR2} -> 'Final Measure'
13. 'Final Measure' -> 'Quality Assessment'
14. 'Quality Assessment' -> {END}
\"\"\"

descriptive_file:
\"\"\"
<!--
For further explanation please refer to the PDF handbook documentation regarding the Coffee Roasting Process.
->

# Coffee Roasting Handbook 1st Edition Exclusive!

# About our Coffee:

To achieve excellence, we roast our coffee on a weekly basis directly in our coffeehouse. However, there are two primary things to know about our coffee roasting process: where we get our beans and how we roast them.
We import green coffee beans from the coffee-growing regions of the world, which are generally between the Tropic of Cancer and the Tropic of Capricorn, where conditions are ideal for coffee cherries to grow. We have established good connections with great importers and farmers to get the absolute best coffee that benefits everyone involved, from the farmer to the importer to the coffee drinker in our coffee house.
The coffees we source are, at a minimum, Fair Trade certified. The goal of Fair Trade is to create partnerships and terms of trade that will be financially and ethically beneficial to producers in developing countries. In simpler terms, this means the beans we roast are bought at a fair price that allows the hardworking people growing the coffee to make a living off their wages and not be exploited.
Additionally, we will refer to one of the many coffees we offer as “direct trade.” While there is no international certification for direct trade, as there is with Fair Trade, the general concept of direct trade is that our importers purchase beans directly from individual farmers. Fair Trade beans are typically purchased through coops, where several farmers deliver their beans, which are then combined for sale, so there is no direct traceability of the beans back to a particular farm. This obviously doesn’t match the exceptionally high regard we have for our customers. Therefore, with direct trade we are able to pinpoint to you the specific farmer who produced the beans. These beans are typically of the highest quality and the exceptional farmers end up receiving a higher percentage of the price you pay for your coffee in our great coffeehouse.
Once the beans arrive at the coffeehouse in 100-pound bags and boxes, we then roast them on-demand in our roasting room. We use what is referred to as a roasting chamber, as opposed to a drum roaster used by most other coffee roasters. We believe there are some unique advantages to our chamber roasting process. The chamber roasting process, also known as hot air roasting, uses forced hot air to agitate and roast coffee beans. The perfectly controlled stifling air flows over a tilted bed and circulates through the beans, roasting each bean evenly. This hot air reaches very high temperatures.
We believe this method of roasting creates one of the best coffees you will ever taste for a few reasons. First, it has a unique method of removing the chaff that the coffee beans shed as they heat. This is important because coffee beans are so absorbent if the chaff remained in the chamber during the roast, as it does in drum roasters, it would soak up some of that unwanted flavor.
Another reason is its efficiency in heat transference. Our machines can reach higher temperatures in half of the time of many drum roasters, which is absolutely essential to ensuring a smooth cup of coffee with the least amount of acidity possible. Before the roasting process can indeed extract the essential flavors of a given coffee bean, the natural moisture needs to be extracted. The longer it takes to do this the more time it allows for acids to build up and block the real flavor of the bean and potentially cause stomach irritation. So, by reaching a higher temperature faster we minimize acid buildup and genuinely highlight the bean's natural flavors. Naturally, the moisture is handled by our exceptional roasting chambers and although it is always measured, it does not change anything for us since we can’t directly manipulate the moisture level.
Just like corn in Indiana, coffee is a seasonal crop so you may notice different coffees during various times of the year. This is because we are committed to providing the freshest and tastiest cup of coffee, which means sometimes a particular type of bean just is not in season.
We provide brief descriptions of each bean and blend on the bags. Our goal is to present highly drinkable coffee through blends and single origins.

# Controls and Basic Settings:

## Power Switch: 
The power switch is the upper-left knob on the main power system visible in the control panel. It turns stiffly, as it is a mechanical timer. The on position is fully clockwise, and the off position is fully anticlockwise. Its primary function is a safety switch; it will automatically switch off the roaster if not manually reset periodically. The switch can also function as a timer, in which case it operates as follows:
-> 9 o'clock: 10 minutes
-> 12 o'clock: 20-minutes
-> 3 o'clock: 30-minutes
Before charging the roaster with green beans, turn the switch fully on. Alternatively, set it to run for a little longer than the predicted time for the roast. If the roaster stops during the process, immediately turn the switch back on.

## Heater Control: 
The knob at the bottom-left of the control panel steplessly adjusts the heater current from entirely off to fully on. As the heaters warm and cool, their resistance changes slightly, which causes the current to drift away somewhat from the intended setting. Thus, it is necessary to readjust the electrical current back to the desired setting a few minutes after changing the setting to obtain a precise heat level.

## Ammeter: The ammeter is on the upper left of the control panel. It measures the electrical current flowing through the heaters. Each mark on the meter corresponds to 0.5-Ampere. One can convert the displayed electrical current to the consumed power with the formula P=I*E, where P is the power (watts), I is the current intensity (amperes), and E is the electromotive force (volts). Alternatively, use an energy monitor such as a KIll-a-Watt®.

## Blower Control: The blower is multi-purpose; it moves air through the roaster, removes chaff from the roasting chamber, and can cool the roasted beans. The knob at the bottom-right of the control panel steplessly adjusts the blower level. There are two versions of this control. On some models, the blower is always on. On other models, the blower stays off from the lowest setting to about 3.8, at which point it begins to turn. Although the dial has higher graduations, it does not turn past 8.

## Thermometer: The bean temperature displayed on the thermometer is a relative value, not the actual bean temperature. The BT indicated by thermometers on all roasters varies, mainly depending on the probe’s placement and the batch size. It is advisable to correlate the displayed temperature to the actual bean temperature at known points. The appendix contains a table to record corrected values for future reference. The temperature displayed via the ET port, on the other hand, is accurate. For our use case, using heat sensors inside the roasting chambers is the best option. In fact, we have 3 different heat sensors inside each temperature sensor.

## Electrical circuit Breaker: 
The circuit breaker is at the roaster’s back, next to the power cord. It shuts down the roaster if there is a failure causing an excessive current draw. If the roaster does not operate, reset the breaker by depressing the button. If the breaker opens again, the roaster needs repair.

# Roasting process:
We roast our own coffee in the coffeehouse on a weekly basis. There are two primary things to know about our coffee roasting: the roasting degrees, the height of the coffee trays, and the oven temperatures.

## Roasting Degrees:

Coffee roasting is one of the most influential factors of coffee taste. Roasting transforms green beans into the aromatic and flavorful coffee that wakes our senses in the morning. However, roasting beans at various levels achieves more than merely darkening the beans; it also changes many of the beans’ physical attributes as well.

## Height of Coffee Trays:

Every coffee pile in a tray has a different height measured in mm (millimeters). Obviously, the higher the pile, the more heat an oven would require to achieve the desired roasting degree. The reverse effect happens on lower piles, which would require less oven heat. Therefore, the height of our coffee in the trays is a factor of most importance to the successful accomplishment of our excellent coffee roasting process and thus needs to be considered whenever analyzing the result of a roasting process!

## Oven Temperatures:

In total, our facility possesses 5 ovens, and each oven is equipped with 3 state-of-the-art heat sensors. For our use case, it is obviously essential to analyze the highest and lowest temperatures recorded by the heat sensors. The lowest recordable temperature is 0° and the highest is 1000°. The sensors themselves were handcrafted by our own engineers who not only have years of background in the coffee roasting industry but also wanted to outdo themselves and create a unique temperature sensor specifically for our niche! If any damages or malfunctions are to be experienced, then it is crucial that the upper management is notified without any delays! Insulating the Roasting Chamber is also an option: Some owners add a layer of heat-proof insulation around the exterior of the roasting chamber. This insulation allows the Quest to retain more heat, increasing capacity and the speed of heating. However, the downside is that if the user wishes to dump heat when a roast is getting too hot, it will be slower.

## Roasting Guidelines:

In general, we first distinguish between three roasting degrees: light, medium, and dark. Secondly, we have to acknowledge the coffee pile height in the tray as that plays a big role in the temperature of the roasting ovens which is the third and last constraint that needs to be abided by. Due to logistics, the moisture levels are recorded as metrics but they are not relevant for the violation analysis since there are no feasible measures to change the moisture levels of the coffee beans. Similarly, the amount of time a coffee batch spends inside each of the roasting chambers can not be changed: Each roasting chamber takes 5 minutes. Therefore, moisture levels and timestamps are not really relevant for the final measure analysis.

For better understanding, we describe temperature rules with boundary temperatures t_min and t_max and distinguish between:
-> open brackets, e.g., (t_min, t_max), this means that the boundary temperatures ARE NOT included in the rules.
-> closed brackets, e.g., [t_min, t_max], this means that the boundary temperatures ARE included in the rules.

-> Light Roast:
Goes through roasting ovens 1,2 and 3.
Light roasts are light brown with no oil on the bean surface, with a toasted grain taste and noticeable acidity. A common misconception is that Light Roasts don’t have as much caffeine as their darker, bolder counterparts. However, the truth is precisely the opposite! As beans roast, the caffeine slowly cooks out of the beans. Therefore, because lightly roasted beans cook for a shorter time and at a lower temperature, they retain more caffeine from the original green coffee bean. Other roasters refer to a Light Roast as Light City Roast, New England Roast, or Cinnamon Roast.

We first distinguish between a tray height of less than 180mm and higher or equal to 180mm:

--> Coffee tray height lower than 180mm:
We inherently can not allow the temperature of roasting oven 1 to go below 120° or above 400°. Roasting oven 2 should maintain its temperature as [220°, 500°]. The final product will present a good quality if the highest temperatures of roasting oven 3 remain at 550°.

--> Coffee tray height of at least 180mm:
Roasting oven 1 should follow the temperature rule [140°, 420°]. Afterward, it is not allowed for roasting oven 2 to go above 520° or below 240°. Finally, the product will not pass the quality standard if roasting oven 3 fails to maintain its temperatures below 571°.


-> Medium Roast:
Goes through roasting ovens 1,2,3 and 4.
Medium roasts are medium brown to brown with no oil on the surface, although darker roasts in this group may appear slightly shiny. They are balanced, exhibiting significant flavor and aroma. Medium Roast coffees are brown and have a thicker body than a Light Roast. Unlike Light, Medium starts to take on a bit of the taste from the roasting process, losing some of the bright floral flavors typical of a Light Roast. Instead, they carry a much more balanced flavor with a medium amount of caffeine. A Medium is roasted until just before the second crack.
For a successful medium roast of coffee beans, the following technical requirements should be followed:

--> Coffee tray height of at most 170mm:
Temperatures of roasting 1 should follow [170°,450°].
Temperatures of roasting 2 should follow [270°,550°].
Temperatures of roasting 3 should follow [370°,650°].
Temperatures of roasting 4 should not exceed 550°.

--> Coffee tray height of at least 170mm:
Temperatures of roasting 1 should avoid (0°,180°) and (460°,1000°).
Temperatures of roasting 2 should avoid (0°,290°) and (570°,1000°).
Temperatures of roasting 3 should avoid (0°,390°) and (670°,1000°).
Temperatures of roasting 4 should reach at most 560°.


-> Dark Roast:
Dark roasts are dark brown to almost black, coffee beans roasted until they exude oils and therefore have an oil sheen glowing on the surface. The roasting process’s flavor overwhelms the beans’ flavor, and the coffee from some beans may taste spicy, bitter, or smoky.	To be considered Dark, beans roast to a temperature of anything higher than 440° or essentially to the end of the second crack. If beans roast much hotter than 780°, the coffee will start to taste more and more of charcoal and will not pass the final quality check. This roasting degree is the only one that requires the use of a roasting oven 5. If the coffee pile on the tray reaches 175mm and beyond, then the roasting oven 5 should not have its temperatures exceed 580°. Similarly, for coffee piles smaller than 175mm, roasting oven 5 should not go beyond 560°.
Many other big-batch roasters cut corners by roasting larger quantities faster at extremely high temperatures for a short amount of time but it is vital for us to still respect a new pattern of roasting beginning at oven chamber 1 if the coffee pile is at least 175mm high then roasting oven 1 should not exceed 580° and the lowest temperature allowed would be 220°, similarly for roasting oven 2 the temperatures reach at most 680° and go no lower than 320°. Continuing the process, if roasting oven 3 goes above 780° or if roasting oven 4 exceeds 680°, the final product will be rejected! The same outcome will happen if roasting oven 3 fails to maintain at least 421° or if roasting oven 4 goes lower than 320°.
However, for piles of other heights, roasting oven 1 should remain between 200° and 560° including both temperatures. These piles of other sizes can also accept temperatures of at least 300° and up to 660° for roasting chamber 2, however, if they surpass 760° or if the temperature drops below 400° at roasting oven 3, then the final product will undoubtedly be rejected. Finally, please respect that in order to achieve the first crack in the coffee beans, oven chamber 4 should go as high as 680° but not drop below 320°.


# Additional Information

## Increasing Capacity by painting the drum
Some Quest owners–to increase the maximum batch capacity or alter the roast environment’s thermal dynamics–paint the roasting drum’s exterior with high-heat matte black spray paint. Doing so causes the drum to efficiently absorb and conduct more infrared heat to the roast chamber independent of airflow speed (convection). Increasing the drum’s ability to absorb infrared heat increases the batch capacity, and heat changes are faster, even for large batch sizes (EG. <10 minutes, 300g roasts on an 400° M3).

## Coffee Bean Cooling
The supplied rectangular bean collector placed in the chaff collector cools the beans. This works but has several drawbacks. First, it is slow. Second, there is no air circulation through the roasting chamber with the bean collector inserted into the chaff collector. Use an external cooler instead, such as the optional one from the manufacturer or make one. Make a small box with a muffin fan in it and set the bean collector on top. The flow of ambient air through the beans is much more efficient than the Quests’ inbuilt cooling function.
\"\"\"
"""