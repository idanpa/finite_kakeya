import sys
# q - size of the field, n - dimension of the vector space
q, n = int(sys.argv[1]), int(sys.argv[2])

#%%
import itertools
import json
from math import comb as choose
from tqdm import tqdm
from functools import cache
import numpy as np

@cache
def line(b, m):
    return set(tuple(b_plus_tm[bi][t][mi] for bi, mi in zip(b, m)) for t in range(q))

def is_kakeya(K, Fnq):
    for m in Fnq:
        for b in Fnq:
            if K.issuperset(line(b, m)):
                break
        else:
            return False
    return True

def load_sets():
    try:
        with open('kakeya.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_set(q, n, K_len, K):
    print(f'{(q,n,K_len)} - {K}')
    sets = load_sets()
    sets[str((q,n,K_len))] = K
    with open('kakeya.json', 'w') as f:
        try:
            json.dump(sets, f, default=tuple)
        except KeyboardInterrupt:
            json.dump(sets, f, default=tuple)
            raise

def get_set(q, n, blen):
    return load_sets().get(str((q,n,blen)), None)
#%%
print(f'{q=}, {n=}')

bi, t, mi = np.meshgrid(range(q), range(q), range(q), indexing='ij')
b_plus_tm = (bi + t*mi)%q # assume the finite field order is prime
Fnq = set(itertools.product(range(q), repeat=n))

#%%
for K_len in range(len(Fnq)-1, choose(q+n-1, n)-1, -1):
    K = get_set(q, n, K_len)
    if K == []:
        print(f'{(q,n,K_len+1)} - {get_set(q, n, K_len+1)}')
        break
    if K is not None:
        continue
    print(f'{q}, {n}, {K_len} / {len(Fnq)}')
    for K in tqdm(itertools.combinations(Fnq, K_len), total=choose(len(Fnq), K_len)):
        K = set(K)
        if is_kakeya(K, Fnq):
            save_set(q, n, K_len, K)
            break
    else:
        save_set(q, n, K_len, set())
        break
