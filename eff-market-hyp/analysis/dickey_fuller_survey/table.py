import pandas as pd
from pathlib import Path 
import seaborn as sns

def _color_red_or_green(val):
    if isinstance(val, float):
        color = 'red' if val < 0.05 else 'green'
        return 'color: %s' % color

adf_results = pd.read_pickle("./tables/adf_results.pickle")
adf_results.sort_values("adf_p_value",ascending=False, inplace=True, ignore_index=True)
cm = sns.color_palette("vlag", as_cmap=True)
s = adf_results.style.applymap(_color_red_or_green)
with open("./tables/adf_results.html", "w") as table_file:
    html = s.render()
    table_file.write(html)
