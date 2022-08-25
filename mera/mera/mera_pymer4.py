from typing import List

import pandas as pd
import numpy as np
from pymer4.models import Lmer


def run_mera(
    residual_df: pd.DataFrame,
    ims: List[str],
    event_cname: str,
    site_cname: str,
    assume_biased: bool = True,
):
    """
    Runs mixed effects regression analysis for the given
    residual dataframe using pymer4 package

    Parameters
    ----------
    residual_df: dataframe
        Residual dataframe, has to contain all
        specified IMs (as columns) along with
         columns for event and site id
    ims: list of strings
        IMs for which to run to mixed effects
        regression analysis.

        Note: Has to be a list, can't be a numpy array!
    event_cname: string
        Name of the column that contains the event ids
    site_cname: string
        Name of the column that contains the site ids
    assume_biased: bool
        If true then the model fits a bias term, removing
        any model bias (wrt. given dataset)

        Recommended to have this enabled, otherwise any model
        bias (wrt. given dataset) will affect random effect
        terms.

    Returns
    -------
    event_res_df: dataframe
        Contains the random effect for each event (rows) and IM (columns)
    site_res_df: dataframe
        Contains the random effect for each site (rows) and IM (columns)
    me_res_df: dataframe
        Contains the leftover residuals for each record (rows) and IM (columns)
    bias_std_df: dataframe
        Contains bias, between-event sigma (tau), between-site sigma (phi_S2S),
        remaining residual sigma (phi_w) and total sigma (sigma) (columns)
        per IM (rows)
    """
    # Columns cannot have a '.' in them,
    # otherwise statsmodel fails
    ims = [cur_im.replace(".", "p") for cur_im in ims]
    residual_df.columns = [cur_col.replace(".", "p") for cur_col in residual_df.columns]

    # result dataframes
    event_res_df = pd.DataFrame(
        index=np.unique(residual_df[event_cname].values).astype(str), columns=ims
    )
    site_res_df = pd.DataFrame(
        index=np.unique(residual_df[site_cname].values).astype(str), columns=ims
    )
    rem_res_df = pd.DataFrame(index=residual_df.index.values, columns=ims)
    bias_std_df = pd.DataFrame(
        index=ims, columns=["bias", "tau", "phi_S2S", "phi_w", "sigma"]
    )

    for cur_ix, cur_im in enumerate(ims):
        print(f"Processing IM {cur_im}, {cur_ix + 1}/{len(ims)}")

        # Create and fit the model
        cur_columns = [cur_im] + [event_cname, site_cname]
        cur_model = Lmer(
            f"{cur_im} ~ {'1' if assume_biased else '0'} + (1|{event_cname}) + (1|{site_cname})",
            data=residual_df[cur_columns],
        )
        cur_model.fit(summary=False)

        # Get random effects
        event_res_df[cur_im] = (
            cur_model.ranef[0]
            if cur_model.ranef[0].size == event_res_df.shape[0]
            else cur_model.ranef[1]
        )
        site_res_df[cur_im] = (
            cur_model.ranef[0]
            if cur_model.ranef[0].size == site_res_df.shape[0]
            else cur_model.ranef[1]
        )
        rem_res_df[cur_im] = cur_model.residuals

        bias_std_df.loc[cur_im, "bias"] = cur_model.coefs.iloc[0, 0]

        bias_std_df.loc[cur_im, "tau"] = cur_model.ranef_var.loc[event_cname, "Std"]
        bias_std_df.loc[cur_im, "phi_S2S"] = cur_model.ranef_var.loc[site_cname, "Std"]
        bias_std_df.loc[cur_im, "phi_w"] = cur_model.ranef_var.loc["Residual", "Std"]

    # Compute total sigma
    bias_std_df["sigma"] = (
        bias_std_df["tau"] ** 2 + bias_std_df["phi_S2S"] ** 2 + bias_std_df["phi_w"] ** 2
    ) ** (1/2)

    return event_res_df, site_res_df, rem_res_df, bias_std_df
