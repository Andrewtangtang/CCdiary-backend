# CC Diary Backend Documentation
[![CC Diary Intro](https://raw.githubusercontent.com/SimonLiu423/cc_diary/ec4694b2518ead544a0f982be761f6c4276f51dd/presentation/ccDiary_intro.gif)](https://github.com/SimonLiu423/cc_diary/blob/61104e21db6f5a4cf7f9cfe8a971b073cdf62ecd/presentation/ccDiary.pdf)
*Click on the GIF to view our full presentation PDF*
## Introduction
The CC Diary backend provides the essential APIs to support the functionalities of the CC Diary app. It enables diary management, sentiment analysis, and chatbot responses, facilitating a seamless user experience focused on mental health and emotional well-being.

## Prerequisites
Ensure that the following tools are installed before running the backend:

- Python 3.12
- Flask
- Other required Python libraries (as listed in `requirements.txt`)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Andrewtangtang/CCdiary-backend
    cd CCdiary-backend
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set the environment variable to avoid library conflicts:
    ```bash
    export KMP_DUPLICATE_LIB_OK=True
    ```

## Running the Application

Start the Flask server by running:
```bash
python app.py
```
The server will be accessible at http://0.0.0.0:5000/.

## API Endpoints


1. ### `/feedback` [POST]

**Description:** Processes a diary entry and provides mental health feedback.

**Request:**

- JSON object with the following fields:
   - `diary_description`: The text content of the diary entry.
   - `language`: The language of the entry (e.g., `zh_Hant_TW` for Traditional Chinese).

**Response:**

- JSON object containing:
   - `feedback`: AI-generated feedback based on the diary entry.

**Example Request:**
```json
{
  "diary_description": "Today I felt very stressed.",
  "language": "English"
}
```
**Example Response:**
```json
{
  "feedback": "It's important to acknowledge your stress. Consider practicing relaxation techniques such as deep breathing or mindfulness. If the stress persists, seeking support from a mental health professional might be beneficial."
}
```

2. ### `/query` [POST]

**Description:** Handles health-related questions and provides responses through the chatbot.

**Request:**

- JSON object with the following fields:
   - `question`: The user's health-related query.
   - `language`: The language of the query (e.g., `zh_Hant_TW` for Traditional Chinese).

**Response:**

- JSON object containing:
   - `answer`: AI-generated answer to the question.

**Example Request:**
```json
{
  "question": "What are the symptoms of depression?",
  "language": "English"
}
```

**Example Response:**
```json
{
  "answer": "Common symptoms of depression include persistent sadness, loss of interest in activities, changes in appetite or sleep patterns, and feelings of worthlessness or guilt."
}
```

3. ### `/record` [GET]

**Description:** Retrieves all diary records in JSON format.

**Response:**

- JSON array containing all diary records.

**Example Response:**
```json
[
  {
    "id": 1,
    "diary_description": "Today I felt very stressed.",
    "language": "English",
    "timestamp": "2024-08-27T10:00:00Z"
  },
  {
    "id": 2,
    "diary_description": "Had a great day at work.",
    "language": "English",
    "timestamp": "2024-08-26T15:30:00Z"
  }
]
```

## Technologies Used

- OpenAI: Powers the AI-based mental health feedback.
- LangChain: Facilitates customization of language model pipelines.
- Hugging Face: Provides models for sentiment analysis.
- Pytorch: Used for analyzing and generating feedback based on user diary entries.
- Flutter: Utilized for building the frontend of the app.[frontend](https://github.com/SimonLiu423/cc_diary)

## License

Copyright (c) 2024 vaclis. All rights reserved.

This software and associated documentation files (the "Software") are the exclusive property of vaclis. The Software is protected by copyright laws and international copyright treaties, as well as other intellectual property laws and treaties.

Unauthorized copying, modification, distribution, or use of this Software, via any medium, is strictly prohibited without the express written permission of vaclis.

For licensing inquiries, please contact: vacliscofounders@gmail.com

## Contact

Feel free to mail to us by vacliscofounders@gmail.com for collaboration or bugs report!

- [@vaclisinc](https://www.github.com/vaclisinc)
- [@SimonLiu423](https://www.github.com/SimonLiu423)
- [@WavJaby](https://www.github.com/WavJaby)
- [@Andrewtangtang](https://www.github.com/Andrewtangtang) 

---


Developed with ❤️ by 游松澤 (Yu Song-Ze), 張羿軒 (Zhang Yi-Xuan), 劉力瑋 (Liu Li-Wei), 張昀棠 (Zhang Yun-Tang)

Project Team: 不嘻嘻的時候，黑客松松澤



