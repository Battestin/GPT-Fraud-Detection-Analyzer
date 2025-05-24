from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

model = "gpt-4" # gpt-3.5-turbo don't work, it doesn't identify the fraud

def load_file(filename):
    try:
        with open(filename, "r") as file:
            data = file.read()
            return data
    except IOError as e:
        print(f"Error loading file: {e}")

def save_file(filename, content):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
    except IOError as e:
        print(f"Error saving file: {e}")

def transaction_analyzer(transactions_list):
    print("1. Starting transaction analysis")

    system_prompt = """
        Analyze the following financial transactions and identify whether each one is a "Possible Fraud" or should be "Approved".
        Add a "Status" attribute with one of the values: "Possible Fraud" or "Approved".

        Each new transaction must be inserted into the JSON list.

        # Possible indications of fraud
        - Transactions with very discrepant amounts
        - Transactions that occur in very distant locations

        Use the output format below for your response.

        # Output Format
        {
            "transactions": [
                {
                    "id": "id",
                    "type": "credit or debit",
                    "merchant": "merchant name",
                    "time": "transaction time",
                    "amount": "R$XX,XX",
                    "product_name": "product name",
                    "location": "city - state (Country)",
                    "status": ""
                },
            ]
        }
    """

    messages_list = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"Consider the CSV below, where each line is a different transaction: {transactions_list}. Your response must adopt the #Output Format (just a JSON, no other comments)."
        }
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages_list,
        temperature=0
    )

    content = response.choices[0].message.content.replace("'", '"')
    print("\Content:", content)
    json_result = json.loads(content)
    #print("\nJSON:", json_result)
    return json_result

def generate_opinion(transaction):
    print("2. Generating opinion for transaction", transaction["id"])
    system_prompt = f"""
    For the following transaction, provide an opinion only if its status is "Possible Fraud". In your opinion, include a justification for why you identified it as fraud.
    Transaction: {transaction}

    ## Response Format
    "id": "id",
    "type": "credit or debit",
    "merchant": "merchant name",
    "time": "transaction time",
    "amount": "R$XX,XX",
    "product_name": "product name",
    "location": "city - state (Country)",
    "status": "",
    "opinion": "Put Not Applicable if the status is Approved"
    """

    messages_list = [
        {"role": "user", "content": system_prompt}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages_list
    )

    content = response.choices[0].message.content
    print("\nOpinion:")
    return content

def generate_recomendation(opinion):
    print("3. Generating recommendations")

    system_prompt = f"""
    For the following transaction, provide an appropriate recommendation based on the status and details of the transaction: {opinion}

    Recommendations can be "Notify Customer", "Trigger Anti-Fraud Department", or "Perform Manual Verification".
    They should be written in a technical format.

    Also include a classification of the type of fraud, if applicable.
    Generate the response formated for a txt file.
    """

    messages_list = [
        {"role": "system", "content": system_prompt}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages_list
    )

    content = response.choices[0].message.content
    print("\nRecommendation:")
    return content


transactions_list = load_file("Alura\GPT Python criando ferramentas com API\GPT - Transaction Analizer\\data\\transactions.csv")
analized_transactions = transaction_analyzer(transactions_list)

for transaction in analized_transactions["transactions"]:
    if transaction["status"] == "Possible Fraud":
        opinion = generate_opinion(transaction)
        recomendation = generate_recomendation(opinion)
        transaction_id = transaction["id"]
        trasaction_product = transaction["product_name"]
        transaction_status = transaction["status"]
        save_file(f"Alura\GPT Python criando ferramentas com API\GPT - Transaction Analizer\\data\\recomendation-{transaction_id}-{trasaction_product}-{transaction_status}.txt", recomendation)

