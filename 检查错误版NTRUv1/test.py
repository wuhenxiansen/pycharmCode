while C[index].coe[index1] % int(pow(2, lenB)) != sum:
    C[index].coe[index1] += NTRU.p
    C[index].coe[index1] %= NTRU.q