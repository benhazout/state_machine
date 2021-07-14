
## Installation

To install state_machine package run:

``` commandline
pip3 install git+https://github.com/benhazout/state_machine.git

```
or clone the repository  and install using setup.py:
``` commandline
git clone https://github.com/benhazout/state_machine.git
python3 setup.py install

```
# state_machine

**Description**:  Framework for building state machines. Provides common functionality and elements of state machines such as State, Event, Transition (Normal, Self and Null) and StateMachine.

## usage example
**Description**: A system that supports 2 types of events. The role of the machine is to output a message when it detects that the same type of event has been triggered 3 times in a row.

First lets grasp a better understanding through a UML: 

![](https://i.ibb.co/wJZtTgY/fsm-three-in-a-row.jpg)

in order to implement this in the example.py:

First import state_machine
``` python
from state_machine.state_machine import StateMachine, State, Event
```

####Extend State to print State name on entry
- note we added on every state entry to print the state's name - this is in order that we can track the current state without requesting it 'manully' every time.

``` python
class MyState(State):

    def __init__(self, name):
        super().__init__(name)
        self.on_entry(self.entry_callback)
        self.on_exit(self.exit_callback)

    def entry_callback(self, data):
        print(self.name)

    def exit_callback(self, data):
        pass
```
####Create output function - to be called when event has been triggered 3 times in a row
``` python
def output_three_in_a_row(data):
    print('event triggered THREE TIMES IN A ROW!')
```
####Create states
- note that on states D and G (final states) we added our output function to the state 'on_entry' callbacks - so when entering these states 'output_three_in_a_row' will be called

``` python
s_a = MyState('A')
s_b = MyState('B')
s_c = MyState('C')
s_d = MyState('D')
s_d.on_entry(output_three_in_a_row)
s_e = MyState('E')
s_f = MyState('F')
s_g = MyState('G')
s_g.on_entry(output_three_in_a_row)
```
####Create events
``` python
e0 = Event('0')
e1 = Event('1')
```
####Create State Machine
``` python
triple_event = StateMachine('Triple Event')
```
####Add states to State Machine
``` python
triple_event.add_state(s_a, initial_state=True)
triple_event.add_state(s_b)
triple_event.add_state(s_c)
triple_event.add_state(s_d)
triple_event.add_state(s_e)
triple_event.add_state(s_f)
triple_event.add_state(s_g)
```
####Add events to State Machine
``` python
triple_event.add_event(e0)
triple_event.add_event(e1)
```
####Add transitions to State Machine
- pay attention - this implements the logic of the machine

``` python
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
```
####Start the machine
``` python
triple_event.start('')
```
####Trigger events
``` python
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
```
####Output
``` commandline
A
B
E
B
C
D
event triggered THREE TIMES IN A ROW!
A
B
E
E
F
G
event triggered THREE TIMES IN A ROW!

```

####Full example.py file
``` python
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
```
## Objects properties and methods
### State, Event, Transition and StateMachine
###State
***Properties***:
-name
-entry_callbacks
-exit_callbacks

***Methods***:
-on_entry
-on_exit
-start (starts all on entry callbacks)
-stop (starts all on exit callbacks)
###Event
***Properties***:
-name
###Transition
***Properties***:
-event
-source_state
-destination_state
-condition (optional)
-action (optional)

***Methods***:
-add_condition
-add_action

####NormalTransition(Transition)
passes state both as source and destination,  stops and starts state callbacks 
***Properties***:  
-from
-to
####SelfTransition(Transition)
passes state both as source and destination,  stops and starts state callbacks 
***Properties***:  
-self
####NullTransition(Transition)
passes state both as source and destination,  doesn't stop/start state callbacks
***Properties***:  
-self
###StateMachine
***Properties***:
-name
-states
-events
-transitions
-initial_state 
-final_state
-current_state

***Methods***:
-start (start the State Machine and the initial state)
-restart (when wanting to restart a machine that has stopped for some reason, and we want to continue from it's last-current state)
-stop (stop the machine)
-add_state
-add_event
-add_transition
-add_self_transition
-add_null_transition
-trigger_event (trigger an event)

