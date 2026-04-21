import streamlit as st
import random

st.title("🎯 Advanced Number Guessing Game")

# ---------------------------
# Difficulty settings
# ---------------------------
difficulty = st.selectbox(
    "Select Difficulty",
    ["Easy (1–50)", "Medium (1–100)", "Hard (1–200)"]
)

if difficulty == "Easy (1–50)":
    max_range = 50
    max_attempts = 10
elif difficulty == "Medium (1–100)":
    max_range = 100
    max_attempts = 10
else:
    max_range = 200
    max_attempts = 8

# ---------------------------
# Initialize session state
# ---------------------------
if "number" not in st.session_state or st.session_state.get("range") != max_range:
    st.session_state.number = random.randint(1, max_range)
    st.session_state.attempts = 0
    st.session_state.score = 100
    st.session_state.guesses = []
    st.session_state.game_over = False
    st.session_state.range = max_range

st.write(f"Guess a number between 1 and {max_range}")
st.write(f"Attempts allowed: {max_attempts}")

# ---------------------------
# User input
# ---------------------------
guess = st.number_input(
    "Enter your guess:",
    min_value=1,
    max_value=max_range,
    step=1
)

# ---------------------------
# Game logic
# ---------------------------
if st.button("Submit Guess") and not st.session_state.game_over:

    st.session_state.attempts += 1
    st.session_state.guesses.append(int(guess))

    # Score reduction
    st.session_state.score -= 10

    if guess < st.session_state.number:
        st.warning("📉 Too Low!")

        # range hint
        st.info(f"Hint: Number is between {guess} and {max_range}")

    elif guess > st.session_state.number:
        st.warning("📈 Too High!")

        # range hint
        st.info(f"Hint: Number is between 1 and {guess}")

    else:
        st.success(
            f"🎉 Correct! You guessed it in {st.session_state.attempts} attempts. "
            f"Score: {st.session_state.score}"
        )
        st.session_state.game_over = True

    # Attempts check
    if st.session_state.attempts >= max_attempts and not st.session_state.game_over:
        st.error(f"❌ Game Over! The number was {st.session_state.number}")
        st.session_state.game_over = True

# ---------------------------
# Show previous guesses
# ---------------------------
if st.session_state.guesses:
    st.write("🧾 Previous guesses:", st.session_state.guesses)

# ---------------------------
# Restart game
# ---------------------------
if st.button("🔄 Restart Game"):
    st.session_state.clear()
    st.rerun()