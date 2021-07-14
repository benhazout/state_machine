import pickle

STATE_FILE = 'state_file'


def read_state():
    """
    Read State from file using pickle
    loads python object stored in STATE_FILE using pickle
    :return: returns python object
    """
    file = open(STATE_FILE, 'rb')
    state = pickle.load(file)
    file.close()
    return state


def write_state(state):
    """
    Write State to file using pickle
    :param state: python object to be stored in STATE_FILE using pickle
    :return:
    """
    file = open(STATE_FILE, 'wb')
    pickle.dump(state, file)
    file.close()
