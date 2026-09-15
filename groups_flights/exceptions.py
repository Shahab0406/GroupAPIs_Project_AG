class InsufficientSeatsError(Exception):
    def __init__(self, seat_type: str, requested: int, available: int):
        self.seat_type = seat_type
        super().__init__(
            f"Only {available} {seat_type} seat(s) available, but {requested} requested."
        )
