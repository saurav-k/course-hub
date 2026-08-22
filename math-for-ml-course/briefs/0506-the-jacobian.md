# 0506 - The Jacobian is the chain rule when both ends are vectors

> **PLACEHOLDER NUMBER.** Real number assigned by the scaffold (#41). Report label C06.

| | |
|---|---|
| Module | M05 Calculus |
| Rung | working (`pill med`) |
| Label | `core` |
| Prerequisites | 0502, 0504. M03: matrix multiplication, shapes, the matrix as a linear map. |
| Enables | 0507, 0508, 0512, and M08's change of variables |

## The single tight idea

Stack every partial derivative of a vector-to-vector map into a matrix and the chain rule
becomes matrix multiplication.

## Beats, in order

1. **A layer takes a vector and returns a vector.** There is no single slope. There are
   `n x m` of them, and the question is how to hold them.
2. **The Jacobian, defined.** `J[i][j] = d f_i / d x_j`, shape `n x m` for
   `f : R^m -> R^n`. Rows index outputs, columns index inputs, and getting that backwards
   is the most common error in the territory.
3. **The vector chain rule, in the exact form backpropagation uses.**
   `grad_x z = (dy/dx)^T grad_y z`.
4. **Read that line aloud.** A gradient goes in, gets multiplied by a transposed
   Jacobian, and a gradient comes out. That is one backpropagation step and nothing else.
5. **The vector-Jacobian product.** Autodiff never builds `J`, it computes `v^T J`.
   Say why with a number: `J` for a 4096-to-4096 layer holds 16.7 million entries that
   would be discarded after one multiplication.
6. **Worked: a Jacobian determinant that is exactly a volume factor,** checked twice.
7. **Forward pointer.** That determinant is what makes a change of variables in a density
   work, which is M08's, and it is why normalising flows are built out of maps whose
   determinant is cheap.

## Named theorems and their stated proofs

**Theorem 1. The multivariate chain rule.**

> Let `g : R^m -> R^n` be differentiable at `a` and `f : R^n -> R^p` differentiable at
> `g(a)`. Then `f . g` is differentiable at `a` and
> `J_{f.g}(a) = J_f(g(a)) J_g(a)`.
>
> *Proof.* Write `b = g(a)`, `A = J_f(b)`, `B = J_g(a)`. Differentiability gives
> `g(a + h) = b + B h + r(h)` with `r(h)/||h|| -> 0`, and
> `f(b + k) = f(b) + A k + s(k)` with `s(k)/||k|| -> 0`.
> Put `k = B h + r(h)`, which tends to `0` with `h`. Then
>
>   `f(g(a + h)) = f(b) + A(B h + r(h)) + s(k) = f(g(a)) + (A B) h + [A r(h) + s(k)]`.
>
> It remains to show the bracket is `o(||h||)`. First, `||A r(h)|| <= ||A|| ||r(h)||`,
> and `||r(h)||/||h|| -> 0`, so that term is `o(||h||)`. Second, `||k|| <= ||B|| ||h|| +
> ||r(h)||`, which is `O(||h||)`, and `s(k)/||k|| -> 0`, so `||s(k)||/||h|| =
> (||s(k)||/||k||)(||k||/||h||) -> 0` as well (when `k = 0` the term is zero and there is
> nothing to bound). Hence `f . g` is differentiable at `a` with derivative `A B`. **QED**
>
> The scalar chain rule of 0502 is the case `m = n = p = 1`, where the matrix product is
> a product of numbers.

**Theorem 2. The Jacobian determinant is the local volume factor.**

> Let `f : R^n -> R^n` be differentiable at `a`. Then for a small region `S` containing
> `a`, `vol(f(S)) / vol(S) -> |det J_f(a)|` as `S` shrinks to `a`.
>
> *Proof, stated at the level this course works at.* Near `a`, `f(x) = f(a) + J(x - a) +
> o(||x - a||)`. Dropping the remainder, `f` acts on the region as the affine map
> `x -> f(a) + J(x - a)`. A translation does not change volume, and the change-of-variables
> theorem for a linear map `J` multiplies volume by `|det J|`, which is the defining
> property of the determinant. The neglected remainder is `o` of the region's diameter,
> so its contribution to the volume ratio vanishes in the limit. **QED**
>
> The honest note: the linear-algebra fact that `|det J|` is the volume scaling of a
> linear map is M04's, and this page cites it rather than proving it again.

## Figures

1. **Orientation, `flowchart LR`.** "The chain rule for scalars (0502)" into "THIS PAGE:
   the chain rule for vectors" into "backpropagation (0507)" and "change of variables (M08)".
2. **`flowchart LR`.** Two composed maps `R^5 -> R^3 -> R^1` with the Jacobian shapes on
   the edges, `3 x 5` then `1 x 3`, and the composed shape `1 x 5` beneath.
   *Kills:* transpose-and-shape confusion, by making the shapes the visible content.
3. **`svg.chart`, quantitative.** A unit square with labelled corners mapped by
   `J = [[-2, 1], [1, 1]]` to a parallelogram, with `|det J| = 3` and both areas annotated.
   *Kills:* "the determinant is an algebra exercise".
4. **`sequenceDiagram`.** A cotangent vector travelling right to left through three
   operations, each returning `v^T J`, never building `J`.
   *Kills:* "autodiff computes the Jacobian".

## Worked example, in eight parts

1. **Setting.** One neural network layer, `tanh(W x + b)`, mapping `R^3 -> R^2`, composed
   with a second layer mapping `R^2 -> R^2`. Not an abstract map: this is what a network is.
2. **Symbolic.** `.math` for `J[i][j] = d f_i / d x_j` and for the composition rule, with
   a `.gloss` naming `i`, `j`, `m`, `n`, and saying which index is which.
3. **Picture.** Figure 2, the shapes, before any entry is computed.
4. **`ol.worked`.**
   - **Differentiate the first layer.** The tanh derivative `1 - tanh^2` scales each row
     of `W1`, giving a `2 x 3` matrix.
   - **Differentiate the second.** Same shape rule, giving `2 x 2`.
   - **Multiply.** `2 x 2` times `2 x 3` is `2 x 3`, which is the composed map's shape.
   - **Check against the definition.** Finite-difference the composed map directly.
   - **Take a vector-Jacobian product** two ways, once by building the product and once
     by accumulating right to left.
5. **`.keynum`** on nothing: derived here.
6. **Sanity check.** The composed Jacobian must be `2 x 3`, because the composed map takes
   three numbers and returns two. If the shapes do not chain, the multiplication order is
   wrong, and that is the error to look for first.
7. **What changes if** the second layer is widened to `R^2 -> R^7`? The composed Jacobian
   becomes `7 x 3` and the vector-Jacobian product needs a seven-entry `v`. Nothing about
   the method changes, which is the point of writing it as a matrix product.
8. **In words.** Composing two layers is multiplying two Jacobians, and the shape rule
   tells you the answer before you compute a single entry.

## Quiz seeds

**Q1.** For `f : R^m -> R^n`, what is the shape of the Jacobian?
*Answer:* `n x m`.
*Distractors:* `m x n` is the transpose and is the most common slip; `m x m` and `n x n`
each assume a square map.

**Q2, misconception.** Why does reverse-mode autodiff compute `v^T J` rather than
building `J`?
*Answer:* because `J` for a wide layer is enormous and every entry would be discarded
immediately after one multiplication.
*Distractors:* "because `J` is not computable" is false; "because `J` is not symmetric"
is true and irrelevant; "because `v^T J` is more accurate" is false, they agree to
machine precision, and the program measures the gap at `5.6e-17`.

## Practice seed

**Stem.** For the map `y1 = -2 x1 + x2`, `y2 = x1 + x2`: write the Jacobian, compute its
determinant, state what happens to the area of the unit square, then confirm the answer a
second way using the images of the two basis vectors.

**Hint.** The second route needs no calculus at all. Where do `(1,0)` and `(0,1)` land?

**Solution.** `J = [[-2, 1], [1, 1]]`, `det J = -3`, so areas are multiplied by
`|det J| = 3`. The basis vectors map to `(-2, 1)` and `(1, 1)`, which span a
parallelogram of area `|(-2)(1) - (1)(1)| = 3`.

**`.p-check`.** The two routes must agree, and a negative determinant is not an error:
the sign records that the map flips orientation, and only the magnitude scales area.

## Code and dataset

`../code/m05_06_jacobian.py`. No csv: the object is a map, and the program constructs the
two layers explicitly so the reader can change the weights and re-run.

Verified output to quote: the analytic product `J2 J1` agrees with a finite-difference
Jacobian of the composed map to `4.687e-11`; the vector-Jacobian product accumulated in
reverse agrees with building the product to `5.551e-17`; and for a square restriction of
the map, `|det J| = 0.019123`, with the measured area ratio of a shrinking square
converging `0.019191`, then `0.019124`, then `0.019123`.

## Sources

- Goodfellow, Bengio and Courville, *Deep Learning*, section 4.3.1 for the Jacobian's
  definition, and 6.5.2 for `grad_x z = (dy/dx)^T grad_y z` and the description of
  backpropagation as a Jacobian-gradient product per operation.
  `https://www.deeplearningbook.org/contents/numerical.html`,
  `https://www.deeplearningbook.org/contents/mlp.html`
- Deisenroth, Faisal and Ong, *Mathematics for Machine Learning*, section 5.3, including
  Example 5.8 whose `|det J| = 3` this page reuses, and the remark that the Jacobian
  determinant is the magnification factor for an area or a volume.
  `https://mml-book.github.io/book/mml-book.pdf`
