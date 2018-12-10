import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

def generate_toys(n_samples, z=None):
    Y = np.zeros(n_samples)
    Y[n_samples//2:] = 1

    if z == None:
        Z = np.random.normal(0, 1, size=n_samples)
    elif z == '2gauss':
        Z0 = np.random.normal(0, 1, size=n_samples//2)
        Z1 = np.random.normal(1, 1, size=n_samples//2)
        Z = np.concatenate([Z0, Z1])
    else:
        Z = z * np.ones(n_samples)

    X0 = np.random.multivariate_normal([0, 0], [[1, -0.5],[-0.5, 1]], size=n_samples//2)
    X1 = np.random.multivariate_normal([1, 1], 0.5*np.eye(2), size=n_samples//2)
    X1[:,1] += Z[n_samples//2:]
    X = np.concatenate([X0, X1])

    # reshuffle to mix y=0,1
    x1, x2 = X[:,0], X[:,1]
    s = np.stack([x1, x2, Y, Z], axis=1)
    X = s[:, :2]
    Y = s[:, 2]
    Z = s[:, 3]

    return X, Y, Z


def generate_hmumu():

    # first, load the dataset
    df = pd.read_csv('../data/combined_10000.csv')
    n_total = df.shape[0]

    X_names = ['Muons_Eta_Lead', 'Muons_Eta_Sub', 'Z_PT']
    Z_names = ['Muons_Minv_MuMu']
    Y_names = ['IsSignal']
    W_names = ['GlobalWeight', 'MLWeight']
    X = df[X_names]
    Z = df[Z_names]
    Y = df[Y_names].values
    W = df[W_names].values

    # normalise all features
    x_scaler = StandardScaler()
    z_scaler = StandardScaler()
    scaled_X = x_scaler.fit_transform(X)
    scaled_Z = z_scaler.fit_transform(Z)

    # first yield the scalers
    #print('yielding the scalers')
    yield x_scaler, z_scaler

    # and then sample the dataset randomly
    while True:
        #print('receiving the n_samples')
        n_samples = yield # feed how many samples you'd like in each iteration (using send method)
        indices = np.random.randint(0, n_total, size=n_samples)
        #print('yielding scaled data')
        yield scaled_X[indices, :], Y[indices, :], scaled_Z[indices, :], W[indices, :]

