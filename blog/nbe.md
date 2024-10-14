---
title: You Could Have Invented Normalization-by-Evaluation
date: October 13, 2024
---

### Author's Note

This post only covers NbE from the _implementation_ perspective. The original formulation of NbE is a _proof technique_ used for properties of programming languages, and this use of NbE in implementation settings was derived from that. If you're interested, check out [Andreas Abel's habilitation](https://www.cse.chalmers.se/~abela/habil.pdf) for a comprehensive rundown of NbE as a proof technique.

---

## Introduction

If you're implementing some sort of dependently typed language, you've probably heard of normalization-by-evaluation, or NbE. Wikipedia describes NbE like this:

> In programming language semantics, normalization by evaluation (NBE) is a method of obtaining the normal form of terms in the λ-calculus by appealing to their denotational semantics.

That probably doesn't say much to you, so let's go over it in a more practical fashion.

## The Problem

Let's say you're implementing some sort of program that deals with equations, maybe a computer algebra system or something of the sort. For starters, you decide to implement a function that decides when two expressions are _equal_. For simplicity, we're only going to allow variables and addition in our expressions. Some examples:

$$
z + (x + y) = y + (x + z)
$$

$$
a + (b + c) = c
$$

$$
x = x + y
$$

Our program will take in a data structure representing these expressions as an input, and output a boolean telling us whether the expressions are equal or not. For instance on these three examples it should output `true`, `false`, `false`.

Let's go ahead and write out the pseudocode for the algorithm
```javascript
function equal(x, y) {
    if(x is Add(leftx, rightx)) {
        if(y is Add(lefty, righty)) {
            return equal(leftx, lefty) && equal(rightx, righty)
        }
    } else if(x is Var(namex)) {
        if(y is Var(namey)) {
            return namex == namey
        }
    }
    return false
}
```

Seems simple enough, we represent our expressions as trees, and `equal` just walks down the tree. This simple program doesn't work though!

$$
x + y = y + x
$$

In the above equation, the algorithm will fail even though the two sides of the equation are indeed equal -- the algorithm doesn't deal with _commutativity_.

Simple enough, let's just add a case into the program for that

```javascript
function equal(x, y) {
    if(x is Add(leftx, rightx)) {
        if(y is Add(lefty, righty)) {
            return
                equal(leftx, lefty) && equal(rightx, righty) ||
                equal(leftx, righty) && equal(lefty, rightx)
        }
    } else if(x is Var(namex)) {
        if(y is Var(namey)) {
            return namex == namey
        }
    }
    return false
}
```
Our algorithm now works for the commutativity example. But we're still not done! We need to deal with _associativity_, the fact that $x + (y + z) = (x + y) + z$. You probably get the point now -- what should be a simple program is turning into something very complicated. This is such a simple expression language and we're already running into this issue, imagine the explosion of rules there would be once we added nontrivial features like negation and multiplication.

## The Solution

The solution you would probably think of, without ever hearing about NbE, is to simplify your data structure. This isn't even something specific to evaluating expressions -- everywhere in CS changing your data structure is often the first thing you're recommended to try!

Let's first deal with associativity, what changes to our data structure can we make? Well in math we deal with associativity by just removing parenthesis completely. Instead of writing $x + (y + z)$ or $(x + y) + z$, we just write $x + y + z$. Can we reify this practice in our choice of data structure? Yes!

Instead of representing our expressions as trees, we'll represent them as _lists_. To convert our tree expressions to list expressions, we just flatten the trees.
```javascript
function flatten(expr) {
    if(expr is Var(name)) {
        return [name]
    } else if(expr is Add(x, y)) {
        return flatten(x) ++ flatten(y)
    }
}
```
Some examples at a REPL:
```javascript
> flatten(Add(Var("x"), Var("y")))                // x + y
["x", "y"]                                        // x + y
> flatten(Add(Var("x"), Add(Var("y"), Var("z")))) // x + (y + z)
["x", "y", "z"]                                   // x + y + z
> flatten(Add(Add(Var("x"), Var("y")), Var("z"))) // (x + y) + z
["x", "y", "z"]                                   // x + y + z
```

Now our equality function works with these list-based expressions instead of the tree-based expressions. Much simpler!
```javascript
function equal(x, y) {
    var x = flatten(x)
    var y = flatten(y)
    if(x.length != y.length) {
        // expressions have different number of variables
        // so we can say they're not equal
        return false
    } else {
        // expressions have same number of variables
        // so we compare each variable
        for(var i = 0; i < x.length; i++) {
            if(x[i] != y[i]) {
                return false
            }
        }
    }
    return true
}
```
And now our equality function works on these sorts of equations:

$$
x + (y + z) = (x + y) + z
$$

$$
x + ((y + z) + w) = (x + y) + (z + w)
$$

It will correctly return `true` on both.

Now let's deal with commutativity -- the fact that $x + y = y + x$. What's another simple change to our data structure that will make this easy? One solution: We sort the list! The change to our `equal` function is simple:
```javascript
function equal(x, y) {
    var x = flatten(x)
    x.sort() // add call to sort
    var y = flatten(y)
    y.sort() // add call to sort
    if(x.length != y.length) {
        // expressions have different number of variables
        // so we can say they're not equal
        return false
    } else {
        // expressions have same number of variables
        // so we compare each variable
        for(var i = 0; i < x.length; i++) {
            if(x[i] != y[i]) {
                return false
            }
        }
    }
    return true
}
```

Our code now correctly decides equality of expressions with addition, and obeys the associative and commutative laws correctly. All in very simple program! If you're ever done this sort of thing -- adding a preprocessing step to your expression or program data structure to make some function easier to implement -- then you've essentially done NbE.

## NbE in Practice

Congratulations! You just reinvented NbE. This is the meat of NbE -- adding a preprocessing step in between your data structure and your function that _transforms_ the original data structure into a new one, where the new one is easier for the function to work with. This intermediate data structure is called a **normal form**, and the preprocessing step is called **evaluation**.

Anyway, a person more familiar with the standard practice of NbE would have reorganized our code into this shape:
```javascript
function flatten(expr) {
    if(expr is Var(name)) {
        return [name]
    } else if(expr is Add(x, y)) {
        return flatten(x) ++ flatten(y)
    }
}

function evaluate(expr) {
    var flat_expr = flatten(expr);
    flat_expr.sort();
    return flat_expr;
}

function equalAux(x, y) {
    if(x.length != y.length) {
        return false
    } else {
        for(var i = 0; i < x.length; i++) {
            if(x[i] != y[i]) {
                return false
            }
        }
    }
    return true
}

function equal(x, y) {
    return equalAux(evaluate(x), evaluate(y))
}
```

All we've done is split out the steps more cleanly -- we have the `evaluate` function that transforms our original data structure into our normal form (lists of sorted variables), we have an `equalAux` function that works with our normal form, and we have the `equal` runner function that combines all these steps.

In a programming language for instance, we would see these same steps, except that the original data structure is a tree representing _lambda terms_. The evaluation function that partially normalizes these lambda terms into a form that is easy for equality checking and other functions to work with.

A function we did not implement, but that you would probably need, is called **reification**. This function takes the normal form and transforms it back into the original data structure. This would be needed say for instance, if you wanted to print back the expressions to the user. You don't want to expose the gory details of your internal normal form data structure to the user, so you instead expose this "`reify`" function. Here's the code:
```javascript
function reify(x) {
    var new_x = Var(x[0])
    for(var i = 1; i < x.length; i++) {
        new_x = Add(new_x, x[i])
    }
}
```
```javascript
> reify(["x", "y", "z"])                 // x + y + z
Add(Add(Var("x"), Var("y")), Var("z"))   // (x + y) + z
```
You could write a better version of this function, but it works well enough.

## Conclusion

Anyway, in conclusion, you could have invented NbE! It's a fairly simple technique that just happens to have some domain-specific terminology around it because of the theory it is founded in. I won't go over the theory here, but maybe I will in a future post. Bye!