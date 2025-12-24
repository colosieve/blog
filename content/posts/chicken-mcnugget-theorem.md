+++
title = "Chicken McNugget Theorem"
date = 2025-12-02T00:00:00Z
author = "colosieve"
tags = ["math", "number-theory", "combinatorics"]
+++

The Chicken McNugget Theorem (also called the Frobenius Coin Problem or Sylvester-Frobenius Theorem) answers: what's the largest amount you *can't* make with coins of two denominations?

## Theorem

For two coprime positive integers $a$ and $b$ (i.e., $\gcd(a,b) = 1$):

The largest integer that **cannot** be expressed as $ka + lb$ (where $k, l \geq 0$ are non-negative integers) is:

$$ab - a - b$$

Using Simon's Favorite Factoring Trick (SFFT), this equals:

$$(a-1)(b-1) - 1$$

## Example

For $a = 5$ and $b = 7$:

- Largest non-representable number = $5 \times 7 - 5 - 7 = 23$
- Check: 24 = 5+5+7+7, 25 = 5×5, 26 = 5+7+7+7, 27 = 5+5+5+5+7, ...
- But 23 cannot be written as $5k + 7l$

This is why it's called the "Chicken McNugget" theorem — McNuggets used to come in packs of 6, 9, and 20. The largest number of nuggets you couldn't order exactly was 43.
