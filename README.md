<h1 align="center">boulder-stats</h1>

## 🚧 Setup

### Installation

* Set up a Telegram-Bot. #TODO: links and instructions
* pip install ...
* boulder_stats setup -t <TOKEN> #TODO
* boulder_stats get_unlock_pw #TODO
* add bot to conversation
* /unlock <UNLOCK_PW>

Now the bot responds to commands in this chat.

```

```

## 🔧 Usage

Usage example:

```

```

<!-- jinja-block help
Help text:

```
> boulder_stats -h

{{ execute_command("./boulder_stats/cli.py -h | exit") }}

```
jinja-block help-->
<!-- jinja-out help start-->
Help text:

```
> boulder_stats -h

INFO: Showing help with the command 'cli.py -- --help'.

NAME
    cli.py

SYNOPSIS
    cli.py COMMAND

COMMANDS
    COMMAND is one of the following:

     start_bot
       Start bot.

     collect_data
       Use scheduler to periodically collect data.


```
<!-- jinja-out help end-->



## 🎯 Troubleshooting

*


## 📦 Dependencies
<!-- jinja-block deps
{{ "\n".join(dep_strings) }}
jinja-block deps-->
<!-- jinja-out deps start-->
 * [apscheduler](https://github.com/agronholm/apscheduler) - In-process task scheduler with Cron-like capabilities
 * [attrs](https://www.attrs.org/) - Classes Without Boilerplate
 * [beautifulsoup4](http://www.crummy.com/software/BeautifulSoup/bs4/) - Screen-scraping library
 * [Fire](https://github.com/google/python-fire) - A library for automatically generating command line interfaces.
 * [jinja2](https://palletsprojects.com/p/jinja/) - A very fast and expressive template engine.
 * [matplotlib](https://matplotlib.org) - Python plotting package
 * [mechanicalsoup](https://mechanicalsoup.readthedocs.io/) - A Python library for automating interaction with websites
 * [numpy](https://www.numpy.org) - NumPy is the fundamental package for array computing with Python.
 * [pandas](https://pandas.pydata.org) - Powerful data structures for data analysis, time series, and statistics
 * [requests](https://requests.readthedocs.io) - Python HTTP for Humans.
 * [selenium](https://github.com/SeleniumHQ/selenium/) - Python bindings for Selenium
 * [setuptools](https://github.com/pypa/setuptools) - Easily download, build, install, upgrade, and uninstall Python packages
<!-- jinja-out deps end-->
