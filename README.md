## Setup
- use python ```3.8.9```
- create virtual environment using command ```python -m venv venv```
- activate virtual environment using command ```source venv/bin/activate```
- install requirements using command ```pip install -r requirements.txt```
- run ```python main.py```

## Usage
- open swagger ui at http://127.0.0.1:8000/docs
- call ```/answer``` api which accepts two files
- files container questions and reference document to search for answer
- example questions.json and reference.json
    ```
    {
    "questions": [
        "What are your SLAs for notification?",
        "Which cloud providers do you rely on?"
        ]
    }
    ```

    ```
    [
        {
            "content": "What are your SLAs for notification?",
            "answer": "We have a SLA for notifications. Please review our SLAs for more information.",
            "comment": "We have a SLA for notifications. Please review our SLAs for more information."
        },
        {
            "content": "What are your SLAs for notification?",
            "answer": "We have a SLA for notifications. Please review our SLAs for more information.",
            "comment": "We have a SLA for notifications. Please review our SLAs for more information."
        }
    ]
    ```