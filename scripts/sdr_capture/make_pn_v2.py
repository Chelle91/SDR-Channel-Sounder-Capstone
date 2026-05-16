import numpy as np

def m_sequence(register_length=10):
    reg = np.ones(register_length, dtype=int)
    seq = []

    for _ in range(2**register_length - 1):
        seq.append(reg[-1])
        feedback = (reg[2] + reg[9]) % 2
        reg[1:] = reg[:-1]
        reg[0] = feedback

    return np.array(seq)

pn = m_sequence(10)
pn = 2*pn - 1
pn_complex = pn.astype(np.complex64)

pn_complex.tofile("pn.dat")

print("Saved pn.dat")
print("PN length:", len(pn_complex))
