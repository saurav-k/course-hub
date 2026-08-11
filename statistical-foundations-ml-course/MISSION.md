# Mission

## Why this course exists

Rebuild university-level probability and statistics for a working software architect, from the ground up, with as close to zero cognitive load as the material allows.

The learner is a tech lead and architect.
He is strong in engineering and reasons fluently about systems, concurrency, and failure.
The gap is not intelligence and it is not mathematical maturity.
The gap is that the probability and statistics he learned at university has gone cold, and the notation now reads as friction rather than as meaning.

So this course optimises for one thing above all others: **the learner should never have to reconstruct a missing step.**
Every calculation is worked in full.
Every symbol is named in words before it is used in a formula.
Every idea arrives as a picture before it arrives as an equation.

## The source

The course follows the lecture series *Statistical Foundations of Machine Learning* taught at IIT Bombay by Nikhil Karamchandani (`nikhilk@ee.iitb.ac.in`) and D. Manjunath (`dmanju@ee.iitb.ac.in`).
Lecture 1 is dated Aug 11, 2026.
Course evaluation in the source is Homeworks 15, Midsem 15, Endsems 70.

The lecture deck is the spine.
This course is the expansion of that spine into something a person can learn from alone, without the lecturer in the room.

## Success looks like

The learner can:

- Say what question probability answers and what question statistics answers, and tell which one a business problem is asking.
- Choose between a mean and a median for a specific dataset, and defend the choice with the reason, not the habit.
- Take a real formula off a slide, name every symbol in it, and work it end to end on paper.
- Read a confidence interval and say what it does and does not claim.
- Look at a correlation coefficient and know how much weight it can carry.
- Open Lecture 2 without dread.

## Structure

The course nests three levels deep, because a lecture is too much for one sitting and a slide is too little for one page:

```
course  ->  lecture  ->  page
```

Each lecture gets a hub page that carries its logistics and links its parts in order.
Each part is one tight idea, sized to a single sitting, and ends by pointing at the next.
Lecture 1 is nine pages: a hub plus eight content parts.

## Constraints

- **Diagrams carry the teaching.** Every content page has at least three, and the course uses several distinct kinds. Mermaid draws structure; hand-authored inline SVG draws anything quantitative, because no diagram library can draw a distribution.
- **One colour, one meaning, every page.** Statistics is teal, probability is indigo, signal is green, noise is grey, and the thing that bites you is rust. The palette is the same on page one and page nine.
- **Every figure works in light and dark.** SVG colours come from CSS custom properties, never from a literal hex value.
- **Every number matches the deck.** Where the deck states a figure, this course states the same figure. It does not round it differently, re-derive it, or improve it.
- **Where the lecture is loose, say so.** An honest note about a limitation teaches more than a smooth explanation that hides one.
- Full prose, complete sentences, plain dash, never an em dash.

## Out of scope

- Measure-theoretic probability. The source course is an engineering course and so is this one.
- Proofs for their own sake. A proof appears when it is the clearest explanation available, not as a ritual.
- Machine learning itself. The title says *foundations of* machine learning: this is the probability and statistics that machine learning stands on. Models, training, and architectures belong to the other courses in this hub.
- Programming exercises. The learner already codes. Nothing here is blocked on writing a script.

## Revisit when

Lecture 2 is written.
At that point check whether nine pages per lecture is the right grain, or whether a shorter lecture should collapse into fewer.
