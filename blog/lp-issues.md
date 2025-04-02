---
title: Issues with Logic Programming
---

A programming language has to fix an execution strategy. For instance functional languages can be call-by-value, call-by-name, call-by need, imperative languages are typically always call-by-value, etc. I'm giving the call-by- family as a specific example here, but in general your language just needs some sort of execution semantics

A key property of a good execution semantics is that it makes good progress. That is to say, it generates infinite loops as rarely as possible. What does this mean? Consider the following lambda term

$$
(\lambda x y. x) \text{finite_value} \text{infinite_loop}
$$

We have the function $\lambda x y. x$, which takes two arguments and returns the first. We then apply this function to $\text{finite_value}$ and $\text{infinite_loop}$.

Using a call-by-value execution strategy, both arguments would first be executed and then passed to the function. This causes an infinite loop, because it means that we execute the $\text{infinite_loop}$ term! We say that in this case, call-by-value does not make good progress

Now let's consider a different execution strategy, call-by-name, in which a term is only executed once it is pattern-matched upon. In this case, executing the function makes better progress, returning $\text{finite_value}$! This is because the \text{infinite_loop} argument is never used, and so a call-by-need strategy will not try to execute it

Notice how in this case, one evaluation strategy is "worse" than another in terms of this progress metric in that it allows more useful programs to execute. For instance Haskell uses call-by-need, which we may exploit to write weird programs that would only result in infinite loops in a call-by-value language

Let's take this back to where we started: Logic programming.

What is logic programming's execution semantics? The answer is proof search, where we have a proposition P and attempt to find a proof for P -- P is a logic program. Proof search is extremely badly behaved as a execution semantics, in terms of the progress metric. It is extremely undecidable in that most cases outside very tightly-defined domains quickly result in infinite loops -- proof search, out of all the execution strategies out there, produces some of the most infinite loops in a practical execution semantics 

To alleviate this, logic programs use a very directed form of proof search that also may be compiled to somewhat efficient code, but these restrictions cause the language to lose the free-form, undirected, relational nature that we care about in the first place

Constraint logic programming seeks to improve on this by adding decidable domains to a bigger logic language. This helps in that it improve the amount of progress a program may make without compromising the expressivity of the language, but also means the language is not as general purpose as functional, imperative, or otherwise languages, because in order to make different programming tasks feasible in a manner that is "beautiful" for a logic program you must continually add different domains to suit that task, if there even exists a decidable domain for the task. Perhaps it is possible to encode your problem in a different domain, but then you have encoding overhead (both mental and efficiency-wise), which is again not an issue in general purpose languages where you don't have to ever worry about the progress metric of your program in the first place 