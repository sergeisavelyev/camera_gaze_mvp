class ContactCounter:
    """
    Считает события контакта на основе бинарного сигнала looking / not looking.
    Использует антидребезг и state machine.
    """

    STATE_NOT_LOOKING = "NOT_LOOKING"
    STATE_LOOKING = "LOOKING"

    def __init__(self, frames_to_confirm_looking: int = 8, frames_to_confirm_not_looking: int = 5):
        self.frames_to_confirm_looking = frames_to_confirm_looking
        self.frames_to_confirm_not_looking = frames_to_confirm_not_looking

        self.state = self.STATE_NOT_LOOKING
        self.contacts_count = 0

        self.looking_streak = 0
        self.not_looking_streak = 0

    def update(self, looking: bool) -> dict:
        new_contact = False

        if looking:
            self.looking_streak += 1
            self.not_looking_streak = 0
        else:
            self.not_looking_streak += 1
            self.looking_streak = 0

        if self.state == self.STATE_NOT_LOOKING:
            if self.looking_streak >= self.frames_to_confirm_looking:
                self.state = self.STATE_LOOKING
                self.contacts_count += 1
                new_contact = True

        elif self.state == self.STATE_LOOKING:
            if self.not_looking_streak >= self.frames_to_confirm_not_looking:
                self.state = self.STATE_NOT_LOOKING

        return {
            "state": self.state,
            "contacts_count": self.contacts_count,
            "new_contact": new_contact,
            "looking_streak": self.looking_streak,
            "not_looking_streak": self.not_looking_streak,
        }