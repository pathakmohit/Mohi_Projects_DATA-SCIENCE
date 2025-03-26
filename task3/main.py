try:
    import streamlit as st
    import pandas as pd
    from collections import Counter
except ModuleNotFoundError:
    print("Error: Required modules not found. Please install them using 'pip install streamlit pandas'")
    exit()

# Initialize session state for analytics
if 'queries' not in st.session_state:
    st.session_state.queries = []
if 'topics' not in st.session_state:
    st.session_state.topics = []
if 'ratings' not in st.session_state:
    st.session_state.ratings = []

st.title("Chatbot Analytics Dashboard")

# User Input Simulation
query = st.text_input("Ask the chatbot:")
topic = st.text_input("Enter topic related to the query:")
rating = st.slider("Rate your satisfaction (1-5):", 1, 5, 3)

if st.button("Submit Query"):
    if query and topic:
        st.session_state.queries.append(query)
        st.session_state.topics.append(topic)
        st.session_state.ratings.append(rating)
        st.success("Query submitted successfully!")

# Display Analytics
st.subheader("Analytics")

# Number of queries
st.write(f"Total Queries: {len(st.session_state.queries)}")

# Most common topics
if st.session_state.topics:
    topic_counts = Counter(st.session_state.topics)
    most_common_topics = pd.DataFrame(topic_counts.most_common(5), columns=["Topic", "Count"])
    st.write("Most Common Topics:")
    st.dataframe(most_common_topics)

# Average Satisfaction Rating
if st.session_state.ratings:
    avg_rating = sum(st.session_state.ratings) / len(st.session_state.ratings)
    st.write(f"Average Satisfaction Rating: {avg_rating:.2f}/5")
