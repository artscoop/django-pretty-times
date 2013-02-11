from datetime import datetime, tzinfo, timedelta


__all__ = ("date", )


class UTC(tzinfo):

    def utcoffset(self, dt):
        return timedelta(hours=0, minutes=0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)


def date(time):
    now = get_now(time)

    if time > now:
        past = False
        diff = time - now
    else:
        past = True
        diff = now - time

    days = diff.days

    if days is 0:
        return get_small_increments(diff.seconds, past)
    else:
        return get_large_increments(days, past)


def get_now(time):
    if time.tzinfo:
        utc = UTC()
    else:
        utc = None
    return datetime.now(utc)


def get_small_increments(seconds, past):
    if seconds < 10:
        result = 'just now'
    elif seconds < 60:
        result = _pretty_format(seconds, 1, 'seconds', past)
    elif seconds < 120:
        result = past and 'a minute ago' or 'in a minute'
    elif seconds < 3600:
        result = _pretty_format(seconds, 60, 'minutes', past)
    elif seconds < 7200:
        result = past and 'an hour ago' or 'in an hour'
    else:
        result = _pretty_format(seconds, 3600, 'hours', past)
    return result


def get_large_increments(days, past):
    if days == 1:
        result = past and 'yesterday' or 'tomorrow'
    elif days < 7:
        result = _pretty_format(days, 1, 'days', past)
    elif days < 14:
        result = past and 'last week' or 'next week'
    elif days < 31:
        result = _pretty_format(days, 7, 'weeks', past)
    elif days < 61:
        result = past and 'last month' or 'next month'
    elif days < 365:
        result = _pretty_format(days, 30, 'months', past)
    elif days < 730:
        result = past and 'last year' or 'next year'
    else:
        result = _pretty_format(days, 365, 'years', past)
    return result


def _pretty_format(diff_amount, units, text, past):
    pretty_time = (diff_amount + units / 2) / units
    return ("%d %s ago" if past else "in %d %s") % (pretty_time, text)
