from vertexai.preview.generative_models import GenerativeModel
from prompt_utils import COFFEE_ROASTING_PROMPT_1, COFFEE_ROASTING_PROMPT_2


def generate_request_coffee_roasting_prompt_1():
    model = GenerativeModel("gemini-pro-vision")
    responses = model.generate_content(
        contents=COFFEE_ROASTING_PROMPT_1,
        generation_config={
            "max_output_tokens": 2048,  # Currently the max output (15.01.2024)
            "temperature": 0.1,
            "top_p": 1,
            "top_k": 32
        },
        stream=True,
    )

    for response in responses:
        print(response.text, end="")


def generate_request_coffee_roasting_prompt_2():
    model = GenerativeModel("gemini-pro-vision")
    responses = model.generate_content(
        contents=COFFEE_ROASTING_PROMPT_2,
        generation_config={
            "max_output_tokens": 2048,  # Currently the max output (15.01.2024)
            "temperature": 0.1,
            "top_p": 1,
            "top_k": 32
        },
        stream=True,
    )

    for response in responses:
        print(response.text, end="")


# Print result for both prompts with 3 generated answers for each prompt
for p in range(1, 3):
    print(f"--- START OF: COFFEE ROASTING REQUEST PROMPT {p}-----\n")
    for attempt in range(1, 4):
        print(f"----- START OF: PROMPT {p} GENERATION NR. {attempt} -----\n")
        if p == 1:
            generate_request_coffee_roasting_prompt_1()
        else:
            generate_request_coffee_roasting_prompt_2()
        print(f"----- END OF: PROMPT {p} GENERATION NR. {attempt} -----\n")
    print(f"--- END OF: COFFEE ROASTING REQUEST PROMPT {p}-----\n\n")
    print("\n-------- NOW SWITCHING FROM PROMPT 1 TO PROMPT 2 --------\n\n")
