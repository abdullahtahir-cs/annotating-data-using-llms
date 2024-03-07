
"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

# Import the package
import google.generativeai as genai
import csv

# Set up the API key
genai.configure(api_key="YOUR-API-KEY")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

# Set up the safety settings
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

# Create the model
model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Start a chat
convo = model.start_chat(history=[])


# Define the function to annotate tweets
def annotate_tweets(prompt, tweets):
    annotations = []
    # giving prompt to the model
    convo.send_message(f"{tweets}\n\n{prompt}")
    result = convo.last.text
    # cleaning the result and splitting it into annotations
    result = result.split('.')
    for res, tweet in zip(result, tweets):
        result_split = res.split("/")
        if len(result_split) == 3:
            annotations.append((result_split[0].strip(), tweet, prompt, result_split[1].strip(), result_split[2].strip()))
    return annotations


# Define the function to read tweets from a CSV file
def read_tweets_from_csv(csv_file, limit):
    tweets = []
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader, start=1):
            if i > limit:
                break
            tweets.append(row["OriginalTweet"])
    return tweets


# Define the function to write the output to a CSV file
def write_output_to_csv(output_file, annotations):
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["No.", "tweet", "Prompt", "generated annotations", "explanation"])
        for annotation in annotations:
            writer.writerow(annotation)


# Define the main function
def main():
    CSV_FILE = 'Corona_NLP_test.csv'
    OUTPUT_FILE = 'output1.csv'
    # limit to read the tweets from the CSV file
    LIMIT = 20
    
    # Read the tweets from the CSV file
    tweets = read_tweets_from_csv(CSV_FILE, LIMIT)
    
    # Define the prompt1 and labels
    labels = ["Positive", "Extremely positive", "Negative", "Extremely Negative"]
    prompt = f"take this list, this is a list of tweets, I want to do annotation on all tweets one by one, read one tweet, and generate annotations for this tweet from the following labels: {labels}\n i.e. you have to assign any label from these labels to each tweet, by reading that tweet and analyzing it and the most related label you think is, give it to that tweet, you have to give me your answer in the following format:\n\n\"tweet number/label given to the corresponding number tweet/reason why you gave this label to this tweet.\"\n\nsee this few examples to understand the format more:\n\"1/Positive/because this tweet conveys positive message.\"\n\"2/Negative/because negative language is used in tweet.\"\nabove is only the examples to show you format, you have to give me your result in this format"
    annotations = annotate_tweets(prompt, tweets)
    write_output_to_csv(OUTPUT_FILE, annotations)

    # Define the prompt2 and labels
    OUTPUT_FILE = 'output2.csv'
    prompt = f"Please analyze the sentiment of the above tweets and annotate it using the following labels: {labels}\n i.e. you have to assign any label from these labels to each tweet, by reading that tweet and analyzing it and the most related label you think is, give it to that tweet, you have to give me your answer in the following format:\n\n\"tweet number/label given to the corresponding number tweet/reason why you gave this label to this tweet.\"\n\nsee this few examples to understand the format more:\n\"1/Positive/because this tweet conveys positive message.\"\n\"2/Negative/because negative language is used in tweet.\"\nabove is only the examples to show you format, you have to give me your result in this format"
    annotations = annotate_tweets(prompt, tweets)
    write_output_to_csv(OUTPUT_FILE, annotations)

    # Define the prompt3 and labels
    OUTPUT_FILE = 'output3.csv'
    prompt = f"Determine the sentiment expressed in the above tweets and select the appropriate label and annotate them from the following labels: {labels}\n i.e. you have to assign any label from these labels to each tweet, by reading that tweet and analyzing it and the most related label you think is, give it to that tweet, you have to give me your answer in the following format:\n\n\"tweet number/label given to the corresponding number tweet/reason why you gave this label to this tweet.\"\n\nsee this few examples to understand the format more:\n\"1/Positive/because this tweet conveys positive message.\"\n\"2/Negative/because negative language is used in tweet.\"\nabove is only the examples to show you format, you have to give me your result in this format"
    annotations = annotate_tweets(prompt, tweets)
    write_output_to_csv(OUTPUT_FILE, annotations)

    print(f"Annotations generated and written to {OUTPUT_FILE}.csv")

# Call the main function
if __name__ == "__main__":
    main()
