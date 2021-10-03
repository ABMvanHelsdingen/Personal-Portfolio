"""
OPTIONAL TODO: Testing

This function implements testing that can (and should) be extended for the project.

This is primarily so you can execute unit tests on your code without needing to be a part of a
network of devices.

It contains an example that tests the communication protocol parsing for recieving messages.
Also included is some mocking functionality in the folder testing_modules. These mimic the behaviour
of the micro:bit modules. You can and should extend those, especially if you use new functions in
your code.
"""
import sys
import random
from testing_filesx import radio, microbit, utime

"""
Here we are setting up the mock libraries so that when we do import our code that would be flashed,
it can actually find and use these modules.

Note that this isn't the actual functionality of those modules - but we are creating something
functionally similar that we can test on. For example, the radio module on the micro:bit doesn't
have a push_message function - we just need to somehow create a message to read.

"""
sys.modules['radio'] = radio
sys.modules['microbit'] = microbit
sys.modules['utime'] = utime

import main
"""
Note: We need to heed the scope of the modules - we must call prototype.radio, instead of just
radio, even though they point to the same module, because there is a prototype scope that contains
its own radio module.

Also note we have only tested happy paths (ideal/standard inputs) here.
"""
def test_choose_opponent():
    """ Test the choose_opponent function with a random ID number """
    # Setup
    opponent_id = random.randint(0, 99)
    ida, idb = (opponent_id//10, opponent_id%10)
    history = ['a']*ida + ['b'] + ['a']*idb + ['b']
    main.microbit.button_history.load_history(history)
    # Run test
    got_opponent_id = main.choose_opponent()
    assert got_opponent_id == bytes(str(opponent_id), 'UTF-8')
    print('Passed Assert')

def test_choose_play():
    """ Test the choose_play function with a given play """
    # TODO
    assert False

def test_send_choice():
    """ Test the play message sending capabilities with a given message """
    # Setup
    main.MYID = b'69'
    opponent_id = b'42'
    the_play = b'R'
    round_number = 7
    # Run test
    main.send_choice(opponent_id, the_play, round_number)
    assert main.radio.get_last_out() == b'4269R7'

def test_acknowledge_message():
    """ Test the acknowledgement message construction and send functionality """
    # Setup
    main.MYID = b'69'
    opponent_id = b'42'
    round_number = 7
    # Run test
    main.send_acknowledgement(opponent_id, round_number)
    assert main.radio.get_last_out() == b'4269X7'

def test_parse_message():
    """ Test the ability to parse an incoming message """
    # TODO: THIS TEST IS INCOMPLETE
    # Setup

    # Case 1: Received a play
    received_message_case_1 = b'6942R6'
    radio.push_message(received_message_case_1)
    # Case 2: Received an acknowledgement
    received_message_case_2 = b'6942X5'
    radio.push_message(received_message_case_2)

    # Run Test
    assert False
test_choose_opponent()