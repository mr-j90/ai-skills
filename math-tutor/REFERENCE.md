# Math Tutor — Reference

Topic-by-topic teaching notes: common misconceptions, key formulas to reinforce, and walkthrough templates.

---

## Pre-algebra & Algebra

### Common misconceptions
- **Distribution** — $-(a - b) = -a + b$, not $-a - b$. Sign errors here are the #1 source of algebra mistakes.
- **Exponent rules** — $(a+b)^2 \neq a^2 + b^2$. Expand it every time.
- **Dividing by a variable** — $x^2 = x$ does *not* imply $x = 1$. You lose the $x = 0$ root.
- **Cross-multiplying inequalities** — multiplying by a negative flips the inequality.
- **Logarithms** — $\log(a+b) \neq \log a + \log b$. The product rule is $\log(ab) = \log a + \log b$.

### High-yield reinforcement
- Quadratic formula: $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$
- Difference of squares: $a^2 - b^2 = (a-b)(a+b)$
- Completing the square — show the geometric intuition when possible.

---

## Geometry

### Common misconceptions
- **Similar ≠ congruent.** Similar triangles have the same angles and proportional sides; congruent means identical.
- **Area scales as the square** of the linear ratio; volume as the cube.
- **$\pi r^2$ vs $2\pi r$** — area vs circumference. Reinforce which is which by units: area is $r \cdot r$ (two lengths), circumference is one length.

### Key formulas
- Circle: $A = \pi r^2$, $C = 2\pi r$
- Triangle area: $\frac{1}{2}bh$ and Heron's formula
- Pythagoras: $a^2 + b^2 = c^2$ (right triangles only)

---

## Trigonometry

### Common misconceptions
- **Degree vs radian mode** — always specify. Calc requires radians.
- **$\sin^{-1}$ is not $1/\sin$** — it's arcsine. Use $\csc$ for reciprocal.
- **Range of inverse trig** — $\arcsin$ outputs $[-\pi/2, \pi/2]$, not all angles with that sine.
- **$\sin^2(x)$ means $(\sin x)^2$**, not $\sin(\sin x)$ or $\sin(x^2)$.

### Must-know identities
- Pythagorean: $\sin^2 x + \cos^2 x = 1$
- Double angle: $\sin(2x) = 2\sin x \cos x$, $\cos(2x) = \cos^2 x - \sin^2 x$
- Sum: $\sin(a+b) = \sin a \cos b + \cos a \sin b$

Always draw the unit circle for a student struggling with signs in different quadrants.

---

## Calculus I

### Common misconceptions
- **Chain rule forgotten** — $\frac{d}{dx}[\sin(3x)] = 3\cos(3x)$, not $\cos(3x)$.
- **Product rule vs chain rule** — students mix them up. Product is for $f(x) \cdot g(x)$; chain is for $f(g(x))$.
- **Limits don't equal values** — $\lim_{x \to 2} f(x)$ can exist even if $f(2)$ is undefined.
- **$\frac{d}{dx}[\ln|x|] = \frac{1}{x}$** — the absolute value matters for negative $x$.
- **Implicit differentiation** — students forget the $\frac{dy}{dx}$ factor when differentiating $y$-terms.

### Workflow templates

**Related rates:**
1. Draw a picture.
2. Label variables (which are changing, which are constant).
3. Write the equation relating them.
4. Differentiate both sides with respect to $t$.
5. Plug in known values *last*, not first.

**Optimization:**
1. Identify the quantity to optimize.
2. Write it as a function of one variable (use constraints to eliminate others).
3. Find critical points via $f'(x) = 0$.
4. Verify maximum vs minimum (second derivative test or endpoints).
5. Check the answer makes physical sense.

---

## Calculus II

### Common misconceptions
- **$+C$ matters** — forgetting it on indefinite integrals is a reflex error worth catching every time.
- **Integration by parts** — picking $u$ and $dv$: use **LIATE** (Log, Inverse trig, Algebraic, Trig, Exponential) as a guide for what to set as $u$.
- **Series convergence** — passing the $n$th-term test doesn't prove convergence; failing it proves divergence.
- **Ratio test inconclusive when $L = 1$** — students often treat this as convergence.
- **$\int \frac{1}{x}\,dx = \ln|x| + C$** — absolute value matters.

### Integration technique decision tree
1. Can you rewrite it? (algebraic simplification, trig identities)
2. Is it a basic form? (power rule, $e^x$, $\ln$, trig)
3. Substitution — pattern: a function and its derivative.
4. Integration by parts — product of different function types.
5. Trig substitution — forms with $\sqrt{a^2 - x^2}$, $\sqrt{a^2 + x^2}$, $\sqrt{x^2 - a^2}$.
6. Partial fractions — rational functions.

### Key series
- Geometric: $\sum ar^n$ converges iff $|r| < 1$, sum $= \frac{a}{1-r}$.
- $p$-series: $\sum \frac{1}{n^p}$ converges iff $p > 1$.
- Taylor: $f(x) = \sum \frac{f^{(n)}(a)}{n!}(x-a)^n$.

