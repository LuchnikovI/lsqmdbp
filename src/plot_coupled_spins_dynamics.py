#!/usr/bin/python3.10

# pylint: skip-file

import os
from argparse import ArgumentParser
import numpy as np
from scipy.linalg import expm # type: ignore
import matplotlib.pyplot as plt # type: ignore
from im import coupled_dynamics
from constants import sigmax, sigmay, sigmaz
from cli_utils import _hdf2im, _hdf2trained_im

#plt.rcParams.update({
#    "text.usetex": True,
#    "font.family": "Helvetica"
#})

#def truncate_choi_rank(ker, rank):
#    lb, _, _, _, _, rb = ker.shape
#    sq_lb = int(np.sqrt(lb))
#    sq_rb = int(np.sqrt(rb))
#    ker = ker.reshape((sq_lb, sq_lb, 2, 2, 2, 2, sq_rb, sq_rb))
#    ker = ker.transpose((0, 2, 4, 6, 1, 3, 5, 7)).reshape((sq_lb * sq_rb * 2 * 2, sq_lb * sq_rb * 2 * 2))
#    u, s, vh = np.linalg.svd(ker)
#    ker = u[:, :rank] @ (s[:rank, np.newaxis] * vh[:rank])
#    ker = ker.reshape((sq_lb, 2, 2, sq_rb, sq_lb, 2, 2, sq_rb))
#    ker = ker.transpose((0, 4, 1, 5, 2, 6, 3, 7))
#    ker = ker.reshape((lb, 2, 2, 2, 2, rb))
#    return ker


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '--im_path1', '-p1',
        required=True,
        help="path to a directory with all the data for the influence matrix coupled with the first spin (`./experiments/output/<experiment_type>/<config_name>/<timestamp>`)",
    )
    parser.add_argument(
        '--im_path2', '-p2',
        required=True,
        help="path to a directory with all the data for the influence matrix coupled with the second spin (`./experiments/output/<experiment_type>/<config_name>/<timestamp>`)",
    )
    parser.add_argument(
        '--xx_int', '-x',
        default='0',
        help="xx interaction amplitude between spins"
    )
    parser.add_argument(
        '--yy_int', '-y',
        default='0',
        help="yy interaction amplitude between spins"
    )
    parser.add_argument(
        '--zz_int', '-z',
        default='1',
        help="zz interaction amplitude between spins"
    )
    args = parser.parse_args()
    im_exact1 = _hdf2im(args.im_path1)
    im_exact2 = _hdf2im(args.im_path2)
    #im_trained1 = list(map(lambda x: truncate_choi_rank(x, 5), reversed(_hdf2trained_im(args.im_path1))))
    #im_trained2 = list(map(lambda x: truncate_choi_rank(x, 5), reversed(_hdf2trained_im(args.im_path2))))
    im_trained1 = list(reversed(_hdf2trained_im(args.im_path1)))
    im_trained2 = list(reversed(_hdf2trained_im(args.im_path2)))
    xx = float(args.xx_int)
    yy = float(args.yy_int)
    zz = float(args.zz_int)
    h = xx * np.kron(sigmax, sigmax) + yy * np.kron(sigmay, sigmay) + zz * np.kron(sigmaz, sigmaz)
    u = expm(1j * h).reshape((2, 2, 2, 2))
    phi = np.tensordot(u, u.conj(), axes=0)
    phi = phi.transpose((0, 4, 1, 5, 2, 6, 3, 7)).reshape((4, 4, 4, 4))
    lmbds_gen = [np.linalg.eigvalsh(rho) for rho in coupled_dynamics(im_exact1, im_exact2, phi)]
    lmbds_trained = [np.linalg.eigvalsh(rho) for rho in coupled_dynamics(im_trained1, im_trained2, phi)]
    plt.title(r"$J_x={}$, $J_y={}$, $J_z={}$".format(xx, yy, zz))
    plt.plot([lmbds[0] for lmbds in lmbds_gen], 'b')
    plt.plot([lmbds[1] for lmbds in lmbds_gen], 'r')
    plt.plot([lmbds[2] for lmbds in lmbds_gen], 'k')
    plt.plot([lmbds[3] for lmbds in lmbds_gen], 'g')
    plt.plot([lmbds[0] for lmbds in lmbds_trained], 'b--')
    plt.plot([lmbds[1] for lmbds in lmbds_trained], 'r--')
    plt.plot([lmbds[2] for lmbds in lmbds_trained], 'k--')
    plt.plot([lmbds[3] for lmbds in lmbds_trained], 'g--')
    plt.legend([r"$\lambda_0$ exact", r"$\lambda_1$ exact", r"$\lambda_2$ exact", r"$\lambda_3$ exact",
                r"$\lambda_0$ predicted", r"$\lambda_1$ predicted", r"$\lambda_2$ predicted", r"$\lambda_3$ predicted"])
    plt.xlabel("Time")
    plt.savefig(os.path.dirname(args.im_path1) + "/coupled_dynamics_plot.png")


if __name__ == '__main__':
    main()
