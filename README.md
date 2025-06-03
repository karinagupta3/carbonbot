# CarbonBot - Carbon Reform RAG Assistant

This repository contains a Streamlit application that uses the Miriel RAG (Retrieval-Augmented Generation) API to create an AI assistant for Carbon Reform employees. The assistant can answer questions about Carbon Reform using information from uploaded documents.

## Features

- Interactive chat interface built with Streamlit
- Integration with Miriel RAG API for document retrieval and question answering
- Custom prompt engineering to ensure relevant and specific responses
- Display of document sources used to generate answers
- Debug mode to view full API responses

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the root directory with the following variables:

```
MIRIEL_API_KEY=your_api_key_here
MIRIEL_PROJECT_ID=your_project_id_here
```

You can get your API key and project ID by signing up for an account on the [Miriel website](https://miriel.ai).

## Usage

Run the Streamlit app with:

```bash
streamlit run app.py
```

The app will be available at http://localhost:8501 in your web browser.

## Miriel Python Client

This repository also includes the official Python client library for interacting with the Miriel API. You can use this client in your own projects:

```python
from miriel import Miriel

# Initialize the client with your API key
miriel_client = Miriel(api_key="your_api_key")

#add data
miriel_client.learn("The Founders of Miriel are David Garcia, Josh Paulson, and Andrew Barkett")

#Query the documents
query_response = miriel_client.query("Who are the founders of Miriel?")
print(f"Query response: {query_response}")

```

## Calling search with an image

```python
    ...
    query_response = miriel_client.query("What does this image show?", input_images="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg")
    print(f"Query response: {query_response}")
```

## Calling with a structured output

```python
    ...

    #define a schema for the structured output
    output_schema = {
        "founders" : ["string"],
        "number_of_founders": "integer"
    }
    query_response = miriel_client.query("Who are the founders of Miriel?", response_format=output_schema)
    print(f"Query response: {query_response}")
```
Only "integer", "float", "string", "boolean", "array" (list), and "object" (dict) are supported.  Default values not yet supported.

## Documentation
For more details on the API, see the [API Documentation](API.md).
