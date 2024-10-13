---
title: Test
---

# Test

Here's the typing rule for the lambda calculus

$$
\frac{
    \Gamma, x : A \vdash e : B
}{
    \Gamma \vdash \lambda x. e : A \to B
}
\quad
\frac{
    (x, A) \in \Gamma
}{
    \Gamma \vdash x : A
}
\quad
\frac{
    \Gamma \vdash f : A \to B \quad
    \Gamma \vdash v : A
}{
    \Gamma \vdash f(v) : B
}
$$

Something something sequent calculus.