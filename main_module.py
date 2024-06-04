import argparse
import traceback
import json
import ollama
import inquirer
from datetime import datetime

# python main_module.py "bruh" --models llama3 mistral

# Local import
import log
from cli_color import Color


def ask_all_models(ollama_client, models: list, message: str):
    for model in models:
        print("")
        print(f"Using model {model}")
        stream = ollama_client.chat(
            model=model,
            messages=[{"role": "user", "content": message}],
            stream=True,
        )

        for chunk in stream:
            print(chunk["message"]["content"], end="", flush=True)


def return_models(ollama_client):

    models = []
    for model in ollama_client.list()["models"]:
        models.append(model["name"])

    questions = [
        inquirer.Checkbox(
            "models",
            message="What models do you want to use?",
            choices=models,
        ),
    ]
    response = inquirer.prompt(questions)

    return response

if __name__ == "__main__":

    try:
        parser = argparse.ArgumentParser(
            description="This is the description for the main parser!"
        )
        parser.add_argument(
            "host",
            type=str,
            help="The URL of the Ollama host.",
        )
        parser.add_argument(
            "--system-prompt",
            nargs="?",
            help="Optional. The path to the file that has the system prompt you want to use.",
        )        
        # Add arguement that takes in a list of models
        parser.add_argument(
            "--models",
            nargs="+",
            help="Optional. List of models to use.",
        )
        parser.add_argument(
            "--debug",
            action="store_true",
            help="Optional. Use this argument if you are debugging any errors.",
        )

        args = parser.parse_args()

        logger = log.get_logger(
            logger_name=__file__ + " Logger",
            log_file_name=__file__ + ".log",
            debug=args.debug,
        )

        logger.debug(args)

        ollama_client = ollama.Client(host=args.host)

        # if args.models:
        #    ask_all_models(ollama_client, args.models, args.message)

        # If the user doesn't provide any models, we'll just prompt them to select from the list of models
        if not args.models:
            args.models = return_models(ollama_client)["models"]

        # Since we're using multiple models here, we need to set up a list of "messages" for each model so that we can provide it to Ollama
        messages = {}
        for model in args.models:
            messages[model] = []
        while True:
            if content_in := input("chat >>> "):

                # Append this new input to the list of messages for each model
                for model in args.models:
                    messages[model].append({"role": "user", "content": content_in})

            message = {"role": "assistant", "content": ""}
            
            # Check if the user provided a file, which should contain the system prompt
            if args.system_prompt:
                with open(args.system_prompt, "r") as f:
                    message["system"] = f.read()
            
            # Iterate through each model that the user provided
            for model in args.models:
                print(Color.blue(f"------ Using model {model} ------"))
                
                # For each model, we'll iterate through the list of messages that we've built up
                for response in ollama_client.chat(
                    model=model, messages=messages[model], stream=True
                ):
                    # Check to see if we get 'done' back, so we just append the message to the growing list
                    # so we can keep track of what we said previously
                    if response["done"]:
                        messages[model].append(message)
                        with open(f"output/chat_{model}.txt", "a+") as f:
                            json.dump(
                                {
                                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "question": content_in,
                                    "response": message["content"]
                                },
                                f,
                                indent=4,
                            )
                    # Get the content from the response
                    content = response["message"]["content"]
                    print(content, end="", flush=True)
                    message["content"] += content
                print()

            print()

    except Exception:
        logger.error("Unhandled Exception!")
        logger.error(traceback.format_exc())
