from sage.misc.lazy_attribute import lazy_attribute                 # type: ignore
from sage.structure.sage_object import load
from sage.combinat.free_module import CombinatorialFreeModule

from train_algebras import TrainAlgebras


class A3(CombinatorialFreeModule):
    """
    A non associative commutative algebra with basis e,v,t

    Product rule given by::

    EXAMPLES::

        sage: import train_algebras.examples
        sage: A3 = train_algebras.examples.A3(QQ)
        sage: e, v, t = A3.algebra_generators()
        sage: e*e
        A3['e'] + A3['t']
        sage: v*v
        0
        sage: t*t
        0
        sage: e*t
        1/2*A3['t']
        sage: t*e
        1/2*A3['t']
        sage: v*t
        0
        sage: t*v
        0
        sage: e*v
        1/2*A3['v']
        sage: v*e
        1/2*A3['v']
    """

    def __init__(self, base_ring):
        """
        EXAMPLES::

            sage: import train_algebras.examples
            sage: A3 = train_algebras.examples.A3(QQ); A3
            A train algebra with basis indexed by {'e', 'v', 't'} over Rational Field
            sage: TestSuite(A3).run()
        """
        CombinatorialFreeModule.__init__(
            self,
            base_ring,
            ("e", "v", "t"),
            category=TrainAlgebras(base_ring),
            prefix="A3",
        )

    @lazy_attribute
    def product_on_basis_table(self):
        e, v, t = self.algebra_generators()
        return {
            ("t", "t"): self.zero(),
            ("e", "e"): e + t,
            ("v", "v"): self.zero(),
            ("v", "e"): v / 2,
            ("v", "t"): self.zero(),
            ("e", "t"): t / 2,
        }
