from state_machine.state_machine import StateMachine, State, Event


# Extend State to print State name on entry
class MyState(State):

    def __init__(self, name):
        super().__init__(name)
        self.on_entry(self.entry_callback)
        self.on_exit(self.exit_callback)

    def entry_callback(self, data):
        print(self.name)

    def exit_callback(self, data):
        pass


def output_three_in_a_row(data):
    """
    function to be called when event has been triggered 3 times in a row
    prints 'THREE IN A ROW!'
    :param data:
    :return:
    """
    print('event triggered THREE TIMES IN A ROW!')


# create states

s_a = MyState('A')
s_b = MyState('B')
s_c = MyState('C')
s_d = MyState('D')
s_d.on_entry(output_three_in_a_row)
s_e = MyState('E')
s_f = MyState('F')
s_g = MyState('G')
s_g.on_entry(output_three_in_a_row)

# create events

e0 = Event('0')
e1 = Event('1')

# create State Machine

triple_event = StateMachine('Triple Event')

# add states to State Machine

triple_event.add_state(s_a, initial_state=True)
triple_event.add_state(s_b)
triple_event.add_state(s_c)
triple_event.add_state(s_d)
triple_event.add_state(s_e)
triple_event.add_state(s_f)
triple_event.add_state(s_g)

# add events to State Machine

triple_event.add_event(e0)
triple_event.add_event(e1)

# add transitions to State Machine

triple_event.add_transition(s_a, s_b, e0)
triple_event.add_transition(s_a, s_e, e1)

triple_event.add_transition(s_b, s_c, e0)
triple_event.add_transition(s_b, s_e, e1)

triple_event.add_transition(s_c, s_d, e0)
triple_event.add_transition(s_c, s_e, e1)

triple_event.add_transition(s_d, s_e, e1)

triple_event.add_transition(s_e, s_b, e0)
triple_event.add_transition(s_e, s_f, e1)

triple_event.add_transition(s_f, s_b, e0)
triple_event.add_transition(s_f, s_g, e1)

triple_event.add_transition(s_g, s_e, e0)

# start State Machine

triple_event.start('')

# trigger events

triple_event.trigger_event(e0)
triple_event.trigger_event(e1)
triple_event.trigger_event(e0)
triple_event.trigger_event(e0)

# trigger e0 third time in a row

triple_event.trigger_event(e0)

# stop State Machine

triple_event.stop('')

# start State Machine again

triple_event.start('')

# trigger a few events

triple_event.trigger_event(e0)
triple_event.trigger_event(e1)

# stop State Machine

triple_event.stop('')

# restart State Machine to continue from last stored state

triple_event.restart('')

# trigger a few more events to reach 3 e1 events in a row
triple_event.trigger_event(e1)
triple_event.trigger_event(e1)