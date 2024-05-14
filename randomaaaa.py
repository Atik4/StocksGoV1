from collections import Counter

# Define constants
N = 10001
MOD = 10**9 + 7

# Precompute factorial and factorial modular inverses
factorials = [1] * N
factorial_inverses = [1] * N
for i in range(1, N):
    factorials[i] = factorials[i - 1] * i % MOD  # Calculate factorial of i
    factorial_inverses[i] = pow(factorials[i], MOD - 2, MOD)  # Calculate the inverse using Fermat's Little Theorem


def comb(n, k):
    """Calculate the combinational number C(n,k) modulo MOD."""
    return factorials[n] * factorial_inverses[k] * factorial_inverses[n - k] % MOD


def countGoodSubsequences(s):
    char_count = Counter(s)
    total_good_subsequences = 0

    for i in range(1, max(char_count.values()) + 1):
        ways_to_form = 1
        for count in char_count.values():
            if count >= i:
                ways_to_form = ways_to_form * (comb(count, i) + 1) % MOD
        total_good_subsequences = (total_good_subsequences + ways_to_form - 1) % MOD

    return total_good_subsequences


print(countGoodSubsequences(s="aabbcc"))
