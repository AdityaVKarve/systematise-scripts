from app.engine.process_manager import create_event_and_handle
import random
from datetime import datetime

class Customer:
    def __init__(self, name, logger=None):
        self.name = name
        self.state = "Walk In"
        self.visited_at = datetime.now()
        self.logger = logger

    def _create_event(self, event_name, metadata=None):
        metadata = metadata or {}
        metadata.update({"customer": self.name, "timestamp": datetime.now().isoformat()})
        event_id = create_event_and_handle(
            name=event_name,
            description=f"Customer {self.name} performed event: {event_name}",
            metadata=metadata,
            logger=self.logger  # <-- pass logger down
        )
        return event_id

    def simulate(self):
        transitions = {
            "Walk In": [
                ("Order Drink", 0.85),
                ("Customer Walk Out", 0.15),
            ],
            "Order Drink": [
                ("Customer Sign Up", 0.7),
                ("Customer Not Sign Up", 0.3),
            ],
            "Customer Sign Up": [
                ("Drink readied", 1.0),
            ],
            "Customer Not Sign Up": [
                ("Drink readied", 1.0),
            ],
            "Drink readied": [
                ("Customer Walk Out", 1.0),
            ],
        }

        current_state = "Walk In"
        while current_state not in ("Customer Walk Out", "Walk Out"):
            self._create_event(current_state)
            current_state = self._next_state(transitions.get(current_state, []))

        # Final event
        self._create_event(current_state)

    def _next_state(self, choices):
        rand = random.random()
        cumulative = 0
        for state, prob in choices:
            cumulative += prob
            if rand <= cumulative:
                return state
        return choices[-1][0]
