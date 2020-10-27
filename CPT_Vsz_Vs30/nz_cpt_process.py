import os
from pathlib import Path

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

from getCPTdata import getCPTdata
from computeVs import Vs_McGann
from computeVsz import compute_vsz_from_vs
from computeVs30 import vsz_to_vs30

out_dir = Path("/home/jam335/scratch/vs30/cpt2vs30/")
plot_dir = out_dir / "validation_plots"

cpt_df = pd.read_csv("/isilon/vs30/input_data/TTGD_CPT_sCPT_Download_2020-09-11/Metadata/cpt_locations_20200909.csv", sep=",")

cpt_root_path = Path("/isilon/vs30/input_data/TTGD_CPT_sCPT_Download_2020-09-11/CPT_Depth_Profile_CSVs/")

results = {}

skipped_fp = open(out_dir / "skipped_cpts", "w")

for row_n, cpt in cpt_df.iterrows():
    dir = f"{'Private' if cpt['TTGD Only'] else 'Public'}_{'sCPT' if cpt.InvestigationType == 'SCPT' else cpt.InvestigationType}"
    fname = f"{cpt.CombinedName}.csv"
    print(row_n, cpt.CombinedName)
    cpt_ffp = cpt_root_path / dir / fname

    if os.path.exists(cpt_ffp):
        try:
            (z, qc, fs, u2) = getCPTdata(cpt_ffp)
        except (ValueError, Exception) as e:
            skipped_fp.write(f"{cpt.CombinedName} - could not read file: {str(e)}\n")
            continue

        max_depth = max(z)
        if max_depth < 5:
            skipped_fp.write(f"{cpt.CombinedName} - depth<5: {max_depth}\n")
            continue
        z_span = max_depth - min(z)
        if z_span < 5:
            skipped_fp.write(f"{cpt.CombinedName} - depth range <5: {z_span}\n")
            continue
        (z, Vs, Vs_SD) = Vs_McGann(z, qc, fs)
        Vsz, max_depth = compute_vsz_from_vs(Vs, z)
        vs30 = vsz_to_vs30(Vsz, z)

        vs30_result = {}
        vs30_result["NZTM_X"] = cpt.NZTM_X
        vs30_result["NZTM_Y"] = cpt.NZTM_Y
        vs30_result["Vsz"] = Vsz
        vs30_result["Vs30"] = vs30
        vs30_result["Zmax"] = max_depth
        vs30_result["Zspan"] = z_span
        results[cpt.CombinedName] = vs30_result

        if row_n < 10:
            fig, ax = plt.subplots()
            ax.plot(fs, z)
            ax.invert_yaxis()
            ax.set_ylabel("Depth")
            ax.set_xlabel("fs")
            ax.grid()
            fig.savefig(plot_dir / f"{cpt.CombinedName}_fs.png")
            plt.close(fig)

            fig, ax = plt.subplots()
            lowerVs = np.exp(np.log(Vs) - Vs_SD)
            upperVs = np.exp(np.log(Vs) + Vs_SD)
            ax.plot(Vs, z, "red")
            ax.plot(lowerVs, z, "r--", linewidth=0.5)
            ax.plot(upperVs, z, "r--", linewidth=0.5)
            ax.grid()
            ax.invert_yaxis()
            ax.set_ylabel("Depth")
            ax.set_xlabel("Vs (m/s)")
            ax.set_xlim(0, 600)
            fig.savefig(plot_dir / f"{cpt.CombinedName}_Vs.png")
            plt.close(fig)
        elif row_n < 10000:
            pass
        else:
            break
    else:
        skipped_fp.write(f"{cpt.CombinedName} - CPT file not found\n")


result_df = pd.DataFrame.from_dict(results, orient="index")
result_df.to_csv(out_dir / "vs30_results.csv")

result_df.plot.scatter("Vs30", "Vsz")
fig = plt.gcf()
fig.savefig(plot_dir / "vs30_vsz_scatter.png")
input()