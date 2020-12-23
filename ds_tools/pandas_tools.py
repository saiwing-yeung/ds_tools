import inspect
import re

import numpy as np
import pandas as pd


# Highlight functions

def isnull(x):
    return pd.isna(x) or np.isnan(x)


def iszero(x):
    return not pd.isna(x) and not np.isnan(x) and x == 0


def contains_text(x, pat):
    return np.array(re.search(pat, str(x)))


def greater_than(x, threshold):
    return 1 if (not pd.isna(x) and x >= threshold) else 0


def less_than(x, threshold):
    return 1 if (not pd.isna(x) and x <= threshold) else 0


def equal_value(x, y):
    return 1 if (not pd.isna(x) and not pd.isna(y) and x == y) else 0


def gen_highlight_style(df, columns, filter_func, threshold=None, bg_color='#fd0'):
    df_to_highlight = pd.Series(data=False, index=df.index)
    if threshold is None:
        df_to_highlight[columns] = filter_func(df.loc[columns])
    else:
        df_to_highlight[columns] = filter_func(df.loc[columns], threshold)
    return [f'background-color: {bg_color}' if df_to_highlight.any() else '' for v in df_to_highlight]


def generate_highlight_func(func):
    sig = inspect.signature(func)
    num_args = len(sig.parameters)
    assert num_args in [1, 2]

    def highlight_func(df, columns, threshold=None, bg_color='#fd0'):
        if num_args == 1:
            return df.style.apply(gen_highlight_style, columns=columns, filter_func=func, bg_color=bg_color, axis=1)
        else:  # 2
            return df.style.apply(gen_highlight_style, columns=columns, threshold=threshold, filter_func=func, bg_color=bg_color, axis=1)
    return highlight_func


highlight_null = generate_highlight_func(isnull)
highlight_zero = generate_highlight_func(iszero)
highlight_contains = generate_highlight_func(contains_text)
highlight_gt = generate_highlight_func(greater_than)
highlight_lt = generate_highlight_func(less_than)
highlight_eqv = generate_highlight_func(equal_value)
