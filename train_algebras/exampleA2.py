from sage.misc.lazy_attribute import lazy_attribute                 # type: ignore
from sage.combinat.free_module import CombinatorialFreeModule
from train_algebras import TrainAlgebras


class A2(CombinatorialFreeModule):
    """
    A non associative commutative algebra with basis e,v,t

    Product rule given by:

    EXAMPLES::

    """

    def __init__(self, base_ring):
        """
        EXAMPLES::

            sage: import train_algebras.examples
            sage: A2 = train_algebras.examples.A2(QQ); A2
            A train algebra with basis indexed by {'e', 'v', 't'} over Rational Field
            sage: TestSuite(A2).run()
        """
        CombinatorialFreeModule.__init__(
            self,
            base_ring,
            ("e", "v", "t"),
            category=TrainAlgebras(base_ring),
            prefix="A2",
        )

    @lazy_attribute
    def product_on_basis_table(self):
        e, v, t = self.algebra_generators()
        return {
            ("t", "t"): self.zero(),
            ("e", "e"): e + t,
            ("v", "v"): self.zero(),
            ("v", "e"): self.zero(),
            ("v", "t"): self.zero(),
            ("e", "t"): t / 2,
        }
