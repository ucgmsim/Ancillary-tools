import os
from pathlib import Path

import pandas as pd

from getCPTdata import getCPTdata

cpt_df = pd.read_csv("/isilon/vs30/input_data/TTGD_CPT_sCPT_Download_2020-09-11/Metadata/cpt_locations_20200909.csv", sep=",")

cpt_root_path = Path("/isilon/vs30/input_data/TTGD_CPT_sCPT_Download_2020-09-11/CPT_Depth_Profile_CSVs/")

for row_n, cpt in cpt_df.iterrows():
    dir = f"{'Private' if cpt['TTGD Only'] else 'Public'}_{cpt.InvestigationType}"
    fname = f"{cpt.CombinedName}.csv"
    cpt_ffp = cpt_root_path / dir / fname

    cpt_data = getCPTdata(cpt_ffp)
    input()