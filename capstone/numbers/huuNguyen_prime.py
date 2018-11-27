from math import floor
from fractions import gcd
from random import randint, randrange


def get_primes(n):
    """
    Iterate through all the possible divisors of n and return a list of all of
    the actual divisors in sorted order.
    """
    result = []
    for i in range(2, n + 1):
        s = 0
        while n % i == 0:
            n = n / i
            s += 1
        if s > 0:
            for k in range(s):
                result.append(i)
            if n == 1:
                return result


def brent_prime(n):
    """
    Implementation of Richard Brent's Pollard rho algorithm for finding a single
    prime factor of the input integer.
    This requires that the integer is not itself prime. This algorithm is not
    deterministic. Sometimes it will return a composite factor of the input
    integer.
    """
    if n % 2 == 0:
        return 2
    y = randint(1, n - 1)
    c = randint(1, n - 1)
    m = randint(1, n - 1)
    g = 1
    r = 1
    q = 1
    while g == 1:
        x = y
        for i in range(r):
            y = ((y * y) % n + c) % n
        k = 0
        while (k < r and g == 1):
            ys = y
            for i in range(min(m, r - k)):
                y = ((y * y) % n + c) % n
                q = q * (abs(x - y)) % n
            g = gcd(q, n)
            k = k + m
        r = r * 2
    if g == n:
        while True:
            ys = ((ys * ys) % n + c) % n
            g = gcd(abs(x - ys), n)
            if g > 1:
                break
    return g


def miller_rabin_prime_test(n, iterations):
    """
    Implementation of the Miller-Rabin primality test, with a slight
    modification where we return True for 1 or 2.
    This test is not deterministic, but with a high iterations factor it is
    extremely robust.
    """
    if n < 2:
        return True
    elif n == 2:
        return True
    elif n % 2 == 0:
        return False
    s = 0
    d = n - 1

    while True:
        q, r = divmod(d, 2)
        if r == 1:
            break
        s += 1
        d = q
    assert(2**s * d == n - 1)
    
    def try_composite(a):
        if pow(int(a), int(d), int(n)) == 1:
            return False
        for i in range(s):
            if pow(int(a), int(2**i * d), int(n)) == n - 1:
                return False
        return True

    for i in range(iterations):
        a = randrange(2, n)
        if try_composite(a):
            return False
    return True


def brent_get_all_primes(n):
    """
    Recursively sniff out primes (and sometimes composites) found by Brent
    algorithm.
    This uses the Miller-Rabin primality test to filter out primes before
    sending them to Brent because Brent cannot handle prime inputs.
    
    """
    while not miller_rabin_prime_test(n, 100):
        p = brent_prime(n)
        n /= p
        return brent_get_all_primes(p) + brent_get_all_primes(n)
    if n == 1:
        return []
    return [n]


def validate_positive_integer():
    """
    Ask the user for input and only return when a positive integer under the
    ceiling is given.
    """
    while True:
        s = input("Whose prime factors do you want to see? ")
        try:
            n = int(s)
            if n >= 100000000000000000000000:
                print ("Enter an integer smaller than", \
                      "100000000000000000000000 (10^23).") 
            elif n > 0:
                return n
            else:
                print ("Enter a positive integer.")
        except ValueError:
            print ("Enter a positive integer.")


def main():
    composite = validate_positive_integer()
    primes = [int(p) for p in brent_get_all_primes(composite)]
    print ("The primes of", composite, "are", primes)


if __name__ == "__main__":
    main()
