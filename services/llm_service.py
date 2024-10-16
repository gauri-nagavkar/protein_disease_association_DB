from openai import OpenAI
from backend.utils.config import OPENAI_API_KEY
import json
client = OpenAI(api_key=OPENAI_API_KEY)


# Set up OpenAI API key

def analyze_paper(text):
    """
    Analyze the given text using OpenAI's GPT-4 model to extract 
    multiple protein-disease associations, each with its own association type.
    """
    try:
        # Call OpenAI API using the ChatCompletion endpoint
        response = client.chat.completions.create(
            model="gpt-4",  # Use GPT-4 model
            messages=[
                {"role": "system", "content": "You are an expert in bioinformatics and are great at reading the abstracts of research papers and figuring out cause-result relationships and associations."},
                {"role": "user", "content": f"Extract the following details from the given text and return the output as a JSON array of objects, where each object contains protein, disease, and association. Example format: [{'{'}'protein': '...', 'disease': '...', 'association': 'Positive'{'}'}, {'{'}'protein': '...', 'disease': '...', 'association': 'Negative'{'}'}]. If there are multiple proteins and/or diseases, return one protein-disease pair per association. Text: {text}"}
            ],
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7
        )

        # Extract the response text
        result_string = response.choices[0].message.content.strip()

        # Print the raw response for debugging purposes
        print("OpenAI Response:", result_string)

        # Parse the result as JSON (since we expect a JSON array of objects)
        data = json.loads(result_string)

        return data

    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return None
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return None
