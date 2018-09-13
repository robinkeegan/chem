import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from chem import module_io


def piper(
    array, alphalevel=1, color=True, show=True, save=False, fname=None,
    figsize=(4, 4)
):
    r"""
    Create a Piper plot using the code by Peeters, (2014).

    Args:

    :param array: A one or two dimensional array containing in mM/L in the \
    order of 'Ca', 'Mg', 'Na', 'K', 'HCO3', 'CO3', 'Cl', 'SO4'.
    :param alphalevel: transparency level of points. If 1, points are opaque
    :param color: boolean, use background coloring of Piper plot default True
    :param show: If True shows plot else returns plot object.
    :param save: Save the plot default is False
    :param fname: Filename default is none
    :param figsize: Figure size tuple default (8, 3)
    :return: Piperplot

    Code from https://github.com/inkenbrandt/Peeters_Piper/blob/master/peeter_\
    piper.py:

    Citation:

    @article {GWAT:GWAT12118,
    author = {Peeters, Luk},
    title = {A Background Color Scheme for Piper Plots to Spatially Visualize \
    Hydrochemical Patterns},
    journal = {Groundwater},
    volume = {52},
    number = {1},
    publisher = {Blackwell Publishing Ltd},
    issn = {1745-6584},
    url = {http://dx.doi.org/10.1111/gwat.12118},
    doi = {10.1111/gwat.12118},
    pages = {2--6},
    year = {2014},
    }
    """
    dat_piper = array
    ndims = len(dat_piper.shape)
    if ndims == 1:
        dat_piper = np.concatenate((dat_piper, dat_piper)).reshape(2, 8)

    def hsvtorgb(H, S, V):
        # conversion (from http://en.wikipedia.org/wiki/HSL_and_HSV)
        C = V*S
        Hs = H / (np.pi/3)
        X = C * (1 - np.abs(np.mod(Hs, 2.0 * np.ones_like(Hs)) - 1))
        N = np.zeros_like(H)
        # create empty RGB matrices
        R = np.zeros_like(H)
        B = np.zeros_like(H)
        G = np.zeros_like(H)
        # assign values
        h = np.floor(Hs)
        # h=0
        R[h == 0] = C[h == 0]
        G[h == 0] = X[h == 0]
        B[h == 0] = N[h == 0]
        # h=1
        R[h == 1] = X[h == 1]
        G[h == 1] = C[h == 1]
        B[h == 1] = N[h == 1]
        # h=2
        R[h == 2] = N[h == 2]
        G[h == 2] = C[h == 2]
        B[h == 2] = X[h == 2]
        # h=3
        R[h == 3] = N[h == 3]
        G[h == 3] = X[h == 3]
        B[h == 3] = C[h == 3]
        # h=4
        R[h == 4] = X[h == 4]
        G[h == 4] = N[h == 4]
        B[h == 4] = C[h == 4]
        # h=5
        R[h == 5] = C[h == 5]
        G[h == 5] = N[h == 5]
        B[h == 5] = X[h == 5]
        # match values
        m = V - C
        R = R+m
        G = G+m
        B = B+m
        return(R, G, B)

    # Basic shape of piper plot
    offset = 0.15
    offsety = offset*np.tan(np.pi/3)
    h = 0.5*np.tan(np.pi/3)
    ltriangle_x = np.array([0, 0.5, 1, 0])
    ltriangle_y = np.array([0, h, 0, 0])
    rtriangle_x = ltriangle_x + 2*offset + 1
    rtriangle_y = ltriangle_y
    diamond_x = np.array([0.5, 1, 1.5, 1, 0.5]) + offset
    diamond_y = h*(np.array([1, 2, 1, 0, 1])) + (offset*np.tan(np.pi/3))
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(
        111, aspect='equal', frameon=False, xticks=[], yticks=[]
    )
    ax.plot(ltriangle_x, ltriangle_y, '-k')
    ax.plot(rtriangle_x, rtriangle_y, '-k')
    ax.plot(diamond_x, diamond_y, '-k')
    # labels and title
    plt.text(-offset,      -offset,  '$Ca^{2+}$',
             horizontalalignment='left', verticalalignment='center')
    plt.text(0.5,          h+offset, '$Mg^{2+}$',
             horizontalalignment='center', verticalalignment='center')
    plt.text(1+offset,     -offset,  '$Na^+ + K^+$',
             horizontalalignment='right', verticalalignment='center')
    plt.text(1+offset,     -offset,  '$HCO_3^- + CO_3^{2-}$',
             horizontalalignment='left', verticalalignment='center')
    plt.text(1.5+2*offset, h+offset, '$SO_4^{2-}$',
             horizontalalignment='center', verticalalignment='center')
    plt.text(2+3*offset,   -offset,  '$Cl^-$',
             horizontalalignment='right', verticalalignment='center')

    # Convert chemistry into plot coordinates
    gmol = np.array([
        40.078, 24.305, 22.989768, 39.0983, 61.01714, 60.0092, 35.4527,
        96.0636
    ])
    eqmol = np.array([2., 2., 1., 1., 1., 2., 1., 2.])
    n = dat_piper.shape[0]
    meqL = (dat_piper / gmol) * eqmol
    sumcat = np.sum(meqL[:, 0:4], axis=1)
    suman = np.sum(meqL[:, 4:8], axis=1)
    cat = np.zeros((n, 3))
    an = np.zeros((n, 3))
    cat[:, 0] = meqL[:, 0] / sumcat  # Ca
    cat[:, 1] = meqL[:, 1] / sumcat  # Mg
    cat[:, 2] = (meqL[:, 2]+meqL[:, 3]) / sumcat  # Na+K
    an[:, 0] = (meqL[:, 4]+meqL[:, 5]) / suman  # HCO3 + CO3
    an[:, 2] = meqL[:, 6] / suman  # Cl
    an[:, 1] = meqL[:, 7] / suman  # SO4

    # Convert into cartesian coordinates
    cat_x = 0.5*(2*cat[:, 2] + cat[:, 1])
    cat_y = h*cat[:, 1]
    an_x = 1 + 2*offset + 0.5*(2*an[:, 2] + an[:, 1])
    an_y = h*an[:, 1]
    d_x = an_y/(4*h) + 0.5*an_x - cat_y/(4*h) + 0.5*cat_x
    d_y = 0.5*an_y + h*an_x + 0.5*cat_y - h*cat_x

    # plot data
    plt.plot(cat_x, cat_y, '.k', alpha=alphalevel)
    plt.plot(an_x,   an_y, '.k', alpha=alphalevel)
    plt.plot(d_x,     d_y, '.k', alpha=alphalevel)

    # color coding Piper plot
    if color is False:
        # add density color bar if alphalevel < 1
        if alphalevel < 1.0:
            ax1 = fig.add_axes([0.75, 0.4, 0.01, 0.2])
            cmap = plt.cm.gray_r
            norm = mpl.colors.Normalize(vmin=0, vmax=1/alphalevel)
            cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                                            norm=norm,
                                            orientation='vertical')
            cb1.set_label('Dot Density')

        return(dict(cat=cat,
                    an=an))
    else:
        import scipy.interpolate as interpolate
        # create empty grids to interpolate to
        x0 = 0.5
        y0 = x0 * np.tan(np.pi/6)
        X = np.reshape(np.repeat(
            np.linspace(0, 2+2*offset, 1000), 1000), (1000, 1000), 'F'
        )
        Y = np.reshape(np.repeat(
            np.linspace(0, 2*h + offsety, 1000), 1000), (1000, 1000), 'C'
        )
        H = np.nan * np.zeros_like(X)
        S = np.nan * np.zeros_like(X)
        V = np.nan * np.ones_like(X)
        A = np.nan * np.ones_like(X)
        # create masks for cation, anion triangle and upper and lower diamond
        ind_cat = np.logical_or(np.logical_and(X < 0.5, Y < 2*h*X),
                                np.logical_and(X > 0.5, Y < (2*h*(1-X))))
        ind_an = np.logical_or(
            np.logical_and(
                X < 1.5+(2*offset),
                Y < 2*h*(X-1-2*offset)
            ),
            np.logical_and(
                X > 1.5+(2*offset),
                Y < (2*h*(1-(X-1-2*offset)))
            )
        )
        ind_ld = np.logical_and(
            np.logical_or(
                np.logical_and(
                    X < 1.0+offset, Y > -2*h*X + 2*h*(1 + 2*offset)
                ),
                np.logical_and(
                    X > 1.0+offset, Y > 2*h*X - 2*h)), Y < h+offsety
        )
        ind_ud = np.logical_and(
            np.logical_or(
                np.logical_and(X < 1.0+offset, Y < 2*h*X),
                np.logical_and(
                    X > 1.0+offset,
                    Y < -2*h*X + 4*h*(1+offset))), Y > h+offsety
        )
        ind_d = np.logical_or(ind_ld == 1, ind_ud == 1)

        # Hue: convert x,y to polar coordinates
        # (angle between 0,0 to x0,y0 and x,y to x0,y0)
        H[ind_cat] = np.pi + np.arctan2(Y[ind_cat]-y0, X[ind_cat]-x0)
        H[ind_cat] = np.mod(H[ind_cat]-np.pi/6, 2*np.pi)
        H[ind_an] = np.pi + np.arctan2(
            Y[ind_an]-y0, X[ind_an] - (x0+1+(2*offset))
        )
        H[ind_an] = np.mod(H[ind_an]-np.pi/6, 2*np.pi)
        H[ind_d] = np.pi + np.arctan2(
            Y[ind_d]-(h+offsety), X[ind_d]-(1+offset)
        )
        # Saturation: 1 at edge of triangle, 0 in the centre,
        # Clough Tocher interpolation, square root to reduce central region
        xy_cat = np.array([[0.0, 0.0],
                           [x0,  h],
                           [1.0, 0.0],
                           [x0, y0]])
        xy_an = np.array([[1+(2*offset), 0.0],
                          [x0+1+(2*offset),  h],
                          [2+(2*offset), 0.0],
                          [x0+1+(2*offset), y0]])
        xy_d = np.array([[x0+offset,  h+offsety],
                         [1+offset, 2*h+offsety],
                         [x0+1+offset,   h+offsety],
                         [1+offset,     offsety],
                         [1+offset,   h+offsety]])
        z_cat = np.array([1.0, 1.0, 1.0, 0.0])
        z_an = np.array([1.0, 1.0, 1.0, 0.0])
        z_d = np.array([1.0, 1.0, 1.0, 1.0, 0.0])
        s_cat = interpolate.CloughTocher2DInterpolator(xy_cat, z_cat)
        s_an = interpolate.CloughTocher2DInterpolator(xy_an, z_an)
        s_d = interpolate.CloughTocher2DInterpolator(xy_d, z_d)
        S[ind_cat] = s_cat.__call__(X[ind_cat], Y[ind_cat])
        S[ind_an] = s_an.__call__(X[ind_an], Y[ind_an])
        S[ind_d] = s_d.__call__(X[ind_d], Y[ind_d])
        # Value: 1 everywhere
        V[ind_cat] = 1.0
        V[ind_an] = 1.0
        V[ind_d] = 1.0
        # Alpha: 1 everywhere
        A[ind_cat] = 1.0
        A[ind_an] = 1.0
        A[ind_d] = 1.0
        # convert HSV to RGB
        R, G, B = hsvtorgb(H, S**0.5, V)
        RGBA = np.dstack((R, G, B, A))
        # visualise
        plt.imshow(RGBA,
                   origin='lower',
                   aspect=1.0,
                   extent=(0, 2+2*offset, 0, 2*h+offsety))
        # calculate RGB triples for data points
        # hue
        hcat = np.pi + np.arctan2(cat_y-y0, cat_x-x0)
        hcat = np.mod(hcat-np.pi/6, 2*np.pi)
        han = np.pi + np.arctan2(an_y-y0, an_x - (x0+1+(2*offset)))
        han = np.mod(han-np.pi/6, 2*np.pi)
        hd = np.pi + np.arctan2(d_y-(h+offsety), d_x-(1+offset))
        # saturation
        scat = s_cat.__call__(cat_x, cat_y)**0.5
        san = s_an.__call__(an_x,  an_y)**0.5
        # value
        v = np.ones_like(hd)
        # rgb
        cat = np.vstack((hsvtorgb(hcat, scat, v))).T
        an = np.vstack((hsvtorgb(han,  san, v))).T
        module_io.output(fig, show, save, fname)
