"""Schedule periodic data collection."""

from apscheduler.schedulers.blocking import BlockingScheduler

from boulder_stats.data_collector import DataCollector


def start_data_collection():
    """Use scheduler to periodically collect data."""
    scheduler = BlockingScheduler()
    data_collector = DataCollector()
    scheduler.add_job(data_collector.collect, trigger="cron", minute="15,45")
    scheduler.start()


if __name__ == "__main__":
    start_data_collection()
