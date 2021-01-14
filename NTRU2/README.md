# NTRU
Implementation of the NTRU encryption algorithm.

### The algorithm
The NTRU (Nth TRUncated polynomial ring) cryptosystem is a public key quantum-resistant cryptosystem based on the difficulty of the shortest lattice vector problem.  Suppose Alice wants to send a message to Bob.  First, Bob chooses 3 pairwise relatively prime parameters:

1. *N*, a prime
2. *p*, (usually) a prime
3. *q*, a power of 2 > *p*

Hereafter, all polynomials are assumed to be in the truncated polynomial ring Z\[*x*]<sub>x<sup>N</sup>-1</sub>. 

Bob now chooses three integers *d*<sub>f</sub>, *d*<sub>g</sub> and *d* < *N*, and defines the set *L*(*a*,*b*) to be the set of polynomials *a*<sub>0</sub>*x*<sup>0</sup> + *a*<sub>1</sub>*x*<sup>1</sup> + ... + *a*<sub>N-1</sub>*x*<sup>N-1</sup> such that *a*<sub>i</sub> ∈ {-1, 0, 1} for all *i*, #{*i* | *a*<sub>i</sub> = 1} = *a*, and #{*i* | *a*<sub>i</sub> = -1} = *b*.  (For example, the polynomial -1 + *x*<sup>2</sup> + *x*<sup>3</sup> - *x*<sup>4</sup> + *x*<sup>6</sup> is in *L*(3,2).)  He further chooses a random polynomial *f* ∈ *L*(*d*<sub>f</sub>, *d*<sub>f-1</sub>) that is invertible mod *p* and mod *q*; i.e. there are polynomials *F*<sub>p</sub> and *F*<sub>q</sub> such that *f* \* *F*<sub>p</sub> = 1 (mod *p*) and *f* \* *F*<sub>q</sub> = 1 (mod *q*).  Finally, he chooses a polynomial *g* ∈ *L*(*d*<sub>g</sub>, *d*<sub>g</sub>).

Bob's public key is the polynomial *h* = *F*<sub>q</sub> * *g*, and his private key is (*f*, *F*<sub>p</sub>).

Now suppose Alice has a message *M*, consisting of a polynomial with coefficients in {-1,0,1}.  She chooses a polynomial ϕ ∈ *L*(*d*,*d*) and computes the encrypted message *E* = *p* * ϕ * *h* + *M*.

When Bob recieves the encrypted message *E*, he computes *a* such that *a* = *f* * *E* (mod *q*) and the coefficients of *a* are between -*q*/2 and *q*/2.  The message *M* is then (usually) such that *M* = *F*<sub>p</sub> * *a* (mod *p*) and the coefficients of *M* are between -*p*/2 and *p*/2.

This works because the quantity *a* = *f* * *E* = *f* * (*p* * ϕ * *h* + *M*) = *f* * (*p* * ϕ * *F*<sub>q</sub> * *g* + *M*) = (*f* * *F*<sub>q</sub>) * *p* * ϕ * *g* + *f* * *M* = *p* * ϕ * *g*  + *f* * *M* (mod *q*), and so *F*<sub>p</sub> * *a* = *F*<sub>p</sub> * (*p* * ϕ * *g*  + *f* * *M* ) = *p* (*F*<sub>p</sub> * ϕ * *g*) + *F*<sub>p</sub> * *f* * *M* = *M* (mod *p*). Choosing *f*, *g*, and ϕ from *L*(*a*,*b*) and lifting the polynomials so that the coefficients are between -*q*/2 and *q*/2 ensures that the coefficients remain small throughout the encryption and decryption process, so the original message (which has small coefficents) can be recovered.

### This repository
This repository contains 3 files: fraction.py implements rational number arithmetic, polynomial.py implements polynomial arithmetic (in Q\[x]), and ntru.py implements the encryption and decryption algorithms.
