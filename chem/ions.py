import matplotlib.pyplot as plt
import numpy as np
import module_io
plt.style.use('seaborn-white')


def meq(array):
    '''
    Convert from milligrams per litre to milli-equivilents per litre.

    Args:

    :param array: A one dimensional array or two dimensional pandas dataframe \
    containing in mg/L in the order of 'Ca', 'Mg', 'Na', 'K', 'HCO3', 'CO3', \
    'Cl', 'SO4'
    :return: The input array in meq/L
    '''
    name, valance, mass = module_io.chemical_properties()

    def process_1d(array, valance, mass):
        return array / mass * valance

    ndims = len(array.shape)
    if ndims == 2:
        return array.apply(process_1d, axis=1, args=(valance, mass))
    if ndims == 1:
        return process_1d(array)


def mM(array):
    '''
    Convert from milligrams per litre to milli-moles per litre.

    Args:

    :param array: A one dimensional array or two dimensional pandas dataframe \
    containing in mg/L in the order of 'Ca', 'Mg', 'Na', 'K', 'HCO3', 'CO3', \
    'Cl', 'SO4'
    :return: The input array in mM/L
    '''
    name, valance, mass = module_io.chemical_properties()

    def process_1d(array, mass):
        return array / mass

    ndims = len(array.shape)
    if ndims == 2:
        return array.apply(process_1d, axis=1, args=(mass,))
    if ndims == 1:
        return process_1d(array)


def schoeller(array, labels=None, show=True, save=False, fname=None, figsize=(6, 4), cmap='tab20'):
    '''
    Create a Schoeller diagram.

    Args:

    :param array: A one dimensional array or pandas dataframe containing in \
    mM/L in the order of 'Ca', 'Mg', 'Na', 'K', 'HCO3', 'CO3', 'Cl', 'SO4'
    :param labels: If a pandas datframe include labels for each row as an array.
    :param show: If True shows plot else returns plot object.
    :param save: Save the plot default is False
    :param fname: Filename default is none
    :param figsize: Figure size tuple default (6, 4)
    :param cmap: The colourmap default is "tab 20"
    :return: A schoeller digram of the data
    '''
    hsv = plt.get_cmap("tab20")
    colors = hsv(np.linspace(0, 1.0, 20))
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
        colors = hsv(np.linspace(0, 1.0, n))
        if labels is not None:
            for i in range(n):
                plot(array.iloc[i, :], name, colors[i], label=labels[i])
            plt.legend()
            module_io.output(f, show, save, fname)
        elif labels == None:
            for i in range(n):
                plot(array.iloc[i, :], name, colors[i], label="")
            module_io.output(f, show, save, fname)


def chloride_vs_stable_isotopes(chloride, d18O, d2H, show=True, save=False, fname=None, figsize=(8, 3)):
    '''
    Plot stable isotopes vs chloride.

    Args:

    :param chloride: A one dimensional array containing chloride in mM/L
    :param d18O: A one dimensional array containing d18O in ‰ VSMOW.
    :param d2H: A one dimensional array containing d2H in ‰ VSMOW.
    :param show: If True shows plot else returns plot object.
    :param save: Save the plot default is False
    :param fname: Filename default is none
    :param figsize: Figure size tuple default (8, 3)
    :return: A plot of stable isotopes vs chloride.
    '''
    hsv = plt.get_cmap("tab20")
    colors = hsv(np.linspace(0, 1.0, 20))
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=False, figsize=figsize)
    ax1.scatter(chloride, d2H, c=colors[0])
    ax1.set_ylabel("$\delta 2 H \ (‰  \ VSMOW)$")
    ax1.set_xlabel("Cl (mM/L)")
    ax2.scatter(chloride, d18O, c=colors[2])
    ax2.set_ylabel("$\delta 18O \ (‰  \ VSMOW)$")
    ax2.set_xlabel("Cl (mM/L)")
    plt.tight_layout()
    module_io.output(f, show, save, fname)


def chloride_ion_ratios(array, show=True, save=False, fname=None, figsize=(6, 6)):
    '''
    Plot chloride vs major ion ratios.

    Args:

    :param array: A one or two dimensional array containing in mM/L in the order of \
    'Ca', 'Mg', 'Na', 'K', 'HCO3', 'CO3', 'Cl', 'SO4'.
    :param show: If True shows plot else returns plot object.
    :param save: Save the plot default is False
    :param fname: Filename default is none
    :param figsize: Figure size tuple default (8, 3)
    :return: A plot of chloride vs major ion ratios.
    '''
    ndims = len(array.shape)
    if ndims == 1:
        array = np.concatenate((array, array)).reshape(2, 8)
    hsv = plt.get_cmap("tab20")
    colors = hsv(np.linspace(0, 1.0, 20))
    f, axes = plt.subplots(3, 2, sharex=True, figsize=(6, 6))
    axes[0, 0].scatter(array[:, 6], array[:, 0] / array[:, 6], c=colors[0])
    axes[0, 0].set_ylabel("Ca/Cl")
    axes[1, 0].scatter(array[:, 6], array[:, 1] / array[:, 6], c=colors[1])
    axes[1, 0].set_ylabel("Mg/Cl")
    axes[2, 0].scatter(array[:, 6], array[:, 2] / array[:, 6], c=colors[2])
    axes[2, 0].set_ylabel("Na/Cl")
    axes[0, 1].scatter(array[:, 6], array[:, 3] / array[:, 6], c=colors[3])
    axes[0, 1].set_ylabel("K/Cl")
    axes[1, 1].scatter(array[:, 6], array[:, 4] / array[:, 6], c=colors[4])
    axes[1, 1].set_ylabel("HCO3/Cl")
    axes[2, 1].scatter(array[:, 6], array[:, 7] / array[:, 6], c=colors[5])
    axes[2, 1].set_ylabel("SO4/Cl")
    axes[2, 0].set_xlabel("Cl (mM/L)")
    axes[2, 1].set_xlabel("Cl (mM/L)")
    plt.tight_layout()
    module_io.output(f, show, save, fname)
