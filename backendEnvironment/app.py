import json
from flask import Flask,request, jsonify, render_template
import requests
from flask_cors import CORS, cross_origin

app=Flask(__name__)
CORS(app)
#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
# Your OpenAI API key
api_key = ''

# Define the API endpoint
GPT3_API_URL = "https://api.openai.com/v1/chat/completions"

#your weather API KEY
api_key_ = "666f26f95d23869dd90abb5efde8efce"

messages = [
        {"role": "system", "content": "You are a helpful assistant."}
]

@app.route("/route_with_cors", methods=["GET"])
@cross_origin()  # Apply CORS to this route
def route_with_cors():
    data = {"message": "CORS is enabled for this route"}
    return jsonify(data)

@app.route("/")
def welcome():
    # print(run_conversation())
    return "welcome"


@app.route("/getWeather",methods=['POST'])
def getData():
    try:
        global messages
        user_input=request.get_json()
        mess=user_input['userMessage']
        messages.append({"role": "user", "content": mess})
        return jsonify(run_conversation())
    except:
        return jsonify({"assistant_reply":"Please provide the valid input"})

#getting the weather response from the weather api
def get_current_weather(location):
    url=f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key_}&units=metric"
    response = requests.get(url)
    data = response.json()
    print(data)
    if data["cod"] == 200:
        return {
            "assistant_reply":f"The Current Weather of {data["name"]} is temperature {data["main"]["temp"]} degree celsius and climate is {data["weather"][0]["main"]}"
        }
    else:
        return {
            "error": "Weather information not available for this location."
        }
def generate_text(text):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
                "messages": messages,
                "model": "gpt-3.5-turbo"
        }
        response = requests.post(GPT3_API_URL, headers=headers, data=json.dumps(payload))
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            assistant_reply = data["choices"][0]["message"]["content"]
            return {"assistant_reply": assistant_reply}
        else:
            print("Error:", response.status_code, response.text)
            return jsonify({"error": "An error occurred"})


def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
        {
            "name":"generate_text",
            "description":"Get the result of the given query",
            "parameters":{
                "type":"object",
                "properties":{
                    "text":{
                        "type":"string",
                        "description":"The query user wants result for , e.g. is delhi suitable for me, what is recursion,hii,tell me about something"
                    },
                },
                "required":["text"]
            },

        },
    ]

    data = {
        "model": "gpt-3.5-turbo-0613",
        "messages": messages,
        "functions": functions,
    }

    response = requests.post(GPT3_API_URL, headers=headers, json=data)
    data1 = response.json()
    response_message = data1["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        print("here")
        available_functions = {
            "get_current_weather": get_current_weather,
            "generate_text":generate_text,
        }
        function_name = response_message["function_call"]["name"]
        print(function_name)
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        print(function_args)
        function_response={}
        if(function_name=="get_current_weather"):
            function_response = function_to_call(location=function_args.get("location"))
            print(function_response)
            messages.append(response_message)  # extend conversation with assistant's reply
            messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response['assistant_reply']
                }
            )
        else:
            function_response = function_to_call(text=function_args.get("text"))
            # Step 4: send the info on the function call and function response to GPT
            messages.append(response_message)  # extend conversation with assistant's reply
            messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response['assistant_reply']
                }
            )  # extend conversation with function response

    data["messages"] = messages
    return function_response
        # second_response = requests.post(GPT3_API_URL, headers=headers, json=data)
        # return second_response.json()
