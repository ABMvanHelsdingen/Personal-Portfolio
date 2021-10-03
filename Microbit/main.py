import microbit
import utime
import radio
import random

# GLOBAL
MYID = b'48'
RPS = (b'R', b'P', b'S')
ROCK = microbit.Image('00000:09990:09990:09990:00000')
PAPER = microbit.Image('99999:90009:90009:90009:99999')
SCISSORS = microbit.Image('99009:99090:00900:99090:99009')


def choose_opponent():
    # """ Return the opponent id from button presses
    #
    # Returns
    # -------
    # bytes:
    #   the 2 digit opponent ID in bytes
    #
    # """

    num = [0]*2 #ID number must be 2 digits even if 0-9
    idx = 0
    while idx < len(num):
        microbit.sleep(100)
        microbit.display.show(num[idx], wait=False)
        if microbit.button_a.was_pressed():
            num[idx] = (num[idx] + 1)%10 #Increment digit being modified
        if microbit.button_b.was_pressed():
            microbit.display.show('X')
            idx += 1 #Change digit being modified
    microbit.display.clear()
    return bytes(''.join(str(n) for n in num), 'UTF-8')

def choose_play(last_move,score, opponent_score, decision_matrix):
    # """ Returns play, based on either an AI strategy or random choice
    #
    # Parameters:
    # -----------
    # last_move: str
    #   'R','P' or 'S', the last move of the opponent
    # score: int
    #   your current score
    # opponent_score: int
    #   the opponents score
    # decision_matrix: dict
    #   3x3 grid of information about opponent's previous moves
    #
    # Returns
    # -------
    # bytes:
    #   b'R', b'P',or b'S': the chosen move
    # """

    #Number of times before the opponent has played their most recent move.
    sum_moves=decision_matrix[last_move]['R']+decision_matrix[last_move]['P']+decision_matrix[last_move]['S']

    #Use random strategy during first 3 rounds, when trailing, or when no data exists on previous move
    if score+opponent_score<=3 or score+2<=opponent_score or sum_moves==0:
        number=random.randint(0,2)
        if number==0:
            microbit.display.show(ROCK)
        elif number==1:
            microbit.display.show(PAPER)
        else:
            microbit.display.show(SCISSORS)

    else:
        cdf=random.randint(1,sum_moves) #Generate random integer
        if cdf<=decision_matrix[last_move]['R']:
            microbit.display.show(PAPER) #In this simulation opponent has played rock, so play paper
            number=1
        elif cdf<=decision_matrix[last_move]['R']+decision_matrix[last_move]['P']:
            microbit.display.show(SCISSORS) #Scissors beats paper
            number=2
        else:
            microbit.display.show(ROCK) #Rock beats scissors
            number=0

    while True:
        if microbit.button_a.was_pressed(): #Only return choice when button A pressed
            return RPS[number]

def send_choice(opponent_id, play, round_number):
    # """ Sends a message via the radio """
    # Parameters:
    # -----------
    # opponent_id: bytes
    #   ID number of opponent
    # play: bytes
    #   b'R', b'P' or b'S'
    # round_number: int
    #   current round number
    #
    # Returns:
    # --------
    # int:
    #   time the message was sent
    # """

    round_number=bytes(str(round_number), 'UTF-8') #From int to bytes of str

    radio.send_bytes(opponent_id+MYID+play+round_number)

    return utime.ticks_ms()

def send_acknowledgement(opponent_id, round_number):
    # """ Sends an acknowledgement message via the radio """
    # Parameters:
    # -----------
    #
    # opponent_id: bytes
    #   ID number of opponent
    # round_number: int
    #   current round number
    #
    round_number=bytes(str(round_number), 'UTF-8')

    radio.send_bytes(opponent_id+MYID+b'X'+round_number)

