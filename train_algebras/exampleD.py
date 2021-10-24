from sage.misc.lazy_attribute import lazy_attribute                 # type: ignore
from sage.combinat.free_module import CombinatorialFreeModule
from train_algebras import TrainAlgebras


class D(CombinatorialFreeModule):
    """
    A non associative commutative algebra with basis e,v,t

    Product rule given by:

    EXAMPLES::

        sage: import train_algebras.examples
        sage: D = train_algebras.examples.D(QQ)
        sage: e, v, t = D.algebra_generators()
        sage: e*e
        D['e']
        sage: v*v
        0
        sage: t*t
        0
        sage: e*t
        0
        sage: t*e
        0
        sage: v*t
        0
        sage: t*v
        0
        sage: e*v
        1/2*D['v']
        sage: v*e
        1/2*D['v']
    """

    def __init__(self, base_ring):
        """
        EXAMPLES::

            sage: import train_algebras.examples
            sage: D = train_algebras.examples.D(QQ); D
            A train algebra with basis indexed by {'e', 'v', 't'} over Rational Field
            sage: TestSuite(D).run()
        """
        CombinatorialFreeModule.__init__(
            self,
            base_ring,
            ("e", "v", "t"),
            category=TrainAlgebras(base_ring),
            prefix="D",
        )

    @lazy_attribute
    def product_on_basis_table(self):
        e, v, t = self.algebra_generators()
        return {
            ("t", "t"): self.zero(),
            ("e", "e"): e,
            ("v", "v"): self.zero(),
            ("v", "e"): v / 2,
            ("v", "t"): self.zero(),
            ("e", "t"): self.zero(),
        }
