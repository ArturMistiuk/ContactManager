from datetime import date

CURRENT_DAY = date.today()


def is_upcoming_birthday(users):
    """
The is_upcoming_birthday function takes a list of users and returns a list of users whose birthday is within the next 7 days.

:param users: Iterate through the list of users
:return: A list of users who have a birthday in the next 7 days
:rtype: List[Contact]
    """
    birthday_boys = []
    for user in users:
        days_until_birthday = (user.birthday - CURRENT_DAY).days
        if 0 <= days_until_birthday <= 7:
            birthday_boys.append(user)
    return birthday_boys
