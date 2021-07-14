from typing import List, Callable, Any, Optional
from . import pickle_actions


class State:
    def __init__(self, name):
        self._name = name
        self._entry_callbacks: List[Callable[[Any], None]] = []
        self._exit_callbacks: List[Callable[[Any], None]] = []

    def __eq__(self, other):
        if other.name == self._name:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __call__(self, data: Any):
        pass

    def on_entry(self, callback: Callable[[Any], None]):
        self._entry_callbacks.append(callback)

    def on_exit(self, callback: Callable[[], None]):
        self._exit_callbacks.append(callback)

    def start(self, data: Any):
        for callback in self._entry_callbacks:
            callback(data)

    def stop(self, data: Any):
        for callback in self._exit_callbacks:
            callback(data)

    @property
    def name(self):
        return self._name


class Event(object):

    def __init__(self, name):
        self._name = name

    def __eq__(self, other):
        if other.name == self._name:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def name(self):
        return self._name


class Transition(object):

    def __init__(self, event: Event, src: State, dst: State):
        self._event = event
        self._source_state = src
        self._destination_state = dst
        self._condition: Optional[Callable[[Any], bool]] = None
        self._action: Optional[Callable[[Any], None]] = None

    def __call__(self, data: Any):
        raise NotImplementedError

    def add_condition(self, callback: Callable[[Any], bool]):
        self._condition = callback

    def add_action(self, callback: Callable[[Any], Any]):
        self._action = callback

    @property
    def event(self):
        return self._event

    @property
    def source_state(self):
        return self._source_state

    @property
    def destination_state(self):
        return self._destination_state


class NormalTransition(Transition):

    def __init__(self, source_state: State, destination_state: State,
                 event: Event):
        super().__init__(event, source_state, destination_state)
        self._from = source_state
        self._to = destination_state

    def __call__(self, data: Any):
        if not self._condition or self._condition(data):
            if self._action:
                self._action(data)
            self._from.stop(data)
            self._to.start(data)


class SelfTransition(Transition):

    def __init__(self, source_state: State, event: Event):
        super().__init__(event, source_state, source_state)
        self._state = source_state

    def __call__(self, data: Any):
        if not self._condition or self._condition(data):
            if self._action:
                self._action(data)
            self._state.stop(data)
            self._state.start(data)


class NullTransition(Transition):

    def __init__(self, source_state: State, event: Event):
        super().__init__(event, source_state, source_state)
        self._state = source_state

    def __call__(self, data: Any):
        if not self._condition or self._condition(data):
            if self._action:
                self._action(data)


class StateMachine:
    def __init__(self, name):
        self._name = name
        self._states: List[State] = []
        self._events: List[Event] = []
        self._transitions: List[Transition] = []
        self._initial_state: Optional[State] = None
        self._final_state: Optional[State] = None
        self._current_state: Optional[State] = None

    def __eq__(self, other):
        if other.name == self._name:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self._name

    def start(self, data: Any):
        """
        Start the State Machine and the initial state
        :param data: data to be passed to the 'start' function of the initial state
        :return:
        """
        if not self._initial_state:
            raise ValueError("initial state is not set")
        self._current_state = self._initial_state

        # write current state to file
        pickle_actions.write_state(self._current_state)

        self._current_state.start(data)

    def restart(self, data: Any):
        """
        When wanting to restart a machine that has stopped for some reason,
        and we want to continue from it's last-current state
        :param data: data to be passed to the 'start' function of the state
        :return:
        """
        last_state = pickle_actions.read_state()

        # make sure that a state was stored from previous machine start
        if not last_state:
            raise ValueError("No last state to restart from from")

        self._initial_state = last_state
        if not self._initial_state:
            raise ValueError("initial state is not set")
        self._current_state = self._initial_state
        self._current_state.start(data)

    def stop(self, data: Any):
        """
        Stop the machine
        :param data: data to be passed to the 'stop' function of the state
        :return:
        """
        if not self._initial_state:
            raise ValueError("initial state is not set")
        if self._current_state is None:
            raise ValueError("state machine has not been started")
        self._current_state.stop(data)

    def add_state(self, state: State, initial_state: bool = False, final_state: bool = False):
        if state in self._states:
            raise ValueError("attempting to add same state twice")
        self._states.append(state)

        if not self._initial_state and initial_state:
            self._initial_state = state

        if not self._final_state and final_state:
            self._final_state = state

    def add_event(self, event: Event):
        self._events.append(event)

    def add_transition(self, src: State, dst: State, evt: Event) -> Optional[Transition]:
        transition = None
        if src in self._states and dst in self._states and evt in self._events:
            transition = NormalTransition(src, dst, evt)
            self._transitions.append(transition)
        return transition

    def add_self_transition(self, state: State, evt: Event) -> Optional[Transition]:
        transition = None
        if state in self._states and evt in self._events:
            transition = SelfTransition(state, evt)
            self._transitions.append(transition)
        return transition

    def add_null_transition(self, state: State, evt: Event) -> Optional[Transition]:
        transition = None
        if state in self._states and evt in self._events:
            transition = NullTransition(state, evt)
            self._transitions.append(transition)
        return transition

    def trigger_event(self, evt: Event, data: Any = None):
        """
        Trigger an event
        :param evt: event to trigger
        :param data: data to be passed to transition
        :return:
        """
        if not self._initial_state:
            raise ValueError("initial state is not set")

        if self._current_state is None:
            raise ValueError("state machine has not been started")

        for transition in self._transitions:

            # execute event only  for the current state
            if transition.source_state == self._current_state and transition.event == evt:
                self._current_state = transition.destination_state

                # write current state to file
                pickle_actions.write_state(self._current_state)

                transition(data)
                break

    @property
    def current_state(self):
        return self._current_state

    @property
    def name(self):
        return self._name
