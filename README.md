---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.10.0
kernelspec:
  display_name: SageMath 9.5.beta3
  language: sage
  name: sagemath
---

# Sage-Train_Algebras

Sage-Train_Algebras is a tiny library to compute with (commutative)
*(pre)train algebras* of finite dimension. It originates from two
successive CIMPA schools in Burkina Faso (Bobo Dioulasso, 2012 &
2021).

It's meant to support computer exploration of (small) examples defined
by their multiplication table, and provides utilities to easily define
such, test isomorphism, test whether they actually are train algebras,
and so on.

## Context

A *pre-train algebra* is a commutative non associative algebra equiped
with an algebra morphism $\omega$ to its base ring satisfying an
equation of the form ... [TODO]

A *train algebra* is a pretrain algebra satisfying an equation of the
form $\alpha_0 x^n + \alpha_1 \omega(x)x^{n-2} + \ldots + \omega(x)^n
=0$, where $alpha_0+\cdots+\alpha_n=0$ (wlog, we may assume
$\alpha_0=1$).

TODO: references

## First example

```{code-cell} ipython3
import train_algebras.examples
```

Let's take an example of train algebra:

```{code-cell} ipython3
A = train_algebras.examples.TrainAlgebra_2_4()
```

Here is an element:

```{code-cell} ipython3
A.an_element()
```

One may build elements by linear combinations of elements of the basis:

```{code-cell} ipython3
e = A.basis()
```

```{code-cell} ipython3
y = e[0] + 2*e[1] + 3*e[2] + 4*e[3]
y
```

Let's do a bit of arithmetic:

```{code-cell} ipython3
y*y
```

```{code-cell} ipython3
(y*y)*(y*y)
```

```{code-cell} ipython3
y*y*y*y
```

By Python's priority rules, the previous product is computed as:

```{code-cell} ipython3
((y*y)*y)*y
```

As can be seen above, the algebra is indeed not associative.

+++

## Looking for isomorphisms between two algebras

In this section, we show how to search for isomorphisms between two
examles of finite dimensional (associative or not) algebras, here
$A_2$ and $A_3$.

In the first subsection we do the search step by step to explain how
it works by reducing the problem to solving polynomial equations. In
the second step, we use the method `isomorphism_ideal` to automate the
process.

+++

Initialisation:

```{code-cell} ipython3
import train_algebras.examples
```

## By hand

+++

We start by defining a generic linear morphism from $A_2$ to $A_3$
mapping each basis element $e_i$ of $A_2$ to $\sum_{j} x_{i,j} f_j$,
where the $x_{i,j}$' are indeterminates and the $f_j$'s the basis of
$A_3$.  To achieve this, we need to extend the base ring with these
indeterminates. 

In our example, the basis of $A_2$ and $A_3$ are indexed by $I=\{e, v, t\}$.


Here are the indeterminates, as a family mapping each pair (i,j) to it's indeterminate:

```{code-cell} ipython3
I = ["e", "v", "t"]
indeterminates = Family({ (i, j): f"x_{i}{j}" for i in I for j in I })
indeterminates
```

```{code-cell} ipython3
indeterminates["e","v"]
```

We extend the base ring (here the rationals QQ) as a polynomial ring
to include the above indeterminates, and also $y$ which will need
later:

```{code-cell} ipython3
R = QQ[tuple(indeterminates) + ("y",)]
R
```

Now we rebuild the indeterminates as a family $(x_{i,j})_{i\in I, j\in I}$ of elements of R:

```{code-cell} ipython3
indeterminates = indeterminates.map(R)
xev = indeterminates["e", "v"]
xev^3 + 4*xev
```

We define the algebras of interest over this polynomial ring:

```{code-cell} ipython3
A2 = train_algebras.examples.A2(R)
A3 = train_algebras.examples.A3(R)
```

and define a linear morphism $w$ between $A_2$ and $A_3$ with generic coefficients:

```{code-cell} ipython3
def w_on_basis(j):
    return A3.sum_of_terms([ (i, indeterminates[i,j]) for i in I])
w = A2.module_morphism(w_on_basis, codomain=A3)
```

This is the morphism with the following matrix:

```{code-cell} ipython3
w.matrix()
```

Let's put this morphism into action:

```{code-cell} ipython3
e,v,t = A2.basis()
```

```{code-cell} ipython3
w(e + 2*v)
```

```{code-cell} ipython3
w(e)*w(t) - w(e*t)
```

Now we build the equations on the coefficients stating that this is a
morphism, and display them after removing duplicates:

```{code-cell} ipython3
equations = [c
             for a1 in A2.basis()
             for a2 in A2.basis()
             for c in (w(a1)*w(a2) - w(a1*a2)).coefficients() ]
set(equations)
```

Let's solve the equations. Alas, Sage's `solve` function does not
accept directly a system of polynomial equations:

```{code-cell} ipython3
solve(equations, R.gens())
```

We need to build explicitly the ideal defined by these equations and
request properties of its variety:

```{code-cell} ipython3
I = R.ideal(equations)
I.dimension()
```

This means that there are a 3-dimensional subvariety of morphisms between $A_2$ and $A_3$. We
could recover the values of the indeterminates from I, and build
explicitly the morphisms.

However we don't want just *morphisms* but *isomorphisms*. To achieve
this, we force the determinant $d$ of the matrix of the morphism to be
non-zero by adding an equation $dy=1$ where $y$ is a new variable. At
the end, there is no isomorphism:

```{code-cell} ipython3
d = matrix(3,3,indeterminates.values()).determinant()
y = R.gens()[-1]
equations.append(d*y-1)
I = R.ideal(equations)
I.dimension()
```

TODO: clarify what this does: check the documenation to see if this is solving over the base ring, or over, say, its algebraic closure.

+++

## Using the `isomorphism_ideal` method

This process is automatized by the method `isomorphism_ideal` of
[FiniteDimensionalNonAssociativeAlgebrasWithBasis](train_algebras.py):

```{code-cell} ipython3
A2.isomorphism_ideal??
```

```{code-cell} ipython3
A2 = train_algebras.examples.A2(QQ)
A3 = train_algebras.examples.A3(QQ)
```

```{code-cell} ipython3
I = A2.isomorphism_ideal(A3)
I.dimension()
```

```{code-cell} ipython3
A2.isomorphism_ideal(A2).dimension()
```
