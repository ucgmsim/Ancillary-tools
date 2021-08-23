from collections import Counter
import os
from pathlib import Path

from mpi4py import MPI
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

from qcore import geo
from getCPTdata import getCPTdata
from computeVs import Vs_McGann
from computeVsz import compute_vsz_from_vs
from computeVs30 import vsz_to_vs30

from loc_filter import locs_multiple_records

def log_error(skipped_fp, cpt_name, error):
    skipped_fp.write(f"{cpt_name} - {error}\n")


def count_digits(arr):
    stringified = str(arr).replace("0", "").replace(".", "")
    return Counter(stringified)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
hostname = MPI.Get_processor_name()
master = 0
is_master = not rank

out_dir = Path("/home/seb56/scratch/syncthing/vs30/cpt2vs30")
plot_dir = out_dir / "validation_plots"

cpt_df = pd.read_csv("/isilon/vs30/input_data/TTGD_CPT_sCPT_Download_2020-09-11/Metadata/cpt_locations_20200909.csv", sep=",")

cpt_root_path = Path("/home/seb56/scratch/syncthing/vs30/cpt2vs30/CPT_Depth_Profile_CSVs")

results = {}

skipped_fp = open(out_dir / "skipped_cpts" / f"skipped_cpts_{rank}", "w")
dup_locs = []

if is_master:
    dup_locs=locs_multiple_records()
    import functools,operator
    dup_locs = functools.reduce(operator.iconcat, list(dup_locs.values()), [])



dup_locs = comm.bcast(dup_locs, root=0)
for row_n, cpt in cpt_df.iterrows():
    if row_n % size != rank:
        continue
    dir = f"{'Private' if cpt['TTGD Only'] else 'Public'}_{'sCPT' if cpt.InvestigationType == 'SCPT' else cpt.InvestigationType}"
    cpt_name = cpt.CombinedName
    fname = f"{cpt_name}.csv"
    print(f"rank: {rank} -- ", row_n, cpt_name)
    cpt_ffp = cpt_root_path / dir / fname

    if os.path.exists(cpt_ffp):
        try:
            (z, qc, fs, u2) = getCPTdata(cpt_ffp)
        except (ValueError, Exception) as e:
            log_error(skipped_fp, cpt_name, f"could not read file: {str(e)}")
            continue

        # duplicate location
        if cpt_name in dup_locs:
            log_error(skipped_fp, cpt_name, f"Duplicate location")
            continue

        # duplicate depth check
        u, c = np.unique(z, return_counts=True)
        if np.any([c > 1]):
            log_error(skipped_fp, cpt_name, f"Duplicate depth detected - invalid CPT")
            continue

        # Check for invalid negative readings
        if any(fs < -0.2) or any(qc < -0.2) or any(u2 < -0.2):
            log_error(skipped_fp, cpt_name, f"negative value - discarding")
            continue

        # Check for repeated digits
        if any(value > 3 for fs_value in fs for value in count_digits(fs_value).values()):
            log_error(skipped_fp, cpt_name, f"Repeated digit - investigating")
            continue

        max_depth = max(z)
        if max_depth < 5:
            log_error(skipped_fp, cpt_name, f"depth<5: {max_depth}")
            continue
        min_depth = min(z)
        z_span = max_depth - min_depth
        if z_span < 5:
            log_error(skipped_fp, cpt_name, f"depth range <5: {z_span}")
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
        vs30_result["Zmin"] = min_depth
        vs30_result["Zspan"] = z_span
        results[cpt_name] = vs30_result
        if row_n < 10:
            fig, ax = plt.subplots()
            ax.plot(fs, z)
            ax.invert_yaxis()
            ax.set_ylabel("Depth")
            ax.set_xlabel("fs")
            ax.grid()
            fig.savefig(plot_dir / f"{cpt_name}_fs.png")
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
            fig.savefig(plot_dir / f"{cpt_name}_Vs.png")
            plt.close(fig)
        elif row_n > 0:
            pass
        else:
            break
    else:
        log_error(skipped_fp, cpt_name, f"CPT file not found")

mpi_results = comm.gather(results, root=master)#
if is_master:
    print(mpi_results)

    master_results = {}
    for result_dict in mpi_results:
        master_results.update(result_dict)
    result_df = pd.DataFrame.from_dict(master_results, orient="index")
    result_df.to_csv(out_dir / "vs30_results.csv")

    ll = geo.wgs_nztm2000x(result_df[["NZTM_X", "NZTM_Y"]])
    result_df["lon"] = ll[:, 0]
    result_df["lat"] = ll[:, 1]

    result_df.plot.scatter("Vs30", "Vsz")
    fig = plt.gcf()
    fig.savefig(plot_dir / "vs30_vsz_scatter.png")
