import numpy as np
import streamlit as st
import random
class TicTacToeGame():
    def __init__(self):
        self.state = '         ' 
        self.player = 'X'
        self.winner = None
    

    def allowed_moves(self):      #find the empty position in the state string 
        states = []               #store all possible next states
        for i in range(len(self.state)):
            if self.state[i] == ' ':
                states.append(self.state[:i] + self.player + self.state[i+1:]) 
        return states

    def make_move(self, next_state):
        if self.winner:
            raise(Exception("Game already completed, cannot make another move!"))
        if not self.valid_move(next_state):
            return False
            

        self.state = next_state
        self.winner = self.predict_winner(self.state)
        if self.winner:
            self.player = None
        elif self.player == 'X':
            self.player = 'O'
        else:
            self.player = 'X'
        return True

    def playable(self):
        return ( (not self.winner) and any(self.allowed_moves()) )

    def predict_winner(self, state):
        lines = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]  # all possible lines
        winner = None
        for line in lines:
            line_state = state[line[0]] + state[line[1]] + state[line[2]]
            if line_state == 'XXX':
                winner = 'X'
            elif line_state == 'OOO':
                winner = 'O'
        return winner

    def valid_move(self, next_state):
        allowed_moves = self.allowed_moves()  #get all possible next states
        if any(state == next_state for state in allowed_moves): #check if the input next_state is in 
            return True
        return False

    def print_board(self):
        s = self.state
        print('     {} | {} | {} '.format(s[0],s[1],s[2]))
        print('    -----------')
        print('     {} | {} | {} '.format(s[3],s[4],s[5]))
        print('    -----------')
        print('     {} | {} | {} '.format(s[6],s[7],s[8]))
    def ai_move(self):
        state = self.state
        if self.player != 'O':
            return False

        possible_states = self.allowed_moves()
        # print(possible_states)
        if not possible_states:
            return False
        lines = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        # if self.count >= 2:
        for line in lines:
            positions=[state[line[0]],state[line[1]], state[line[2]]]
            if positions.count('O')==2 and positions.count(' ')==1:
                empty = line[positions.index(' ')]
                next_state = state[:empty] + 'O' + state[empty+1:]
                self.make_move(next_state)
                return True
        for line in lines:
            positions=[state[line[0]],state[line[1]], state[line[2]]]
            if positions.count('X')==2 and positions.count(' ')==1:
                empty = line[positions.index(' ')]
                next_state = state[:empty] + 'O' + state[empty+1:]
                self.make_move(next_state)
                return True
        if state[4] == ' ':
            next_state = state[:4] + 'O' + state[5:] 
            self.make_move(next_state) 
            return True 
        # for i in [0, 2, 6, 8]: 
        #     if state[i] == ' ': 
        #         next_state = state[:i] + 'O' + state[i+1:] 
        #         self.make_move(next_state) 
        #         return True          
        
        next_state = random.choice(possible_states)
        self.make_move(next_state)
        return True


st.title("TIC TAC TOE GAME")

# -------- Game Mode --------
mode = st.radio(
    "Choose Mode",
    ["Human vs AI", "Human vs Human"],
    horizontal=True
)

# Reset game when mode changes
if "last_mode" not in st.session_state or st.session_state.last_mode != mode:
    st.session_state.game = TicTacToeGame()
    st.session_state.last_mode = mode

if "game" not in st.session_state:
    st.session_state.game = TicTacToeGame()

game = st.session_state.game

st.divider()

# -------- Draw Board --------
cols = st.columns(3)

for i in range(9):
    with cols[i % 3]:
        cell = game.state[i]
        label = cell if cell != ' ' else ' '

        if st.button(
            label,
            key=i,
            disabled=(cell != ' ' or game.winner is not None)
        ):
            new_state = game.state[:i] + game.player + game.state[i+1:]
            if game.make_move(new_state):
                st.rerun()

# -------- AI Move (ONLY in AI mode) --------
if (
    mode == "Human vs AI"
    and game.player == 'O'
    and game.playable()
    and game.winner is None
):
    st.info("🤖 AI is playing...")
    game.ai_move()
    st.rerun()

st.divider()

# -------- Game Status --------
if game.winner:
    st.success(f"🎉 Winner: {game.winner}")
elif not game.playable():
    st.warning("🤝 Game Draw!")
else:
    st.info(f"👉 Player {game.player}'s turn")

# -------- Reset --------
if st.button("🔄 Reset Game"):
    st.session_state.game = TicTacToeGame()
    st.rerun()





