import matplotlib.pyplot as plt
import numpy as np
from chem import module_io
plt.style.use('seaborn-white')


def eb(array, mg=True):
    r"""
    Conduct an electrical balance.

    Args:

    :param array: A one dimensional array or two dimensional pandas dataframe \
    containing ions in mg/L or meq/L in the order of 'Ca', 'Mg', 'Na', 'K', \
    'HCO3', 'CO3', 'Cl', 'SO4'.
    :param mg: If units are mg the meq function is applied (default is True).
    :return: The electrical balance of each sample.
    """
    if mg is True:
        array = meq(array)

    def eb1d(array):
        sum_cat = np.sum(array[0:4])
        sum_an = np.sum(array[4:])
        return (sum_cat + sum_an) / (sum_cat - sum_an) * 100

    ndims = len(array.shape)
    if ndims == 2:
        return array.apply(eb1d, axis=1)
    if ndims == 1:
        return eb1d(array)


def meq(array):
    r"""
    Convert from milligrams per litre to milli-equivilents per litre.

    Args:

    :param array: A one dimensional array or two dimensional pandas dataframe \
    containing ions in mg/L in the order of 'Ca', 'Mg', 'Na', 'K', 'HCO3', \
    'CO3', 'Cl', 'SO4'.
    :return: The input array in meq/Ls
    """
    name, valance, mass = module_io.chemical_properties()

    def process_1d(array, valance, mass):
        return array / mass * valance

    ndims = len(array.shape)
    if ndims == 2:
        return array.apply(process_1d, axis=1, args=(valance, mass))
    if ndims == 1:
        return process_1d(array)


def mM(array):
    r"""
    Convert from milligrams per litre to milli-moles per litre.

    Args:

    :param array: A one dimensional array or two dimensional pandas dataframe \
    containing in mg/L in the order of 'Ca', 'Mg', 'Na', 'K', 'HCO3', 'CO3', \
    'Cl', 'SO4'
    :return: The input array in mM/L
    """
    name, valance, mass = module_io.chemical_properties()

    def process_1d(array, mass):
        return array / mass
    ndims = len(array.shape)
    if ndims == 2:
        return array.apply(process_1d, axis=1, args=(mass,))
    if ndims == 1:
        return process_1d(array)


def schoeller(
    array, labels=None, show=True, save=False, fname=None,
    figsize=(6, 4), cmap='tab20'
):
    r"""
    Create a Schoeller diagram.

    Args:

    :param array: A one dimensional array or pandas dataframe containing in \
    mM/L in the order of 'Ca', 'Mg', 'Na', 'K', 'HCO3', 'CO3', 'Cl', 'SO4'
    :param labels: If a pandas datframe include labels for each row as an \
    array.
    :param show: If True shows plot else returns plot object.
    :param save: Save the plot default is False
    :param fname: Filename default is none
    :param figsize: Figure size tuple default (6, 4)
    :param cmap: The colourmap default is "tab 20"
    :return: A schoeller digram of the data
    """
    hsv = plt.get_cmap("tab20")
    colors = hsv(np.linspace(0, 1.0, 10))
    f = plt.figure(figsize=figsize)
    plt.ylabel("Concentration (mM/L)")
    name, valance, mass = module_io.chemical_properties()

    def plot(array_1D, name, colour, label=""):
        plt.plot(name, array_1D, c=colour, marker='o', label=label)

    ndims = len(array.shape)

    if ndims == 1:
        plot(array, name, colors[0])
        module_io.output(f, show, save, fname)

    if ndims == 2:
        hsv = plt.get_cmap(cmap)
        n = len(array)
        if n < 10:
            colors = hsv(np.linspace(0, 1, 10))
        colors = hsv(np.linspace(0, 1.0, n))
        if labels is not None:
            for i in range(n):
                plot(array.iloc[i, :], name, colors[i], label=labels[i])
            plt.legend()
            module_io.output(f, show, save, fname)
        elif labels is None:
            for i in range(n):
                plot(array.iloc[i, :], name, colors[i], label="")
            module_io.output(f, show, save, fname)


