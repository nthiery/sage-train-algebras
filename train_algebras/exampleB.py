from sage.misc.lazy_attribute import lazy_attribute                 # type: ignore
from sage.combinat.free_module import CombinatorialFreeModule
from train_algebras import TrainAlgebras


class B(CombinatorialFreeModule):
    """
    Another non associative commutative algebra with basis e,v,t with product rule given by::

    EXAMPLES::

        sage: import train_algebras.examples
        sage: B = train_algebras.examples.B(QQ)
        sage: e, v, t = B.algebra_generators()
        sage: e*e
        B['e']
        sage: v*v
        B['t']
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
        1/2*B['t']
        sage: v*e
        1/2*B['t']
    """

    def __init__(self, base_ring):
        """
        EXAMPLES::

            sage: import train_algebras.examples
            sage: B = train_algebras.examples.B(QQ); B
            A train algebra with basis indexed by {'e', 'v', 't'} over Rational Field
            sage: TestSuite(B).run()
        """
        CombinatorialFreeModule.__init__(
            self,
            base_ring,
            ("e", "v", "t"),
            category=TrainAlgebras(base_ring),
            prefix="B",
        )

    @lazy_attribute
    def product_on_basis_table(self):
        e, v, t = self.algebra_generators()
        return {
            ("t", "t"): self.zero(),
            ("e", "e"): e,
            ("v", "v"): t,
            ("v", "e"): t / 2,
            ("v", "t"): self.zero(),
            ("e", "t"): self.zero(),
        }
