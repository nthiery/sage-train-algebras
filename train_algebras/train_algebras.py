from sage.misc.lazy_attribute import lazy_attribute                 # type: ignore
from sage.categories.category_types import Category_over_base_ring  # type: ignore
from .finite_dimensional_non_associative_algebras_with_basis import FiniteDimensionalNonAssociativeAlgebrasWithBasis
from sage.combinat.free_module import CombinatorialFreeModule  # type: ignore

class PreTrainAlgebras(Category_over_base_ring):
    """
    Pre-train algebras

    .. WARN::

        All pre-train algebras are supposed to be commutative and
        finite dimensional.

    EXAMPLES::

        sage: from train_algebras import PreTrainAlgebras
        sage: C = PreTrainAlgebras(QQ)
        sage: C.super_categories()
        [Category of commutative finite dimensional non associative algebras with basis over Rational Field]

    TESTS::

        sage: TestSuite(C).run()

    """

    def super_categories(self):
        return [FiniteDimensionalNonAssociativeAlgebrasWithBasis(self.base_ring()).Commutative()]

class TrainAlgebras(Category_over_base_ring):
    """
    Train algebras

    EXAMPLES::

        sage: from train_algebras import TrainAlgebras
        sage: C = TrainAlgebras(QQ)
        sage: C.super_categories()
        [Category of pre train algebras over Rational Field]

    TESTS::

        sage: TestSuite(C).run()
    """

    def super_categories(self):
        return [PreTrainAlgebras(self.base_ring())]

    def example(self):
        return Example(self.base_ring())

    class ParentMethods:
        def _repr_(self):
            """
            EXAMPLES::

                sage: from train_algebras import TrainAlgebras
                sage: C = TrainAlgebras(QQ)
                sage: C.example()                # indirect doctest
                A train algebra with basis indexed by {'e', 'v', 't'} over Rational Field
            """
            return "A train algebra with basis indexed by %s over %s" % (
                self.basis().keys(),
                self.base_ring(),
            )


class Example(CombinatorialFreeModule):
    """
    An example of train algebra

    Basis: e,v,t

    Product rule:

    - `e^2=e+t`
    - `v^2=v+t`
    - `et=vt=1/2t`
    - `t^2=0`
    - `ev=v`

    We check that this algebra satisfies an algebraic identity with
    two parameters `X` and `Y`. We will need some variables to
    represent generic elements of the ground ring::

        sage: R = QQ['x','y','z']
        sage: from train_algebras import TrainAlgebras
        sage: A = TrainAlgebras(R).example()

    We build a generic element `X` of the algebra::

        sage: x,y,z = R.gens()
        sage: e,v,t = A.algebra_generators()
        sage: X = x*e + y*v + z*t

     The identity is linear in `Y`, so we can just let `Y` run through
     the basis; otherwise we would have needed to define `Y` like `X`,
     using more variables in the base ring::

        sage: for Y in [e,v,t]:
        ....:     print(3 * X*((X*X)*Y) - 2 * X*(X*(X*Y)) - ((X*X)*X)*Y)
        0
        0
        0
    """

    def __init__(self, base_ring):
        """
        EXAMPLES::

            sage: from train_algebras import TrainAlgebras
            sage: A = TrainAlgebras(QQ).example(); A
            A train algebra with basis indexed by {'e', 'v', 't'} over Rational Field
            sage: TestSuite(A).run() # not tested (breaks horribly because of the cheating with associative algebras
        """
        CombinatorialFreeModule.__init__(
            self,
            base_ring,
            ("e", "v", "t"),
            category=TrainAlgebras(base_ring),
            prefix="A",
        )

    @lazy_attribute
    def product_on_basis_table(self):
        e, v, t = self.algebra_generators()
        return {
            ("t", "t"): self.zero(),
            ("e", "e"): e + t,
            ("v", "v"): v + t,
            ("e", "t"): t / 2,
            ("v", "t"): t / 2,
            ("e", "v"): v,
        }
