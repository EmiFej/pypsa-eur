# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: : 2023 The PyPSA-Eur Authors
#
# SPDX-License-Identifier: MIT
"""
Retrieve monthly fuel prices from Destatis.
"""

import logging

import pandas as pd

logger = logging.getLogger(__name__)

from pathlib import Path

from _helpers import configure_logging, set_scenario_config

if __name__ == "__main__":
    if "snakemake" not in globals():
        from _helpers import mock_snakemake

        snakemake = mock_snakemake("retrieve_eletricity_demand")
        rootpath = ".."
    else:
        rootpath = "."
    configure_logging(snakemake)
    set_scenario_config(snakemake)

    versions = ["2019-06-05", "2020-10-06"]
    url = "https://data.open-power-system-data.org/time_series/{version}/time_series_60min_singleindex.csv"

    df1, df2 = [
        pd.read_csv(url.format(version=version), index_col=0) for version in versions
    ]
    res = pd.concat([df1, df2[df2.index > df1.index[-1]]], join="inner")
    res.to_csv(snakemake.output[0])
