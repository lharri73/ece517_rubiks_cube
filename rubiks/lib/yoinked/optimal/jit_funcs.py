JIT_ENABLE = False
from rubiks.lib.yoinked.optimal.enums import Edge

if JIT_ENABLE:
    from numba import jit, njit
    from numba.typed import List

    # Ed = [Edge.UR, Edge.UF, Edge.UL, Edge.UB, Edge.DR, Edge.DF, Edge.DL, Edge.DB, Edge.FR, Edge.FL, Edge.BL, Edge.BR]

    @njit
    def edge_multiply(b_ep, b_eo, ep, eo):
        e_perm = [0] * 12
        e_ori = [0] * 12
        for e in range(12):
            if isinstance(b_ep[e], Edge):
                bep_vap = b_ep[e].value
            else:
                bep_vap = b_ep[e]
            e_perm[e] = ep[b_ep[e]]
            e_ori[e] = (b_eo[e] + eo[b_ep[e]]) % 2
        for e in range(12):
            ep[e] = e_perm[e]
            eo[e] = e_ori[e]

        return ep, eo

else:
    Ed = Edge
    def edge_multiply(b_ep, b_eo, ep, eo):
        e_perm = [0] * 12
        e_ori = [0] * 12
        for e in Ed:
            e_perm[e] = ep[b_ep[e]]
            e_ori[e] = (b_eo[e] + eo[b_ep[e]]) % 2
        for e in Ed:
            ep[e] = e_perm[e]
            eo[e] = e_ori[e]

        return ep, eo
