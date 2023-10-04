# Test Driven Development with Barnsley's Fern

## Introduction

Barnsley's fern is a fractal structure that replicates real-life ferns. It is generated by applying a series of coordinate transformations to an initial point. 

For more details see the [Wikipedia page](https://en.wikipedia.org/wiki/Barnsley_fern)

Below is a fern consisting of one million points.

<img src="fern.png" alt="drawing" width="400"/>


## Learning aims

The aims of this project were to become familiar with the test and behavioural driven development processes (pytest & behave). 

## Learning outcomes

* First experience of developing code from scratch using BDD
* Use of Mock objects in pytest
* Use of fixture teardowns in pytest to "clean up" after tests
* Use of mutation testing mutmut
  
I found mutation testing to be a helpful learning experience, as the mutations are designed to expose weaknesses in code and tests. As such each mutant that survives teaches a basic principle of robust testing. 

From mutation testing I learnt that boundary/edge cases should be tested and that a good test probes the whole of a function/class, not just a single line.