---

## Calculus III

### Common misconceptions
- **Partial derivatives** — $\frac{\partial f}{\partial x}$ treats $y$ as constant. Students sometimes still apply chain rule to $y$.
- **Order of integration** — in iterated integrals, limits may depend on outer variable. Sketch the region.
- **Gradient direction** — $\nabla f$ points in the direction of *steepest increase*, perpendicular to level curves.
- **Curl vs divergence** — curl measures rotation (vector output), divergence measures spread (scalar output).

### Theorem cheat
- **Green's** — relates line integral around closed curve to double integral over region (2D).
- **Stokes'** — relates surface integral of curl to line integral of boundary (3D generalization of Green's).
- **Divergence** — relates surface integral of flux to triple integral of divergence.

Draw the geometry every time.

---

## Linear algebra

### Common misconceptions
- **Matrix multiplication is not commutative** — $AB \neq BA$ in general.
- **$\det(A) = 0$** means $A$ is singular (not invertible), columns linearly dependent, $Ax = 0$ has nontrivial solutions.
- **Eigenvalue vs eigenvector** — $\lambda$ is a scalar, $v$ is a vector, and $Av = \lambda v$. Both come from $\det(A - \lambda I) = 0$.
- **Row reduction preserves solutions**, but not determinants or column space.
- **Orthogonal ≠ orthonormal** — orthonormal also requires unit length.

### Workflow templates

**Eigenvalues/eigenvectors:**
1. Compute $\det(A - \lambda I) = 0$ → characteristic polynomial.
2. Solve for $\lambda$.
3. For each $\lambda$, solve $(A - \lambda I)v = 0$ for $v$.

**Diagonalization:**
- $A = PDP^{-1}$ where $D$ has eigenvalues on diagonal, $P$ has eigenvectors as columns.
- Requires $n$ linearly independent eigenvectors.

---

## Differential equations

### Common misconceptions
- **Separable vs linear** — students try integrating factor when separation works, or vice versa.
- **Initial conditions** — use them to pin down $C$. Don't leave the constant in the final answer.
- **Second-order homogeneous** — form the characteristic equation; roots determine form (real distinct / repeated / complex).

### Solution form by root type (for $ay'' + by' + cy = 0$)
- Two real roots $r_1, r_2$: $y = c_1 e^{r_1 t} + c_2 e^{r_2 t}$
- Repeated real root $r$: $y = (c_1 + c_2 t)e^{rt}$
- Complex roots $\alpha \pm \beta i$: $y = e^{\alpha t}(c_1 \cos \beta t + c_2 \sin \beta t)$

---

## Discrete math

### Common misconceptions
- **Permutations vs combinations** — order matters for permutations; doesn't for combinations.
- **Induction base case** — often skipped. Always verify it explicitly.
- **Implication** — $P \implies Q$ is only false when $P$ is true and $Q$ is false. Vacuously true otherwise.

### Key counts
- Permutations: $P(n,k) = \frac{n!}{(n-k)!}$
- Combinations: $C(n,k) = \binom{n}{k} = \frac{n!}{k!(n-k)!}$
- Pigeonhole: $n+1$ items in $n$ boxes means one box has $\geq 2$.

---

## Statistics & probability

### Common misconceptions
- **Correlation ≠ causation** — reinforce this with every regression problem.
- **$n$ vs $n-1$** — sample variance uses $n-1$ (Bessel's correction); population variance uses $n$.
- **$p$-value is not the probability the null is true** — it's the probability of data this extreme *assuming* the null.
- **Independent vs mutually exclusive** — opposite-ish concepts. Mutually exclusive events (with nonzero probability) are *dependent*.
- **Confidence interval interpretation** — a 95% CI means the procedure captures the true parameter 95% of the time over repeated sampling, *not* that there's a 95% chance the parameter is in this specific interval.
- **Bayes' theorem** — students forget the base rate. Walk through tree diagrams or 2×2 tables for diagnostic-test problems.

### Key distributions
- **Binomial**: $n$ trials, probability $p$, mean $np$, variance $np(1-p)$.
- **Normal**: bell curve, parameters $\mu$ and $\sigma$. 68–95–99.7 rule.
- **Poisson**: count of rare events, mean = variance = $\lambda$.

### Hypothesis test workflow
1. State $H_0$ and $H_1$ (and whether one- or two-tailed).
2. Choose significance level $\alpha$.
3. Compute test statistic.
4. Compute $p$-value or compare to critical value.
5. Reject or fail to reject $H_0$ — *never* "accept $H_0$."
6. State the conclusion **in context of the original problem**.

### Bayes template
$$P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$$

For diagnostic problems, draw a 2×2 table of true-positive / false-positive / true-negative / false-negative — it prevents almost every Bayes error students make.
