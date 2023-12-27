import os
from abc import ABC

import pandas as pd

from benchy.testbench import *
from benchy.plugins.plugin import Plugin


COL_PROBLEM = 'problem'
COL_RUN = 'run'
COL_BEST = 'best'
COL_TIME = 'time'


class CsvPlugin(Plugin, ABC):

    def __init__(self, out_dir: str):
        self._out_dir = out_dir
        self._dfs: dict[str, pd.DataFrame] = dict()

    def testbench_before(self, testbench: Testbench):
        pass

    def testbench_after(self, testbench: Testbench):
        pass

    def problem_before(self, ctx: ProblemContext):
        pass

    def problem_after(self, ctx: ProblemContext):
        pass

    def harness_before(self, ctx: HarnessContext):
        harness_name = ctx.harness().name()
        columns = self._column_names(ctx)
        self._dfs[harness_name] = pd.DataFrame(columns=columns)

    def _column_names(self, ctx):
        parameter_names = ctx.harness().parameter_names()
        return [COL_PROBLEM, *parameter_names, COL_RUN, COL_BEST, COL_TIME]

    def harness_after(self, ctx: HarnessContext):
        pass

    def instance_before(self, ctx: BeforeInstanceContext):
        pass

    def instance_after(self, ctx: AfterInstanceContext):
        harness_name = ctx.harness().name()
        self._append_result(ctx)
        filename = os.path.join(self._out_dir, f"{harness_name}.csv")
        self._dfs[harness_name].to_csv(filename)

    def _append_result(self, ctx):
        harness_name = ctx.harness().name()
        old_df = self._dfs[harness_name]
        row = self._create_row(ctx)
        new_df = pd.concat([old_df, row], ignore_index=True)
        self._dfs[harness_name] = new_df

    def _create_row(self, ctx):
        row = ctx.instance().args().copy()
        row[COL_PROBLEM] = ctx.problem().name()
        row[COL_RUN] = ctx.run()
        row[COL_BEST] = ctx.solution().value()
        row[COL_TIME] = f"{ctx.elapsed_time() * 1000:.0f}"
        return pd.DataFrame.from_records([row])
