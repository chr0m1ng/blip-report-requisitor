# Blip Report Requisitor
[![PyPI version](https://badge.fury.io/py/blip-report-requisitor.svg)](https://badge.fury.io/py/blip-report-requisitor)
![PyPI - Downloads](https://img.shields.io/pypi/dm/blip-report-requisitor)

Wrapper to get blip reports information easily

---

## Installation

```
pip install blip-report-requisitor
```

or

```
pipenv install blip-report-requisitor
```

---

## Usage

```python
from blip_report_requisitor import Requisitor
from datetime import datetime
from json import dumps

# Initialize the requisitor
requisitor = Requisitor('ACCESS_KEY')

# today reports
today = datetime.now()

# get report of some category
report = requisitor.getCustomReport('Some Category', today, today)
print(dumps(report, indent=4))

# get all tracking categories
categories = requisitor.getAllCategories()
print(dumps(categories, indent=4))

# get all reports of all categories
report = requisitor.getAllReportsOfAllCategories(today, today)
print(dumps(report, indent=4))

# get the tickets
tickets = requisitor.getTickets(today, today)
print(dumps(tickets, indent=4))

# get the MAU
Mau = requisitor.getMau(today, today)
print(Mau)

# get MAU since creation
Mau = requisitor.getAllMau()
print(Mau)

# get bot configuration
bot_config = requisitor.getBotConfiguration()
print(dumps(bot_config, indent=4))
```
