from datetime import timedelta

SECONDS_IN_YEAR = 31536000
SECONDS_IN_MONTH = 2592000
SECONDS_IN_WEEK = 604800
SECONDS_IN_DAY = 86400
SECONDS_IN_HOUR = 3600
SECONDS_IN_MINUTE = 60

def td_to_str(td: timedelta, *, time_optional: bool = True, max_only: bool = False) -> str:
    output = []
    total_seconds = int(td.days * SECONDS_IN_DAY + td.seconds)

    if years := int(total_seconds // SECONDS_IN_YEAR):
        output.append(f'{years} {"years" if years > 1 else "year"}')
        total_seconds -= years * SECONDS_IN_YEAR

    if months := int(total_seconds // SECONDS_IN_MONTH):
        output.append(f'{months} {"months" if months > 1 else "month"}')
        total_seconds -= months * SECONDS_IN_MONTH

    if weeks := int(total_seconds // SECONDS_IN_WEEK):
        output.append(f'{weeks} {"weeks" if weeks > 1 else "week"}')
        total_seconds -= weeks * SECONDS_IN_WEEK

    if days := int(total_seconds // SECONDS_IN_DAY):
        output.append(f'{days} {"days" if days > 1 else "day"}')
        total_seconds -= days * SECONDS_IN_DAY
    
    if not time_optional or not output:
        if hours := int(total_seconds // SECONDS_IN_HOUR):
            output.append(f'{hours} {"hours" if hours > 1 else "hour"}')
            total_seconds -= hours * SECONDS_IN_HOUR

        if minutes := int(total_seconds // SECONDS_IN_MINUTE):
            output.append(f'{minutes} {"minutes" if minutes > 1 else "minute"}')
            total_seconds -= minutes * SECONDS_IN_MINUTE

        if seconds := total_seconds:
            output.append(f'{seconds} {"seconds" if seconds > 1 else "second"}')

    if not output:
        output = ['0 seconds']

    return ' '.join(output) if not max_only else output[0]
