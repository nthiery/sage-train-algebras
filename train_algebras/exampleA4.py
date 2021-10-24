from sage.misc.lazy_attribute import lazy_attribute                 # type: ignore
from sage.structure.sage_object import load
from sage.combinat.free_module import CombinatorialFreeModule

from train_algebras import TrainAlgebras


class A4(CombinatorialFreeModule):
    """
    A non associative commutative algebra with basis e,v,t

    Product rule given by::

    EXAMPLES::

        sage: import train_algebras.examples
        sage: A4 = train_algebras.examples.A4(QQ)
        sage: e, v, t = A4.algebra_generators()
        sage: e*e
        A4['e'] + A4['t']
        sage: v*v
        A4['t'] + A4['v']
        sage: t*t
        0
        sage: e*t
        1/2*A4['t']
        sage: t*e
        1/2*A4['t']
        sage: v*t
        1/2*A4['t']
        sage: t*v
        1/2*A4['t']
        sage: e*v
        A4['v']
        sage: v*e
        A4['v']
    """

    def __init__(self, base_ring):
        """
        EXAMPLES::

            sage: import train_algebras.examples
            sage: A4 = train_algebras.examples.A4(QQ); A4
            A train algebra with basis indexed by {'e', 'v', 't'} over Rational Field
            sage: TestSuite(A4).run()
        """
        CombinatorialFreeModule.__init__(
            self,
            base_ring,
            ("e", "v", "t"),
            category=TrainAlgebras(base_ring),
            prefix="A4",
        )

    @lazy_attribute
    def product_on_basis_table(self):
        e, v, t = self.algebra_generators()
        return {
            ("t", "t"): self.zero(),
            ("e", "e"): e + t,
            ("v", "v"): v + t,
            ("v", "e"): v,
            ("v", "t"): t / 2,
            ("e", "t"): t / 2,
        }
