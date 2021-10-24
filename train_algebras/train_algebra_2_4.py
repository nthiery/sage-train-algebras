from sage.misc.lazy_attribute import lazy_attribute                 # type: ignore
from sage.combinat.free_module import CombinatorialFreeModule
from sage.rings.number_field.number_field import NumberField
from .train_algebras import TrainAlgebras
from sage.rings.rational_field import QQ

class TrainAlgebra_2_4(CombinatorialFreeModule):
    """A train algebra with basis e,v,t

    Product rule given by:



    EXAMPLES::

        sage: import train_algebras.examples

    The product rule requires an element `s` such stat `s^2=7`.  If no
    base ring is provided, then the number field QQ['s'] is created
    and used::

        sage: T = train_algebras.examples.TrainAlgebra_2_4(); T
        A train algebra with basis indexed by {0, 1, 2, 3}
        over Number Field in s with defining polynomial s^2 + 7

    If instead a base ring `R` is provided, then `R('s')` should
    return an element `s` satisfying the above equation. Here we start
    from the default base ring and extend it as a polynomial ring::

        sage: K = T.base_ring(); K
        Number Field in s with defining polynomial s^2 + 7
        sage: R = K['x','y','z']
        sage: TR = train_algebras.examples.TrainAlgebra_2_4(R); TR
        A train algebra with basis indexed by {0, 1, 2, 3}
        over Multivariate Polynomial Ring in x, y, z
        over Number Field in s with defining polynomial s^2 + 7

    TESTS::

        sage: TestSuite(T).run()
        sage: TestSuite(TR).run()
    """

    def __init__(self, base_ring=None):
        if base_ring is None:
            s = QQ['s'].gen()
            p = s**2 + 7
            base_ring = NumberField(p, "s")
        s = base_ring('s')
        λ = (1-s)/4
        CombinatorialFreeModule.__init__(
            self,
            base_ring,
            (0, 1, 2, 3),
            category=TrainAlgebras(base_ring),
            prefix="e",
        )

        e = self.basis()

        self.product_on_basis_table = {
            (0, 0): e[0],
            (0, 1): e[1]/2,
            (0, 2): e[2]/2,
            (0, 3): λ*e[3],
            (1, 1): e[3],
            (2, 2): e[3],
            (1, 2): e[3],
            (1, 3): self.zero(),
            (2, 3): self.zero(),
            (3, 3): self.zero()
        }
