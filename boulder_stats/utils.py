"""Helper functions."""
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

OPENING_TIME = "09:00"
CLOSING_TIME = "23:00"


def get_slots(date, opening_time=OPENING_TIME, closing_time=CLOSING_TIME):
    """Return date_range corresponding to slots that can be booked online."""
    if isinstance(date, str):
        date = pd.Timestamp(date).date()
    if isinstance(opening_time, str):
        opening_time = pd.Timestamp(opening_time).time()
    if isinstance(closing_time, str):
        closing_time = pd.Timestamp(closing_time).time()
    start = pd.Timestamp.combine(date=date, time=opening_time)
    end = pd.Timestamp.combine(date=date, time=closing_time)
    return pd.date_range(start=start, end=end, freq="0.5H")


assert all(get_slots("2020-10-28") == get_slots(pd.Timestamp("2020-10-28")))


def is_open(datetime):
    """Return weather datetime lies in the opening times or not."""
    dow = datetime.dayofweek
    time = datetime.time()
    earlier_days = {6, 7}
    start = pd.Timestamp("10:00" if dow not in earlier_days else "09:00").time()
    end = pd.Timestamp("22:00").time()
    return start <= time <= end


def is_future(datetime):
    """Return weather ``datetime`` lies in the future."""
    return datetime > pd.Timestamp.now()


def next_weekday(datetime, weekday):
    """Return date of next ``weekday``."""
    days_ahead = weekday - datetime.weekday()
    if days_ahead < 0:  # Target day already happened this week
        days_ahead += 7
    return datetime + pd.Timedelta(days=days_ahead)


def get_colors_for_df(df, list_of_colors=None, fix_max=None):
    """Interpolate between ``list_of_colors`` to get ``N=fix_max or max(df)`` different color shades.

    Return list with appropriate colors depending on y-value of ``df``.
    """
    list_of_colors = list_of_colors or ["tab:green", "gold", "tab:red"]
    color_palette = LinearSegmentedColormap.from_list(
        "ampel", list_of_colors, N=fix_max or max(df),
    )
    colors = color_palette([int(x) for x in df.fillna(0)])
    return colors


def add_numbers_to_boxplot(df, color=None):
    """Add entries of df as text at appropriate height and with color ``color[i]`` in plot."""
    for i, (index, data) in enumerate(df.items()):
        print(i)
        plt.text(
            x=index,
            y=data + 1.0,
            s=f"{data:.0f}" if data > 0 else "",
            fontweight="bold",
            color=color[i] if color is not None and i < len(color) else None,
            ha="center",
        )


def box_plot_df(
    df, key, x=None, width=20, colors=None, add_nums=True,
):
    """Make a box plot from ``df[key]``."""
    x = x or df.index
    y = df[key]
    plt_kwargs = {}
    if colors is not None:
        plt_kwargs["color"] = colors
    if add_nums:
        add_numbers_to_boxplot(df[key], **plt_kwargs)
    plt.bar(x, y, label=key, width=width, **plt_kwargs)
