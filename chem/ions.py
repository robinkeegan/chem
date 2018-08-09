import matplotlib.pyplot as plt
import numpy as np


def chemical_properties():
    '''
    A database function which contains chemical values
    '''
    names = np.array(['Ca', 'Mg', 'Na', 'K', 'HCO3', 'CO3', 'Cl', 'SO4'])
    valance = np.array([2, 2, 1, 1, -1, -2, -1, -2])
    mass = np.array([40.078, 24.305, 22.989769, 39.0983, 61.0168, 60.01, 35.453, 96.06])
    return names, valance, mass


def meq(array):
    '''
    Convert from milligrams per litre to milli-equivilents per litre.

    Args:

    :param array: A one dimensional array or two dimensional pandas dataframe \
    containing in mg/L in the order of 'Ca', 'Mg', 'Na', 'K', 'HCO3', 'CO3', \
    'Cl', 'SO4'
    :return: The input array in meq/L
    '''
    def process_1d(array):
        name, valance, mass = chemical_properties()
        array / valance * mass

    ndims = len(array.shape)
    if ndims == 2:
        return array.apply(process_1d, axis=1)
    if ndims == 1:
        return process_1d(array)


def schoeller(array, labels=None, show=True, save=False, fname=None, figsize=(4, 6), cmap='tab20'):
    '''
    Create a Schoeller diagram.

    Args:

    :param array: A one dimensional array or pandas dataframe containing in \
    meq/L in the order of 'Ca', 'Mg', 'Na', 'K', 'HCO3', 'CO3', 'Cl', 'SO4'
    :param labels: If a pandas datframe include labels for each row as an array.
    :param show: If True shows plot else returns plot object.
    :param Save: save the plot default is False
    :param fname: filename default is none
    :param figsize: figure size tuple default (4, 6)
    :param cmap: the colourmap default is "tab 20"
    :return: A schoeller digram of the data
    '''
    plt.figure(figsize=(x, y))
    name, valance, mass = chemical_properties()

    def plot(array_1D, name, colour):
        plt.plot(name, array_1D, c=colour, marker='o')

    def output(show, save, fname):
        if show == True and save == False:
            plt.show()
        elif save == True:
            plt.savefig(fname)

    ndims = len(array.shape)

    if ndims == 1:
        plot(array, name, 'k')
        output(show, save, fname)

    if ndims == 2:
        hsv = plt.get_cmap(cmap)
        n = len(array)
        colors = hsv(np.linspace(0, 1.0, n))
        for i in range(n):
            plot(array.iloc[i, :], name, colors[i])
        output(show, save, fname)
