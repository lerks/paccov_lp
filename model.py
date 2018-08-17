import numpy as np


class Model:

    def __init__(self,
                 a: np.ndarray,
                 x: np.ndarray,
                 f: float,
                 rho: float,
                 theta: float):
        self.a: np.ndarray = a
        self.x: np.ndarray = x
        self.f: float = f
        self.rho: float = rho
        self.theta: float = theta

        self.n, self.m = self.a.shape

    def coeff(self, v: int, e: int):
        return self.a[v, e]

    def primal_var(self, e: int):
        return self.x[e]

    def dual_var(self, v: int):
        return (np.expm1(np.log1p(self.f * self.rho * self.theta)
                         * np.dot(self.a[v, :], self.x))
                / self.f)

    def dual_cst(self, e: int):
        dual_var = (np.expm1(np.log1p(self.f * self.rho * self.theta)
                             * np.dot(self.a, self.x))
                    / self.f)
        return np.dot(self.a[:, e], dual_var)

    def dual_cst_at(self, e: int, value: float):
        x = self.x.copy()
        x[e] = value
        dual_var = (np.expm1(np.log1p(self.f * self.rho)
                             * np.dot(self.a, x))
                    / self.f)
        return np.dot(self.a[:, e], dual_var)

    def primal_cst(self, v: int):
        return np.dot(self.a[v, :], self.x)

    def dual_cst_over_range(self, e: int, domain: np.ndarray):
        t, = domain.shape
        x = self.x.copy()
        x[e] = np.infty
        primal_cst_over_range = (np.dot(self.a, self.x).reshape((self.m, 1))
                                 + (self.a[:, e].reshape((self.m, 1))
                                    * (domain - self.x[e]).reshape((1, t))))
        dual_var_over_range = (np.expm1(np.log1p(self.f * self.rho * self.theta)
                                        * primal_cst_over_range)
                               / self.f)
        return np.dot(self.a[:, e], dual_var_over_range)

    def dual_cst_over_time(self, e: int, domain: np.ndarray):
        t, = domain.shape
        x = self.x.copy()
        x[e] = np.infty
        primal_cst_over_time = np.dot(self.a,
                                      np.minimum(x.reshape((self.m, 1)),
                                                 domain.reshape((1, t))))
        dual_var_over_time = (np.expm1(np.log1p(self.f * self.rho * self.theta)
                                       * primal_cst_over_time)
                              / self.f)
        return np.dot(self.a[:, e], dual_var_over_time)


def plot_dual_cst_over_range(
        m: Model, e: int, val: float, max_val: float, steps: int):
    path = list()
    x_vals = np.linspace(0, max_val, steps + 1, endpoint=True)
    y_vals = m.dual_cst_over_range(e, domain=x_vals)
    for i in range(0, steps + 1):
        if x_vals[i] > val:
            break
        path.append("%g,%g" % (i / steps, y_vals[i]))
    return "M " + " L ".join(path)


def plot_dual_cst_over_time(
        m: Model, e: int, val: float, max_val: float, steps: int):
    path = list()
    x_vals = np.linspace(0, max_val, steps + 1, endpoint=True)
    y_vals = m.dual_cst_over_time(e, domain=x_vals)
    for i in range(0, steps + 1):
        if x_vals[i] > val:
            break
        path.append("%g,%g" % (i / steps, y_vals[i]))
    return "M " + " L ".join(path)
