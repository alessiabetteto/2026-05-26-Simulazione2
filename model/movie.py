from dataclasses import dataclass
from datetime import datetime


@dataclass

class Movie:
    id: str
    title: str
    year: int
    date_published: datetime
    duration: int
    country: str
    worlwide_gross_income: str
    languages: str
    production_company: str

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f"{self.title} ({self.id} - {self.year})"

