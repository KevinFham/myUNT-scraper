import numpy as np
import pandas as pd

raw = pd.read_csv('./ENG_course_catalog_database.csv')
# raw = raw.to_numpy()

uid = raw['ID'].unique()
raw = raw.set_index('ID')