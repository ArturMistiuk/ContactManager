from datetime import date

CURRENT_DAY = date.today()


def is_upcoming_birthday(users):
    birthday_boys = []
    for user in users:
        days_until_birthday = (user.birthday - CURRENT_DAY).days
        if 0 <= days_until_birthday <= 7:
            birthday_boys.append(user)
    return birthday_boys