def parse_message(opponent_id, round_number):
    # """ Receive and parse the next valid message, sending an acknowledgment message if necessary
    #
    # Parameters:
    # -----------
    # opponent_id: bytes
    #   ID number of opponent
    # round_number: int
    #   current round number
    #
    # Returns
    # -------
    # bytes:
    #   the relevant part of the message received, else:
    # None
    # """


    message=radio.receive_bytes()

    if message and len(message)>=6:
        if message[0:2]==MYID and message[2:4]==opponent_id: #From opponent to us
            msg_round = int(str(message[5:], 'UTF-8')) #bytes to int
            #Message is a play from current or previous round
            if message_round<=round_number and message[4:5] in RPS:
                send_acknowledgement(opponent_id,message_round)
            #If message relates to current round
            if message_round==round_number:
                return message[4:5]

    return None #If message not relevant

def resolve(my, opp):
    # """ Returns the outcome of a rock-paper-scissors match
    # Also displays the result
    #
    # Parameters
    # ----------
    # my  : bytes
    #     The choice of rock/paper/scissors that this micro:bit made
    # opp : bytes
    #     The choice of rock/paper/scissors that the opponent micro:bit made
    #
    # Returns
    # -------
    # int :
    #     Numerical value for the outcome as listed below
    #      0: Loss/Draw
    #     +1: Win
    #
    # Notes
    # -----
    # Input parameters should be one of b'R', b'P', b'S'
    #
    # Examples
    # --------
    # solve(b'R', b'P') returns 0 (Loss)
    # solve(b'R', b'S') returns 1 (Win)
    # solve(b'R', b'R') returns 0 (Draw)
    #
    # """
    result = RPS.index(my) - RPS.index(opp)
    resolution = [0, 1, 0][result]
    face = [microbit.Image.ASLEEP, microbit.Image.HAPPY, microbit.Image.SAD][result]
    microbit.display.show(face)
    microbit.sleep(333)
    return resolution

def display_score(score, times=3):
    # """ Flashes the score on the display
    #
    # Parameters
    # ----------
    # score : int
    #     The current score
    # times : int
    #     Number of times to flash
    #
    # Returns
    # -------
    # None
    #
    # Notes
    # -----
    # The variable score should be between 0 and 9, inclusive. This is due to a limitation of showing
    # images on the micro:bit display that require more than one screen's worth of pixels to show.
    # """
    screen_off = microbit.Image(':'.join(['0'*5]*5))
    microbit.display.show([screen_off, str(score)]*times, delay=100)

def main():
    # """ Main control loop"""
    # set up the radio
    radio.config(power=6, queue=20)
    radio.on()
    # initialise scores and round number
    score = 0
    opponent_score=0
    round_number = 0
    #This dictionary stores information about successive moves by opponent.
    #decision_matrix[last_move][this_move] is the number of times the opponent has
    # played last_move followed by this_move
    decision_matrix={'R':{'R':0,'P':0,'S':0},'P':{'R':0,'P':0,'S':0},'S':{'R':0,'P':0,'S':0}}
    last_move='P' #Placeholder, line 242 prevents this from causing issues
    # select an opponent
    opponent_id = choose_opponent()
    microbit.sleep(200)
    # loop forever
    while True:
        # get a play from the buttons
        choice = choose_play(last_move,score, opponent_score,decision_matrix)
        # send choice, record time
        send_time=send_choice(opponent_id, choice, round_number)
        acknowledged, resolved = (False, False)
        # passive waiting display
        microbit.display.show(microbit.Image.ALL_CLOCKS, wait=False, loop=True)
        while not acknowledged or not resolved:
            # get a message from the radio
            message = parse_message(opponent_id, round_number)
            if message is not None and message in RPS: #If a play by opponent
                result = resolve(choice, message) #Resolve the round
                resolved=True
                score=score+result #Update score
                this_move=str(message,'UTF-8') #From bytes to str
                opponent_score=opponent_score+1-result
                #Record relationship between opponent's successive moves
                if round_number!=0:
                    decision_matrix[last_move][this_move]=decision_matrix[last_move][this_move]+1
                last_move=this_move
                display_score(score) #Display score
            if message is not None and message==b'X': #If acknowledgement
                acknowledged=True
            # if not acknowledged, resend message every 3s
            if not acknowledged and utime.ticks_diff(utime.ticks_ms, send_time) > 3000:
                send_choice(opponent_id, choice, round_number)
                send_time = utime.ticks_ms()
        round_number=round_number+1

if __name__=='__main__':
    main()