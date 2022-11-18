import time
from datetime import datetime


def date(
    target,
    clock: bool = True,
    seconds: bool = False,
    ago: bool = False,
    only_ago: bool = False,
):
    if isinstance(target, int) or isinstance(target, float):
        target = datetime.utcfromtimestamp(target)

    unix = int(time.mktime(target.timetuple()))
    timestamp = f"<t:{unix}:{'f' if clock else 'D'}>"
    if ago:
        timestamp += f" (<t:{unix}:R>)"
    if only_ago:
        timestamp = f"<t:{unix}:R>"
    return timestamp
