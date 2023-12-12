import streamlit as st
import time

def main():
    st.title("Classroom Scoreboard")

    # Create an empty slot for our dynamic content
    placeholder = st.empty()

    # Assuming you have a function called get_scores() that fetches the latest scores
    while True:
        current_scores = get_scores()
        placeholder.text(current_scores)
        time.sleep(2)  # updates every 2 seconds

def get_scores():
    # Replace this with your actual score fetching code
    # For this example, it just returns a random number as the score
    import random
    return f"Score: {random.randint(0, 100)}"

if __name__ == "__main__":
    main()
