# Blip Report Requisitor

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

# gets the report
report = requisitor.getCustomReport('/event-track/some%20event', today, today)

# show the report
print(dumps(report, ident=4))
```