def chloride_vs_stable_isotopes(
    chloride, d18O, d2H, groupby=False, labels=None,
    show=True, save=False, fname=None, figsize=(8, 3)
):
    r"""
    Plot stable isotopes vs chloride.

    Args:

    :param chloride: A one dimensional array containing chloride in mM/L
    :param d18O: A one dimensional array containing d18O in VSMOW.
    :param d2H: A one dimensional array containing d2H in VSMOW.
    :param groupby: If the data is catagorical change groupby to True default \
    is False. Note is groupby is True labels must be defined.
    :param labels: A one dimensional array of labels for each sample.
    :param show: If True shows plot else returns plot object.
    :param save: Save the plot default is False
    :param fname: Filename default is none
    :param figsize: Figure size tuple default (8, 3)
    :return: A plot of stable isotopes vs chloride.
    """
    hsv = plt.get_cmap("tab20")
    colors = hsv(np.linspace(0, 1.0, 20))
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=False, figsize=figsize)

    def plot(chloride, d2H, d18O, color, label=""):
        ax1.scatter(chloride, d2H, c=color, label=label)
        ax1.set_ylabel("$\delta 2 H$")
        ax1.set_xlabel("Cl (mM/L)")
        ax2.scatter(chloride, d18O, c=color, label=label)
        ax2.set_ylabel("$\delta 18O$")
        ax2.set_xlabel("Cl (mM/L)")

    if groupby is False:
        plot(chloride, d2H, d18O, colors[0])
    elif groupby is True:
        groups = np.unique(labels)
        colors = hsv(np.linspace(0, 1.0, len(groups)))
        for i in range(len(groups)):
            mask = labels == groups[i]
            plot(
                chloride[mask], d2H[mask], d18O[mask], colors[i],
                label=str(groups[i])
            )
        ax1.legend()
        ax2.legend()

    plt.tight_layout()
    module_io.output(f, show, save, fname)


def chloride_ion_ratios(
    array, groupby=False, labels=None, show=True,
    save=False, fname=None, figsize=(8, 6)
):
    r"""
    Plot chloride vs major ion ratios.

    Args:

    :param array: A one or two dimensional array containing in mM/L in the \
    order of 'Ca', 'Mg', 'Na', 'K', 'HCO3', 'CO3', 'Cl', 'SO4'.
    :param groupby: If the data is catagorical change groupby to True default \
    is False. Note is groupby is True labels must be defined.
    :param labels: A one dimensional array of labels for each sample.
    :param show: If True shows plot else returns plot object.
    :param save: Save the plot default is False
    :param fname: Filename default is none
    :param figsize: Figure size tuple default (8, 3)
    :return: A plot of chloride vs major ion ratios.
    """
    ndims = len(array.shape)
    if ndims == 1:
        array = np.concatenate((array, array)).reshape(2, 8)
    hsv = plt.get_cmap("tab20")
    colors = hsv(np.linspace(0, 1.0, 20))
    f, axes = plt.subplots(3, 2, sharex=True, figsize=figsize)

    def plot(array, color, label=''):
        axes[0, 0].scatter(array[:, 6], array[:, 0] / array[:, 6], c=color)
        axes[0, 0].set_ylabel("Ca/Cl")
        axes[1, 0].scatter(array[:, 6], array[:, 1] / array[:, 6], c=color)
        axes[1, 0].set_ylabel("Mg/Cl")
        axes[2, 0].scatter(array[:, 6], array[:, 2] / array[:, 6], c=color)
        axes[2, 0].set_ylabel("Na/Cl")
        axes[0, 1].scatter(array[:, 6], array[:, 3] / array[:, 6], c=color)
        axes[0, 1].set_ylabel("K/Cl")
        axes[1, 1].scatter(
            array[:, 6], array[:, 4] / array[:, 6], c=color,
            label=label
        )
        axes[1, 1].set_ylabel("HCO3/Cl")
        axes[2, 1].scatter(array[:, 6], array[:, 7] / array[:, 6], c=color)
        axes[2, 1].set_ylabel("SO4/Cl")
        axes[2, 0].set_xlabel("Cl (mM/L)")
        axes[2, 1].set_xlabel("Cl (mM/L)")

    if groupby is False:
        plot(array, colors[0])
    elif groupby is True:
        groups = np.unique(labels)
        colors = hsv(np.linspace(0, 1.0, len(groups)))
        for i in range(len(groups)):
            mask = labels == groups[i]
            plot(array[mask], colors[i], label=str(groups[i]))
        axes[1, 1].legend(
            loc='center left', bbox_to_anchor=(1, 0.5), title="Legend"
        )

    plt.tight_layout()
    module_io.output(f, show, save, fname)
