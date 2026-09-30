#!/usr/bin/env python3
"""Plot the prime-counting function using the Sieve of Eratosthenes."""

import argparse
import os
from pathlib import Path


def prime_counting_values(limit: int) -> list[int]:
    """Return ``pi(x)`` for every integer from zero through ``limit``."""
    if limit < 0:
        raise ValueError("limit must be non-negative")

    is_prime = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        is_prime[0] = 0
    if limit >= 1:
        is_prime[1] = 0

    for number in range(2, int(limit**0.5) + 1):
        if is_prime[number]:
            start = number * number
            is_prime[start : limit + 1 : number] = b"\x00" * (
                ((limit - start) // number) + 1
            )

    counts: list[int] = []
    count = 0
    for prime in is_prime:
        count += prime
        counts.append(count)

    return counts


def count_primes(limit: int) -> int:
    """Return the number of prime numbers less than or equal to ``limit``."""
    return prime_counting_values(limit)[-1]


def plot_prime_counting_function(limit: int) -> None:
    """Plot the prime-counting function from zero through ``limit``."""
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError as error:
        raise SystemExit(
            "Matplotlib is required. Run this script with: "
            ".venv/bin/python count_primes.py LIMIT"
        ) from error

    x_values = range(limit + 1)
    counts = prime_counting_values(limit)

    plt.step(x_values, counts, where="post", label=r"$\pi(x)$")
    plt.xlabel("x")
    plt.ylabel("Number of primes ≤ x")
    plt.title(f"Prime-counting function up to {limit}")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()

    output_path = Path.cwd() / "prime_counting_function.png"
    plt.savefig(output_path, dpi=150)
    print(f"Plot saved to {output_path}")

    if os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"):
        plt.show()
    else:
        plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Plot the prime-counting function up to and including LIMIT."
    )
    parser.add_argument("limit", type=int, help="non-negative inclusive upper bound")
    args = parser.parse_args()
    if args.limit < 0:
        parser.error("limit must be non-negative")
    plot_prime_counting_function(args.limit)


if __name__ == "__main__":
    main()
