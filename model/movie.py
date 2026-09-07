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
    tuttiBrani: list
    tuttiBrani: set
    tuttiBrani: dict

    def __hash__(self):
        return hash(self.id)
        # se l'hash è una tupla:
        # return hash((self.GeneID, self.Function))

    def __eq__(self, other):
        return self.id == other.id
        # se l'hash è una tupla:
        # return (self.GeneID, self.Function) == (other.GeneID, other.Function)

    def __str__(self):
        return f"{self.title} ({self.id} - {self.year})"

