# Copyright (c) 2025 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import AutoLocator, AutoMinorLocator


def bar_plot(
    xdata,
    ydata,
    xlabel=None,
    ylabel=None,
    title=None,
    figsize=(10, 5),
    dpi=300,
    filename=None,
):
    """Helper function for creating IIM plots."""
    _, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.bar(xdata, ydata)
    ax.yaxis.grid(color='gray', linestyle='dashed')
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    plt.xticks(rotation=90)

    if filename:
        plt.savefig(filename, dpi=dpi, bbox_inches="tight")


def grouped_bar_plot(
    xtick_labels,
    data,
    xlabel=None,
    ylabel=None,
    legend=None,
    title=None,
    bar_width=0.4,
    figsize=(10, 5),
    dpi=300,
    filename=None,
):
    """Helper function for creating grouped IIM bar plots."""
    _, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.yaxis.grid(color='gray', linestyle='dashed')

    x_pos = np.arange(len(xtick_labels))

    # Loop over data:
    for i, (group, values) in enumerate(data.items()):
        pos = x_pos + (i * bar_width)
        ax.bar(pos, values, width=bar_width, label=group)

    ax.set_xticks(x_pos + ((len(data) - 1) / 2) * bar_width)
    ax.set_xticklabels(xtick_labels)
    plt.xticks(rotation=90)

    ax.legend(legend)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title)

    if filename:
        plt.savefig(filename, dpi=dpi, bbox_inches="tight")


def plot_dynamic(
    data,
    ylim=None,
    yscale="linear",
    xlabel="Time / hours",
    ylabel="Inoperability",
    title=None,
    figsize=(9, 5),
    dpi=300,
    filename=None,
):
    """Helper function for plotting dynamic IIM data."""
    labels = data.columns[1:]
    t_data = data.to_numpy()[:, 0]
    q_data = data.to_numpy()[:, 1:]

    _, ax = plt.subplots(figsize=figsize, dpi=dpi)
    colors = plt.cm.nipy_spectral(np.linspace(0, 1, len(labels)))
    ax.set_prop_cycle("color", colors)

    for j in range(len(labels)):
        ax.plot(t_data, q_data[:, j], label=labels[j], linestyle="-", linewidth=2)

    if ylim:
        ax.set_ylim(ylim)
    plt.yscale(yscale)

    ax.yaxis.grid(color='gray', linestyle='dashed')

    ax.xaxis.set_major_locator(AutoLocator())
    ax.xaxis.set_minor_locator(AutoMinorLocator())

    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=5)

    if filename:
        plt.savefig(filename, dpi=dpi, bbox_inches="tight")


def plot_heatmap(
    df,
    vmin,
    vmax,
    xlabel=None,
    ylabel=None,
    title=None,
    cbar_label="Impact",
    dpi=300,
    filename=None,
):
    """Helper function for creating heatmaps."""
    data = df.pivot(index="infra_i", columns="infra_j", values="impact")
    _, ax = plt.subplots(dpi=dpi)
    sns.heatmap(
        data, linewidth=0.5, vmin=vmin, vmax=vmax, cbar_kws={"label": cbar_label}, ax=ax
    )
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    if filename:
        plt.savefig(filename, dpi=dpi, bbox_inches="tight")
