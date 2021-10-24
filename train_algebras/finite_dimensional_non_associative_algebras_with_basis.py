from sage.misc.cachefunc import cached_method
from sage.categories.category_types import Category_over_base_ring  # type: ignore
from sage.categories.category_with_axiom import CategoryWithAxiom_over_base_ring  # type: ignore
from sage.categories.magmatic_algebras import MagmaticAlgebras  # type: ignore
from sage.matrix.constructor import matrix  # type: ignore


class FiniteDimensionalNonAssociativeAlgebrasWithBasis(Category_over_base_ring):
    r"""
    The category of non associative commutative finite dimensional
    algebra with basis implemented by their multiplication table on
    the basis.

    """

    def super_categories(self):
        """
        EXAMPLES::

            sage: from train_algebras import FiniteDimensionalNonAssociativeAlgebrasWithBasis
            sage: C = FiniteDimensionalNonAssociativeAlgebrasWithBasis(QQ)
            sage: C.super_categories()
            [Category of finite dimensional magmatic algebras with basis over Rational Field]
        """
        return [MagmaticAlgebras(self.base_ring()).WithBasis().FiniteDimensional()]

    def example(self):
        from .train_algebras import TrainAlgebras
        return TrainAlgebras(self.base_ring()).example()

    class ParentMethods:

        @cached_method
        def algebra_generators(self):
            r"""
            Returns the generators of this algebra, as per :meth:`Algebras.ParentMethods.algebra_generators`.

            EXAMPLES::

                sage: from train_algebras import FiniteDimensionalNonAssociativeAlgebrasWithBasis
                sage: A = FiniteDimensionalNonAssociativeAlgebrasWithBasis(QQ).example()
                sage: A.algebra_generators()
                Finite family {'e': A['e'], 'v': A['v'], 't': A['t']}
            """
            return self.basis()

        def isomorphism_ideal(self, other):
            """
            Computes the ideal whose variety is the set of isomorphisms from ``self`` to ``other``

            EXAMPLES::

                sage: import train_algebras
                sage: A2 = train_algebras.examples.A2(QQ)
                sage: A3 = train_algebras.examples.A3(QQ)
                sage: A4 = train_algebras.examples.A4(QQ)
                sage: A2.isomorphism_ideal(A2).dimension()
                2
                sage: A3.isomorphism_ideal(A3).dimension()
                4
                sage: A2.isomorphism_ideal(A3).dimension()
                -1
                sage: A2.isomorphism_ideal(A4).dimension()
                -1
                sage: A3.isomorphism_ideal(A4).dimension()
                -1
            """
            # j: the index of an element of the basis of ``self``
            # i:  the index of an element of the basis of ``other``
            J = self.basis().keys()
            I = other.basis().keys()
            base_ring = self.base_ring()
            R = base_ring[tuple("x%s%s" % (i, j) for i in I for j in J) + ("invdet",)]
            indeterminates = {(i, j): R("x%s%s" % (i, j)) for i in I for j in J}
            invdet = R("invdet")
            # extends the base ring
            self = self.__class__(R)
            other = other.__class__(R)

            def generic_morphism_on_basis(j):
                return other.sum_of_terms([(i, indeterminates[i, j]) for i in I])

            w = self.module_morphism(generic_morphism_on_basis, codomain=other)
            equations = [
                c
                for i in self.basis()
                for j in self.basis()
                for c in (w(i) * w(j) - w(j * i)).coefficients()
            ]
            det = matrix(len(I), len(J), R.gens()[:-1]).determinant()
            equation_det_non_nul = det * invdet - 1
            equations.append(equation_det_non_nul)
            return R.ideal(equations)

        def is_isomorphic(self, other):
            return self.isomorphism_ideal(other).dimension() >= 0

    class Commutative(CategoryWithAxiom_over_base_ring):

        class ParentMethods:
            def product_on_basis(self, a, b):
                r"""
                Product of basis elements, as per :meth:`AlgebrasWithBasis.ParentMethods.product_on_basis`.

                EXAMPLES::

                    sage: from train_algebras import FiniteDimensionalNonAssociativeAlgebrasWithBasis
                    sage: A = FiniteDimensionalNonAssociativeAlgebrasWithBasis(QQ).example()
                    sage: A.product_on_basis('e', 'v')
                    A['v']
                    sage: e, v, t = A.algebra_generators()
                    sage: e*e
                    A['e'] + A['t']
                    sage: v*v
                    A['t'] + A['v']
                    sage: e*t
                    1/2*A['t']
                    sage: t*e
                    1/2*A['t']
                    sage: v*t
                    1/2*A['t']
                    sage: t*v
                    1/2*A['t']
                    sage: t*t
                    0
                    sage: e*v
                    A['v']
                """
                t = self.product_on_basis_table
                if (a, b) in t:
                    return t[a, b]
                elif (b, a) in t:
                    return t[b, a]
                raise TypeError("Product of %s and %s not defined" % (a, b))

    class ElementMethods:
        def plenary_power(self, n):
            """
            Returns the `n`-th plenary power of ``self``

            The `n`-th plenary power of an element `x` of a magma is
            defined recursively as `y*y` where `y` is the `n-1`-th
            plenary power of `x`, taking `x` as the first plenary power
            of itself. On an associative magma, this is `x^{2^{n-1}}`.

            .. TODO:: this should be moved to :cls:`Magmas.ElementMethods`

            EXAMPLES::

                sage: from train_algebras import FiniteDimensionalNonAssociativeAlgebrasWithBasis
                sage: C = FiniteDimensionalNonAssociativeAlgebrasWithBasis(QQ)
                sage: A = C.example(); A
                A train algebra with basis indexed by {'e', 'v', 't'} over Rational Field
                sage: e,v,t = A.algebra_generators()
                sage: e.plenary_power(1)
                A['e']
                sage: e.plenary_power(2)
                A['e'] + A['t']
                sage: e.plenary_power(3)
                A['e'] + 2*A['t']

                sage: a = A.an_element(); a
                2*A['e'] + 3*A['t'] + 2*A['v']
                sage: a.plenary_power(1)
                2*A['e'] + 3*A['t'] + 2*A['v']
                sage: a.plenary_power(2)
                4*A['e'] + 20*A['t'] + 12*A['v']
                sage: a.plenary_power(3)
                16*A['e'] + 480*A['t'] + 240*A['v']

            """
            if n == 1:
                return self
            else:
                return self.plenary_power(n - 1) * self.plenary_power(n - 1)
