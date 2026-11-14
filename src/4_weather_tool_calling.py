
import os
import json
import requests

from openai import OpenAI


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

client = OpenAI()

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


# ---------------------------------------------------------
# 1. Weather Tool
# ---------------------------------------------------------

class WeatherTool:
    """Fetch current weather data using the OpenWeather API."""

    def __init__(self):
        self.url = "https://api.openweathermap.org/data/2.5/weather"
        self.api_key = os.environ["OPENWEATHER_API_KEY"]

    def get_current_weather(self, location: str) -> dict:

        response = requests.get(
            self.url,
            params={
                "q": location,
                "appid": self.api_key,
                "units": "metric"
            },
            timeout=20
        )

        response.raise_for_status()
        data = response.json()

        return {
            "location": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "condition": data["weather"][0]["description"]
        }


# ---------------------------------------------------------
# 2. Initialize Weather Tool
# ---------------------------------------------------------

weather_tool = WeatherTool()


# ---------------------------------------------------------
# 3. Tool Definition
# ---------------------------------------------------------

weather_tool_definition = {
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "Get current weather information for a location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name, such as Mumbai or Pune."
                }
            },
            "required": ["location"],
            "additionalProperties": False
        }
    }
}


# ---------------------------------------------------------
# 4. Common Tool Executor
# ---------------------------------------------------------

def execute_tool(tool_name: str, raw_arguments: str) -> dict:
    """
    Execute the tool requested by the LLM.

    The LLM provides the function name and arguments.
    Python executes the actual function.
    """

    arguments = json.loads(raw_arguments)

    if tool_name == "get_current_weather":

        return weather_tool.get_current_weather(
            location=arguments["location"]
        )

    raise ValueError(f"Unknown tool: {tool_name}")


# ---------------------------------------------------------
# 5. LLM Tool Calling
# ---------------------------------------------------------

def ask_with_weather_tool(question: str):

    messages = [
        {
            "role": "system",
            "content": (
                "Use the weather tool for current weather questions. "
                "For general weather-related conceptual questions, "
                "answer directly without calling the tool. "
                "Do not invent current weather information."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    # First LLM call
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=[weather_tool_definition],
        tool_choice="auto",
        temperature=0
    )

    assistant_message = response.choices[0].message

    # No tool call required
    if not assistant_message.tool_calls:

        return assistant_message.content

    # Process all requested tool calls
    messages.append(
        assistant_message.model_dump(exclude_none=True)
    )

    for tool_call in assistant_message.tool_calls:

        print("\nTool called:", tool_call.function.name)
        print("Raw arguments:", tool_call.function.arguments)

        try:
            # Execute the requested tool
            weather_result = execute_tool(
                tool_name=tool_call.function.name,
                raw_arguments=tool_call.function.arguments
            )

        except Exception as error:

            weather_result = {
                "error": str(error)
            }

        print("Weather result:", weather_result)

        # Add tool execution result to conversation
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(weather_result)
            }
        )

    # Second LLM call
    # LLM uses the tool result to generate a human-readable answer
    final_response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0
    )

    return final_response.choices[0].message.content


# ---------------------------------------------------------
# 6. Main Method
# ---------------------------------------------------------

if __name__ == "__main__":

    # Question 1: Requires weather tool
    answer = ask_with_weather_tool(
        "What is the weather in Mumbai?"
    )

    print("\nWeather Answer:")
    print(answer)

    print("\n================================")

    # Question 2: Does not require weather tool
    answer = ask_with_weather_tool(
        "Why does humidity sometimes make hot weather "
        "feel more uncomfortable?"
    )

    print("\nFinal Answer:")
    print(answer)


# ---------------------------------------------------------
# BASIC CONCEPTS
# ---------------------------------------------------------

# 1. LLM:
#    A Large Language Model understands user questions and
#    generates responses based on the provided context.
#
# 2. Tool Calling / Function Calling:
#    Allows an LLM to request execution of an external function
#    when it needs information or functionality outside its
#    own knowledge.
#
# 3. Tool Definition:
#    Describes the available function to the LLM.
#    It specifies:
#       - Function name
#       - Function description
#       - Required parameters
#       - Parameter types
#
#    The LLM uses this definition to decide when and how
#    to request a tool call.
#
# 4. WeatherTool Class:
#    Contains the actual business logic for fetching weather
#    information using the OpenWeather API.
#
# 5. execute_tool():
#    Acts as a common tool executor.
#    It receives the function name and arguments from the LLM
#    and invokes the corresponding Python function.
#
# 6. Tool Choice:
#    tool_choice="auto" allows the LLM to decide whether
#    a tool call is required.
#
# 7. Assistant Message:
#    When the LLM decides to use a tool, it returns an
#    assistant message containing tool_calls.
#
#    The assistant does not execute the function itself.
#    It only requests the application to execute it.
#
# 8. Tool Response:
#    Python executes the requested function and sends
#    the result back using:
#
#       "role": "tool"
#       "tool_call_id": tool_call.id
#
#    The tool_call_id connects the result to the
#    corresponding tool request.
#
# 9. Second LLM Call:
#    The tool result is added to the conversation.
#    The LLM reads this result and generates a
#    human-readable response.
#
# 10. model_dump():
#     Converts the assistant message object into a
#     dictionary that can be added to the conversation.


# ---------------------------------------------------------
# EXECUTION FLOW
# ---------------------------------------------------------

# User Question
#       |
#       v
# ask_with_weather_tool()
#       |
#       v
# First LLM Call
#       |
#       v
# LLM Analyzes User Question
#       |
#       v
# Is Tool Required?
#       |
#       |-------------------------|
#       |                         |
#      NO                        YES
#       |                         |
#       v                         v
# Return Direct Answer     Assistant Returns Tool Call
#                                 |
#                                 v
#                         execute_tool()
#                                 |
#                                 v
#                         WeatherTool Class
#                                 |
#                                 v
#                         OpenWeather API
#                                 |
#                                 v
#                         Weather JSON Result
#                                 |
#                                 v
#                         Add Tool Result
#                         to Conversation
#                                 |
#                                 v
#                         Second LLM Call
#                                 |
#                                 v
#                         Human-Readable Answer
#                                 |
#                                 v
#                              Return
