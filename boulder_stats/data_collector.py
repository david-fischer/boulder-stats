"""Implements DataCollector class."""
from time import sleep

import attr
import bs4
import pandas as pd
from selenium import webdriver
from selenium.webdriver.remote.command import Command

from .utils import is_future, is_open
from .paths import HDF_PATH


def visitor_df(html_source, date, max_slots=18):
    """Return dataframe with booked entries per time-slot for a given date."""
    date_str = date.strftime("%Y-%m-%d")
    bs = bs4.BeautifulSoup(html_source, "lxml")
    time_rows = bs.select("#offerTimes tr")
    df = pd.DataFrame(
        index=pd.date_range(
            start=f"{date_str} 09:00", end=f"{date_str} 23:00", freq="0.5H"
        ),
        columns=["visitors"],
        dtype=int,
    )
    for row in time_rows:
        try:
            time_cell, number_people_cell = row.select("td")[:2]
            time = time_cell.text[:5]
            number_people = int(number_people_cell.text.split(" ")[0])
            df["visitors"][f"{date_str} {time}"] = max_slots - number_people
        except ValueError:
            pass
    for i, isnull in df["visitors"].isnull().items():
        if isnull:
            if not is_open(i):
                df["visitors"][i] = 0
            elif not is_future(i):
                # df["visitors"][i] = 0
                pass
            else:
                df["visitors"][i] = max_slots
    return df


@attr.s(auto_attribs=True)
class DataCollector:
    """Collect data from :attr:`url` and save it as hdf-file."""

    url: str = "https://187.webclimber.de/de/booking/offer/dein-slot"
    browser: webdriver.Firefox = None
    num_retries: int = 25
    retry_wait_time: float = 1
    max_visitors: int = 18
    hdf_path: str = HDF_PATH
    hdf_key: str = "raw"

    @staticmethod
    def today():
        """Return date of today."""
        return pd.Timestamp.today()

    def open(self):
        """Open selenium browser at :attr:`url`."""
        self.browser = webdriver.Firefox()
        self.browser.get(self.url)

    def browser_is_open(self):
        """Return bool indicating weather :attr:`browser` is open."""
        try:
            self.browser.execute(Command.STATUS)
            return True
        except:  # pylint: disable=bare-except
            return False

    def close(self):
        """Close :attr:`browser`."""
        self.browser.quit()

    def set_date(self, date):
        """Use jquery to change date on website to display the booked slots."""
        date_str = date.strftime("%d/%m/%Y")
        self.browser.execute_script(
            f"$('#bookingCalendar').datepicker('setDate', '{date_str}');"
        )

    def is_loaded(self):
        """Check if the booked data is already loaded."""
        return bool(self.browser.find_elements_by_css_selector("#offerTimes tr"))

    def get_html(self, date):
        """Get html-source for given date.

        Wait long enough to make sure, that the necessary data is loaded.
        """
        date = date or self.today()
        self.set_date(date)
        for _ in range(self.num_retries):
            if self.is_loaded():
                return self.browser.page_source
            sleep(self.retry_wait_time)
        return None

    def get_df(self, dates):
        """Return concatenated df with booking values for given dates."""
        df_list = [
            visitor_df(self.get_html(date), date, self.max_visitors) for date in dates
        ]
        return pd.concat(df_list)

    def get_next_days_df(self, n):
        """Use :meth:`get_df` to obtain the dataframe for the next ``n`` days."""
        dates = pd.date_range(self.today(), periods=n, freq="1D")
        return self.get_df(dates)

    def save_df(self, df):
        """Save the dataframe ``df`` with current timestamp as multi-index to hdf-file."""
        df_with_timestamp = pd.concat([df], keys=[pd.Timestamp.now()])
        df_with_timestamp.to_hdf(self.hdf_path, key=self.hdf_key, mode="a", append=True)

    def collect(self, n=7):
        """Main-function. Collect and save data."""
        if not self.browser_is_open():
            self.open()
        df = self.get_next_days_df(n)
        self.save_df(df)
        self.close()

    def read_df_from_hdf(self):
        """Load and return dataframe from hdf file."""
        return pd.read_hdf(self.hdf_path, self.hdf_key)
