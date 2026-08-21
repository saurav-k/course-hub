# Route scope: By capability ladder

**Route id:** `capability`
**Sections:** 6
**Pages:** 47 deep dives

## What this route is

Six rungs.
Each is one thing machines learned to do, in the order they learned it.

| Rung | What became possible |
|---|---|
| 01 Machines that pattern-match | Produce and transform language without any model of meaning |
| 02 Machines that represent meaning | Put a word somewhere, so that similarity became measurable |
| 03 Machines that attend | Connect any part of an input to any other part, in one step |
| 04 Machines that scale, in both directions | Forecast what a bigger run buys, and then make the result cheap enough to use |
| 05 Machines that follow | Do what they were asked rather than continue what they were given |
| 06 Machines that reason and act | Spend more computation on a harder question, and reach outside themselves |

## Where it differs from the other routes

This is the route that reorders rather than only regrouping.

- **Tokenization moves up.** The lesson on how text becomes numbers sits in rung 02, next to word embeddings, rather than in its chronological slot beside GPT-2. Under this lens it belongs with representation: it is the other half of the answer to "what does the model actually see".
- **The efficiency cluster joins rung 04.** Adapters, serving, mixture of experts, sparse attention and long context sit with scaling laws, because learning to scale down is the same capability as learning to scale up, learned second.

Those two moves are what make this a fourth route rather than a renaming of the first.
The other routes keep the pool in its canonical order.

## What it deliberately leaves out

- **The ten spine chapters.** A capability ladder is already a compression; two compressions in one reading is one too many.
- **A claim that the rungs are discrete.** They overlap by years. The claim is about the order in which each became something you could rely on, not about the moment it was invented.
- **A claim that the ladder is complete.** Rung 06 is in progress, and the pool's last lesson is a register of open questions rather than a rung 07.

## The known compromise

**Not every lesson in the pool is about a capability.**
The lessons about people, money, licences, disclosure and how to read a benchmark are about the ground the ladder stands on, and there is no honest rung for them.

They ride in the rung whose era they belong to, and this route says so rather than pretending otherwise:

- The institutional lesson on 2014 to 2017 sits in rung 03.
- Disclosure, evaluation, the leak and the four axes of open sit in rung 05, the era in which they happened.

A future editor might prefer a seventh section for them.
That would be a defensible change and it would break the route's own promise that every section is a thing machines learned to do, so it should be argued for explicitly rather than done quietly.

## Who it is for

Someone who wants to be able to say what a model can do and when that became true.
It is the best route for a reader who is going to be asked "could it do X in year Y", and the best route for someone deciding what is worth building on.

It is a poor route for causation, which is `constraint`, and a poor route for a first pass, which is `spine`.

## How to extend it

Place a new lesson on the rung whose capability it demonstrates, not the rung whose date it shares.
Ask: what could a machine do after this that it could not do before.

If the answer is "nothing, but it explains why something was possible", it is a context lesson, and it goes in the rung of its era with the others.

If a genuinely new rung appears, it goes at the bottom and it needs a one-line description in the table above that is a *capability*, phrased as a thing machines learned to do.
If you cannot phrase it that way, it is not a rung.
