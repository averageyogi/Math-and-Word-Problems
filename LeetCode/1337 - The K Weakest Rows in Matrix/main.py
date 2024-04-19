def kWeakestRows(mat: list[list[int]], k: int) -> list[int]:
    strengths = []
    for i in mat:
        strengths.append(sum(i))

    return sorted(range(len(strengths)), key=strengths.__getitem__)[:k]


if __name__ == '__main__':
    mat = [[1,1,0,0,0],
           [1,1,1,1,0],
           [1,0,0,0,0],
           [1,1,0,0,0],
           [1,1,1,1,1]]
    k = 3

    print(kWeakestRows(mat, k))
