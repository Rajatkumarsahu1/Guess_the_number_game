import streamlit as st
import random
import pandas as pd
import math

st.set_page_config(page_title="Advanced Number Guessing Game", page_icon="🎯")

st.title("🎯 Advanced Number Guessing Game")

# ---------------------------
# Difficulty Settings
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
    max_attempts = 5
    penalty = 10
else:
    max_range = 200
    max_attempts = 3   # keeping your requirement
    penalty = 15


# ---------------------------
# Initialize Game
# ---------------------------
def init_game():
    st.session_state.number = random.randint(1, max_range)
    st.session_state.attempts = 0
    st.session_state.score = 100
    st.session_state.guesses = []
    st.session_state.game_over = False
    st.session_state.low = 1
    st.session_state.high = max_range


# Reset on difficulty change
if "difficulty" not in st.session_state or st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    init_game()

# High score per difficulty
score_key = f"high_score_{difficulty}"
if score_key not in st.session_state:
    st.session_state[score_key] = 0


# ---------------------------
# Input FIRST (important fix)
# ---------------------------
guess = st.number_input(
    "Enter your guess:",
    min_value=1,
    max_value=max_range,
    step=1,
    disabled=st.session_state.game_over
)

submit = st.button("Submit Guess", disabled=st.session_state.game_over)


# ---------------------------
# Game Logic (runs BEFORE UI)
# ---------------------------
if submit and not st.session_state.game_over:

    guess = int(guess)

    if guess in st.session_state.guesses:
        st.warning("⚠️ Already guessed!")
    else:
        st.session_state.attempts += 1
        st.session_state.guesses.append(guess)

        if guess < st.session_state.number:
            st.session_state.score = max(0, st.session_state.score - penalty)
            st.session_state.low = max(st.session_state.low, guess + 1)
            st.warning("📉 Too Low!")

        elif guess > st.session_state.number:
            st.session_state.score = max(0, st.session_state.score - penalty)
            st.session_state.high = min(st.session_state.high, guess - 1)
            st.warning("📈 Too High!")

        else:
            st.success(
                f"🎉 Correct! You guessed it in {st.session_state.attempts} attempts.\n"
                f"Final Score: {st.session_state.score}"
            )
            st.balloons()
            st.session_state.game_over = True

            if st.session_state.score > st.session_state[score_key]:
                st.session_state[score_key] = st.session_state.score

        # Warmer / Colder
        if len(st.session_state.guesses) > 1 and not st.session_state.game_over:
            prev = st.session_state.guesses[-2]
            prev_diff = abs(prev - st.session_state.number)
            curr_diff = abs(guess - st.session_state.number)

            if curr_diff < prev_diff:
                st.success("🔥 Getting warmer!")
            elif curr_diff > prev_diff:
                st.info("❄️ Getting colder!")
            else:
                st.warning("😐 Same distance!")

        # Game Over check (FIXED timing)
        if st.session_state.attempts >= max_attempts and not st.session_state.game_over:
            st.error(f"❌ Game Over! The number was {st.session_state.number}")
            st.session_state.game_over = True


# ---------------------------
# Header UI (AFTER logic)
# ---------------------------
st.caption(f"🎚️ Difficulty: {difficulty}")
st.write(f"Guess a number between **1 and {max_range}**")

remaining = max(0, max_attempts - st.session_state.attempts)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🎯 Score", st.session_state.score)

with col2:
    st.metric("🔢 Attempts", st.session_state.attempts)

with col3:
    if st.session_state.game_over:
        st.metric("🎮 Status", "Game Over")
    else:
        st.metric("⏳ Left", remaining)

st.progress(min(st.session_state.attempts / max_attempts, 1.0))


# ---------------------------
# Hint
# ---------------------------
if not st.session_state.game_over:
    st.info(f"💡 Try between **{st.session_state.low} and {st.session_state.high}**")


# ---------------------------
# Last Guess
# ---------------------------
if st.session_state.guesses:
    st.write(f"🎯 Last Guess: **{st.session_state.guesses[-1]}**")


# ---------------------------
# History
# ---------------------------
if st.session_state.guesses:
    df = pd.DataFrame({
        "Attempt": list(range(1, len(st.session_state.guesses) + 1)),
        "Guess": st.session_state.guesses
    })
    st.dataframe(df, use_container_width=True)


# ---------------------------
# High Score
# ---------------------------
st.write(f"🏆 High Score ({difficulty}): {st.session_state[score_key]}")


# ---------------------------
# Restart
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


# ---------------------------
# Footer
# ---------------------------
st.markdown("---")
st.caption("Made by rajatks1997@gmail.com | LinkedIn: https://www.linkedin.com/in/rajat-kumar-sahu1/")
