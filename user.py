"""
Represents a user with a rank, username, and score.
"""
class User:

    def __init__(self, rank: int, username: str, score: int):
        self.rank = rank
        self.username = username
        self.score = score
