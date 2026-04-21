import streamlit as st
import random

st.set_page_config(page_title="Advanced Number Guessing Game", page_icon="🎯")

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
    penalty = 8
elif difficulty == "Medium (1–100)":
    max_range = 100
    max_attempts = 10
    penalty = 10
else:
    max_range = 200
    max_attempts = 8
    penalty = 15


# ---------------------------
# Initialize session state
# ---------------------------
def init_game():
    st.session_state.number = random.randint(1, max_range)
    st.session_state.attempts = 0
    st.session_state.score = 100
    st.session_state.guesses = []
    st.session_state.game_over = False
    st.session_state.low = 1
    st.session_state.high = max_range
    st.session_state.range = max_range


if "number" not in st.session_state or st.session_state.get("range") != max_range:
    init_game()

if "high_score" not in st.session_state:
    st.session_state.high_score = 0


# ---------------------------
# UI Info
# ---------------------------
st.write(f"Guess a number between **1 and {max_range}**")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🎯 Score", st.session_state.score)
with col2:
    st.metric("🔢 Attempts", st.session_state.attempts)
with col3:
    remaining = max_attempts - st.session_state.attempts
    st.metric("⏳ Left", remaining)

st.progress(st.session_state.attempts / max_attempts)


# ---------------------------
# Input
# ---------------------------
guess = st.number_input(
    "Enter your guess:",
    min_value=1,
    max_value=max_range,
    step=1
)


# ---------------------------
# Game Logic
# ---------------------------
if st.button("Submit Guess") and not st.session_state.game_over:

    guess = int(guess)
    st.session_state.attempts += 1
    st.session_state.guesses.append(guess)
    st.session_state.score -= penalty

    # Feedback: Too low / high
    if guess < st.session_state.number:
        st.session_state.low = max(st.session_state.low, guess)
        st.warning("📉 Too Low!")
    elif guess > st.session_state.number:
        st.session_state.high = min(st.session_state.high, guess)
        st.warning("📈 Too High!")
    else:
        st.success(
            f"🎉 Correct! You guessed it in {st.session_state.attempts} attempts.\n"
            f"Final Score: {st.session_state.score}"
        )
        st.session_state.game_over = True

        # Update high score
        if st.session_state.score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.score

    # Hot / Cold feedback
    if len(st.session_state.guesses) > 1 and not st.session_state.game_over:
        prev_diff = abs(st.session_state.guesses[-2] - st.session_state.number)
        curr_diff = abs(guess - st.session_state.number)

        if curr_diff < prev_diff:
            st.success("🔥 Getting warmer!")
        else:
            st.info("❄️ Getting colder!")

    # Hint range
    if not st.session_state.game_over:
        st.info(f"Hint: Number is between {st.session_state.low} and {st.session_state.high}")

    # Game over condition
    if st.session_state.attempts >= max_attempts and not st.session_state.game_over:
        st.error(f"❌ Game Over! The number was {st.session_state.number}")
        st.session_state.game_over = True


# ---------------------------
# Previous guesses
# ---------------------------
if st.session_state.guesses:
    st.write("🧾 Previous guesses:", st.session_state.guesses)


# ---------------------------
# High Score
# ---------------------------
st.write(f"🏆 High Score: {st.session_state.high_score}")


# ---------------------------
# Restart / Play Again
# ---------------------------
def reset_game():
    init_game()

if st.session_state.game_over:
    if st.button("▶️ Play Again"):
        reset_game()
        st.rerun()

if st.button("🔄 Restart Game"):
    reset_game()
    st.rerun()
