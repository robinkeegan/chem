import matplotlib.pyplot as plt
import numpy as np
plt.style.use('seaborn-white')


def chemical_properties():
    '''
    A database function which contains chemical values
    '''
    names = np.array(['Ca', 'Mg', 'Na', 'K', 'HCO3', 'CO3', 'Cl', 'SO4'])
    valance = np.array([2, 2, 1, 1, -1, -2, -1, -2])
    mass = np.array([
        40.078, 24.305, 22.989769, 39.0983, 61.0168, 60.01, 35.453, 96.06
    ])
    return names, valance, mass


def output(figure, show, save, fname):
    '''
    To save, show, or return plot object.

    :param figure: The figure object.
    :param show: Boolean to show the plot default is True.
    :param save: Boolean to save the plot default is False.
    :param fname: File name to save the plot default is None.
    :returns: Either  ave, show, or return plot object.
    '''
    if show is True and save is False:
        plt.show()
    elif save is True:
        plt.savefig(fname)
    elif show is False and save is False:
        return figure
