import sys
import pandas as pd

fields = ["Summary", "Priority"]
data = pd.read_csv(str(sys.argv[1]), usecols=fields)
data.to_csv(str(sys.argv[2]), index=True)
