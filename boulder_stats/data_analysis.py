"""Implements Analizer-class."""
import io

import attr
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from .utils import (
    box_plot_df,
    get_colors_for_df,
    get_slots,
)
from .paths import HDF_PATH


def nice_plot(df):
    """Plot ``df["av_visitors_2h"]`` as line and ``df["booked"]`` as colored bar plot."""
    df["av_visitors_2h"].plot(use_index=True, marker="s")
    plt.fill_between(
        df["av_visitors_2h"].index, df["av_visitors_2h"].values, alpha=0.03
    )
    colors = get_colors_for_df(df["booked"], fix_max=18)
    box_plot_df(df, key="booked", colors=colors)
    plt.legend()
    plt.xticks(
        df.index[::2],
        [
            x if i % 2 == 0 else ""
            for i, x in enumerate(df.index[::2].strftime("%H:%M"))
        ],
    )


def calc_cummulated_visitors(df):
    """Calculate total visitors at that time and average visitors over a 2h period and append to ``df``."""
    conv_profile_2h = [0.25, 0.5, 0.75, 1, 0.75, 0.5, 0.25]
    conv_profile_30m = [0, 0, 0, 1, 1, 1, 1]
    total_visitors = np.convolve(df["booked"], conv_profile_30m, mode="same")
    av_visitors_2h = np.convolve(df["booked"], conv_profile_2h, mode="same")
    df["visitors"] = total_visitors
    df["av_visitors_2h"] = av_visitors_2h


@attr.s(auto_attribs=True)
class Analyzer:
    """Handles the data_analysis of the obtained raw data."""

    hdf_path: str = HDF_PATH
    hdf_key: str = "raw"
    raw_df: pd.DataFrame = None
    max_visitors: int = 18

    def __attrs_post_init__(self):
        self.reload()

    def reload(self):
        """Update :attr:`raw_df` from hdf file."""
        self.raw_df = self.read_df_from_hdf()

    def read_df_from_hdf(self):
        """Return object saved under :attr:`hdf_path` with key :attr:`hdf_key`."""
        return pd.read_hdf(self.hdf_path, self.hdf_key)

    def time_series(self, slot):
        """Return time series of booked slots up to the slot time."""
        time_series = self.raw_df.xs(slot, level=1, drop_level=True)
        time_series = time_series[time_series.index < slot]
        return time_series

    def currently_booked(self, slot):
        """Return most recent element :meth:`time_series`.

        This is the current booked state of the slot.
        """
        time_series = self.time_series(slot)
        if len(time_series) == 0:
            return np.nan
        return time_series.iloc[-1]["visitors"]

    def get_currently_booked_day(self, date):
        """Use :meth:`currently_booked` to obtain current state of all slots on ``date``."""
        slots = get_slots(date)
        df = pd.DataFrame(index=slots, columns=["booked"], dtype=int)
        for slot in slots:
            df["booked"][slot] = self.currently_booked(slot)
        return df

    def last_actualized(self):
        """Return date of last actualization."""
        return self.raw_df.iloc[-1].name[0].strftime(format="%d.%m %H:%M")

    def fig_from_df(self, df):
        """Return bytes-object of plot as .png file."""
        nice_plot(df)
        day = df.index[0].date().strftime(format="%A %d.%m.%y")
        plt.title(f"{day} (last updated: {self.last_actualized()})")
        buff = io.BytesIO()
        plt.savefig(buff, format="png")
        plt.close()
        buff.seek(0)
        return buff

    def get_plot_bytes(self, date):
        """Return fig with bookings for a given day and average visitors as bytes-obj of .png-file."""
        df = self.get_currently_booked_day(date)
        calc_cummulated_visitors(df)
        return self.fig_from_df(df)


if __name__ == "__main__":
    plt.style.use("seaborn-notebook")
    analyzer = Analyzer()
    test_df = analyzer.get_currently_booked_day("2020-10-26")
    calc_cummulated_visitors(test_df)
    analyzer.get_plot_bytes("2020-10-28")
    plt.show()

    # print(analyzer.get_currently_booked_day("2020-10-26"))
    # print(analyzer.last_actualized())
