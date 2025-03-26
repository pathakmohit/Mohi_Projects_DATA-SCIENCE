# Task 3 - Chatbot Analytics Dashboard

This project is a **Chatbot Analytics Dashboard** built to track and analyze user interactions with a chatbot. It provides insights into query frequency, popular topics, and user satisfaction ratings using a **Streamlit-based interface**.

## Features
- **Query Tracking**: Logs user queries for analysis
- **Topic Analysis**: Identifies the most common topics using frequency counts
- **Satisfaction Rating**: Captures and averages user satisfaction scores (1-5)
- **Interactive Dashboard**: Displays analytics in real-time via Streamlit

## Project Structure
```
├── app.py            # Main Streamlit application
├── requirements.txt  # Project dependencies
├── README.md         # Documentation
```

## Installation
Ensure Python (>=3.7) is installed. Install dependencies using:
```sh
pip install -r requirements.txt
```

## Running the Application
### Start Streamlit App:
```sh
streamlit run app.py
```

## Data Source
The dashboard collects data dynamically from user inputs. No external dataset is required, but analytics are stored in memory during the session.

## Usage
1. Enter a **query** in the text input field.
2. Provide a **topic** related to the query.
3. Rate your satisfaction (1-5) using the slider.
4. Click **Submit Query** to log the data.
5. View real-time analytics under the "Analytics" section.

## Future Enhancements
- Persist data to a database for long-term analysis
- Add visualizations (e.g., bar charts) for topic counts and ratings
- Include time-based analytics (e.g., queries per day)
