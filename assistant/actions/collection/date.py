import datetime
from datetime import date

from assistant.actions.action import Action
from assistant.models.message import Message

french_days: dict[str, str] = {
    "monday": "lundi",
    "tuesday": "mardi",
    "wednesday": "mercredi",
    "thursday": "jeudi",
    "friday": "vendredi",
    "saturday": "samedi",
    "sunday": "dimanche",
}
french_months: dict[str, str] = {
    "january": "janvier",
    "february": "février",
    "march": "mars",
    "april": "avril",
    "may": "mai",
    "june": "juin",
    "july": "juillet",
    "august": "août",
    "september": "septembre",
    "october": "octobre",
    "november": "novembre",
    "december": "décembre",
}


class TimeAction(Action):
    """This action tells the time."""

    def response(self, message: Message) -> Message:
        hour, minute = datetime.datetime.now().strftime("%H %M").split(" ")
        return Message(content=f"Il est actuellement {hour} heures {minute}")


class DateAction(Action):
    """This action tells the date."""

    def response(self, message: Message) -> Message:
        day, day_number, month, year = date.today().strftime("%A %d %B %Y").split(" ")
        return Message(
            content=f"Nous sommes le {french_days[day.lower()]} {day_number} {french_months[month.lower()]} {year}"
        )
