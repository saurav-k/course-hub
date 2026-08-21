/* The route manifest for this course. Hand-authored, and the single source of
   truth for what the four routes contain.

   `pages` is identity: one entry per file in lessons/, keyed by file name.
   A route lists the same file names in its own order and grouping. A lesson
   therefore has one URL no matter which route reached it.

   outline.js turns the active route into the window.COURSE_OUTLINE that the
   shared rail in assets/hub.js renders. scripts/validate_site.py fails the
   pull request if this file and lessons/ disagree, if a route is missing a
   page of a kind it declares, or if a lesson's static pager does not match
   the route that owns it. See routes/README.md. */
window.COURSE_ROUTES = {
  "key": "llm-evolution",
  "title": "How Language Models Happened",
  "default": "constraint",
  "pages": {
    "0001-spine-before-the-machine-could-read.html": {
      "title": "Before the machine could read",
      "kind": "spine"
    },
    "0002-spine-when-meaning-became-geometry.html": {
      "title": "When meaning became geometry",
      "kind": "spine"
    },
    "0003-spine-the-bottleneck-and-attention.html": {
      "title": "The bottleneck, and the fix called attention",
      "kind": "spine"
    },
    "0004-spine-the-transformer-turn.html": {
      "title": "The Transformer turn",
      "kind": "spine"
    },
    "0005-spine-the-scaling-bet.html": {
      "title": "The scaling bet",
      "kind": "spine"
    },
    "0006-spine-teaching-a-model-to-be-useful.html": {
      "title": "Teaching a model to be useful",
      "kind": "spine"
    },
    "0007-spine-when-the-record-closed.html": {
      "title": "When the record closed",
      "kind": "spine"
    },
    "0008-spine-the-open-weights-turn.html": {
      "title": "The open-weights turn",
      "kind": "spine"
    },
    "0009-spine-making-it-cheap.html": {
      "title": "Making it cheap",
      "kind": "spine"
    },
    "0010-spine-the-reasoning-turn.html": {
      "title": "The reasoning turn, and where we are",
      "kind": "spine"
    },
    "0011-machines-that-talk-without-understanding.html": {
      "title": "Machines that talk without understanding",
      "kind": "pool"
    },
    "0012-the-statistical-turn.html": {
      "title": "The statistical turn: guessing the next word",
      "kind": "pool"
    },
    "0013-translation-without-a-linguist.html": {
      "title": "Translation without a linguist",
      "kind": "pool"
    },
    "0014-what-a-neural-network-actually-is.html": {
      "title": "What a neural network actually is",
      "kind": "pool"
    },
    "0015-backpropagation-and-the-two-winters.html": {
      "title": "Backpropagation, and the two winters",
      "kind": "pool"
    },
    "0016-sequences-memory-and-the-lstm.html": {
      "title": "Sequences, memory, and the LSTM",
      "kind": "pool"
    },
    "0017-the-year-the-hardware-caught-up.html": {
      "title": "2012: the year the hardware caught up",
      "kind": "pool"
    },
    "0018-meaning-as-a-direction-in-space.html": {
      "title": "Meaning as a direction in space",
      "kind": "pool"
    },
    "0019-sequence-to-sequence-and-the-bottleneck.html": {
      "title": "Sequence to sequence, and the eight thousand numbers",
      "kind": "pool"
    },
    "0020-attention-stop-compressing.html": {
      "title": "Attention: stop compressing",
      "kind": "pool"
    },
    "0021-attention-did-not-make-it-fast.html": {
      "title": "The other problem: attention did not make it fast",
      "kind": "pool"
    },
    "0022-who-was-in-the-room.html": {
      "title": "Who was in the room: labs, money, and machines, 2014 to 2017",
      "kind": "pool"
    },
    "0023-two-papers-one-day.html": {
      "title": "Two papers, one day",
      "kind": "pool"
    },
    "0024-the-transformer-drops-recurrence.html": {
      "title": "The Transformer: what dropping recurrence unlocked",
      "kind": "pool"
    },
    "0025-imagenet-for-words.html": {
      "title": "ImageNet for words: pretrain once, specialise later",
      "kind": "pool"
    },
    "0026-the-fork-gpt-1-and-bert.html": {
      "title": "The fork: GPT-1 and BERT",
      "kind": "pool"
    },
    "0027-tokens-how-text-becomes-numbers.html": {
      "title": "Tokens: how text becomes numbers",
      "kind": "pool"
    },
    "0028-gpt-2-and-the-bet-on-scale.html": {
      "title": "GPT-2 and the bet on scale",
      "kind": "pool"
    },
    "0029-where-the-data-actually-came-from.html": {
      "title": "Where the data actually came from",
      "kind": "pool"
    },
    "0030-the-model-they-would-not-release.html": {
      "title": "The model they would not release",
      "kind": "pool"
    },
    "0031-predicting-the-future-with-a-straight-line.html": {
      "title": "Predicting the future with a straight line",
      "kind": "pool"
    },
    "0032-gpt-3-and-learning-without-learning.html": {
      "title": "GPT-3, and learning without learning",
      "kind": "pool"
    },
    "0033-chinchilla-and-data-as-the-new-constraint.html": {
      "title": "Chinchilla, the correction, and data as the new constraint",
      "kind": "pool"
    },
    "0034-teaching-a-model-to-answer.html": {
      "title": "Teaching a model to answer",
      "kind": "pool"
    },
    "0035-chain-of-thought-prompting-becomes-a-lever.html": {
      "title": "Chain of thought: prompting becomes a lever",
      "kind": "pool"
    },
    "0036-a-text-box-changes-everything.html": {
      "title": "A text box changes everything",
      "kind": "pool"
    },
    "0037-the-disclosure-collapse.html": {
      "title": "The disclosure collapse",
      "kind": "pool"
    },
    "0038-reading-an-eval-table-like-a-scientist.html": {
      "title": "Reading an eval table like a scientist",
      "kind": "pool"
    },
    "0039-the-leak-that-started-an-ecosystem.html": {
      "title": "The leak that started an ecosystem",
      "kind": "pool"
    },
    "0040-four-axes-of-open.html": {
      "title": "Four axes of open: weights, code, data, licence",
      "kind": "pool"
    },
    "0041-who-ships-open-weights-now.html": {
      "title": "Who ships open weights now",
      "kind": "pool"
    },
    "0042-lora-and-qlora.html": {
      "title": "LoRA and QLoRA: fine-tuning for the rest of us",
      "kind": "pool"
    },
    "0043-serving-reality.html": {
      "title": "Serving reality: the cache, and what it costs",
      "kind": "pool"
    },
    "0044-mixture-of-experts-the-router.html": {
      "title": "Mixture of experts, part one: the router",
      "kind": "pool"
    },
    "0045-mixture-of-experts-why-it-is-hard.html": {
      "title": "Mixture of experts, part two: why it is hard",
      "kind": "pool"
    },
    "0046-sparsity-moves-to-attention.html": {
      "title": "Sparsity moves to attention",
      "kind": "pool"
    },
    "0047-why-a-small-model-beats-a-huge-one.html": {
      "title": "Why a small model now beats a huge one from 2020",
      "kind": "pool"
    },
    "0048-long-context-capacity-is-not-competence.html": {
      "title": "Long context: capacity is not competence",
      "kind": "pool"
    },
    "0049-thinking-is-just-more-tokens.html": {
      "title": "Thinking is just more tokens",
      "kind": "pool"
    },
    "0050-rewards-a-machine-can-check.html": {
      "title": "Rewards a machine can check",
      "kind": "pool"
    },
    "0051-what-did-not-work-and-why-that-matters.html": {
      "title": "What did not work, and why that matters",
      "kind": "pool"
    },
    "0052-post-training-after-ppo.html": {
      "title": "Post-training after PPO: three things deleted",
      "kind": "pool"
    },
    "0053-tools-protocols-and-the-agent-loop.html": {
      "title": "Tools, protocols, and the agent loop",
      "kind": "pool"
    },
    "0054-why-agents-are-a-systems-problem.html": {
      "title": "Why agents are a systems problem",
      "kind": "pool"
    },
    "0055-multimodality-and-the-model-as-an-interface.html": {
      "title": "Multimodality, and the model as an interface",
      "kind": "pool"
    },
    "0056-where-we-are-now.html": {
      "title": "Where we are now",
      "kind": "pool"
    },
    "0057-what-is-still-open.html": {
      "title": "What is still open, and what would change it",
      "kind": "pool"
    }
  },
  "extras": [
    {
      "title": "Glossary",
      "href": "reference/glossary.html"
    },
    {
      "title": "Chronicle",
      "href": "reference/chronicle.html"
    }
  ],
  "routes": [
    {
      "id": "constraint",
      "name": "By binding constraint",
      "blurb": "Seven eras, each named for the one thing that was holding the field back. Every section opens with the problem and closes with what solved it.",
      "kinds": [
        "pool"
      ],
      "sections": [
        {
          "n": "01",
          "title": "Rules",
          "lessons": [
            "0011-machines-that-talk-without-understanding.html",
            "0012-the-statistical-turn.html",
            "0013-translation-without-a-linguist.html"
          ]
        },
        {
          "n": "02",
          "title": "Meaning",
          "lessons": [
            "0014-what-a-neural-network-actually-is.html",
            "0015-backpropagation-and-the-two-winters.html",
            "0016-sequences-memory-and-the-lstm.html",
            "0017-the-year-the-hardware-caught-up.html",
            "0018-meaning-as-a-direction-in-space.html"
          ]
        },
        {
          "n": "03",
          "title": "Reach",
          "lessons": [
            "0019-sequence-to-sequence-and-the-bottleneck.html",
            "0020-attention-stop-compressing.html",
            "0021-attention-did-not-make-it-fast.html",
            "0022-who-was-in-the-room.html",
            "0023-two-papers-one-day.html",
            "0024-the-transformer-drops-recurrence.html",
            "0025-imagenet-for-words.html",
            "0026-the-fork-gpt-1-and-bert.html",
            "0027-tokens-how-text-becomes-numbers.html"
          ]
        },
        {
          "n": "04",
          "title": "Scale",
          "lessons": [
            "0028-gpt-2-and-the-bet-on-scale.html",
            "0029-where-the-data-actually-came-from.html",
            "0030-the-model-they-would-not-release.html",
            "0031-predicting-the-future-with-a-straight-line.html",
            "0032-gpt-3-and-learning-without-learning.html",
            "0033-chinchilla-and-data-as-the-new-constraint.html"
          ]
        },
        {
          "n": "05",
          "title": "Usefulness",
          "lessons": [
            "0034-teaching-a-model-to-answer.html",
            "0035-chain-of-thought-prompting-becomes-a-lever.html",
            "0036-a-text-box-changes-everything.html",
            "0037-the-disclosure-collapse.html",
            "0038-reading-an-eval-table-like-a-scientist.html"
          ]
        },
        {
          "n": "06",
          "title": "Cost",
          "lessons": [
            "0039-the-leak-that-started-an-ecosystem.html",
            "0040-four-axes-of-open.html",
            "0041-who-ships-open-weights-now.html",
            "0042-lora-and-qlora.html",
            "0043-serving-reality.html",
            "0044-mixture-of-experts-the-router.html",
            "0045-mixture-of-experts-why-it-is-hard.html",
            "0046-sparsity-moves-to-attention.html",
            "0047-why-a-small-model-beats-a-huge-one.html",
            "0048-long-context-capacity-is-not-competence.html"
          ]
        },
        {
          "n": "07",
          "title": "Thinking",
          "lessons": [
            "0049-thinking-is-just-more-tokens.html",
            "0050-rewards-a-machine-can-check.html",
            "0051-what-did-not-work-and-why-that-matters.html",
            "0052-post-training-after-ppo.html",
            "0053-tools-protocols-and-the-agent-loop.html",
            "0054-why-agents-are-a-systems-problem.html",
            "0055-multimodality-and-the-model-as-an-interface.html",
            "0056-where-we-are-now.html",
            "0057-what-is-still-open.html"
          ]
        }
      ]
    },
    {
      "id": "spine",
      "name": "Spine plus deep dives",
      "blurb": "Ten short chapters that tell the whole arc at low resolution, with no maths, readable in an evening. Each chapter is followed by the deep dives that zoom into it.",
      "kinds": [
        "spine",
        "pool"
      ],
      "sections": [
        {
          "n": "01",
          "title": "Before the machine could read",
          "lessons": [
            "0001-spine-before-the-machine-could-read.html",
            "0011-machines-that-talk-without-understanding.html",
            "0012-the-statistical-turn.html",
            "0013-translation-without-a-linguist.html"
          ]
        },
        {
          "n": "02",
          "title": "When meaning became geometry",
          "lessons": [
            "0002-spine-when-meaning-became-geometry.html",
            "0014-what-a-neural-network-actually-is.html",
            "0015-backpropagation-and-the-two-winters.html",
            "0016-sequences-memory-and-the-lstm.html",
            "0017-the-year-the-hardware-caught-up.html",
            "0018-meaning-as-a-direction-in-space.html"
          ]
        },
        {
          "n": "03",
          "title": "The bottleneck, and attention",
          "lessons": [
            "0003-spine-the-bottleneck-and-attention.html",
            "0019-sequence-to-sequence-and-the-bottleneck.html",
            "0020-attention-stop-compressing.html",
            "0021-attention-did-not-make-it-fast.html",
            "0022-who-was-in-the-room.html"
          ]
        },
        {
          "n": "04",
          "title": "The Transformer turn",
          "lessons": [
            "0004-spine-the-transformer-turn.html",
            "0023-two-papers-one-day.html",
            "0024-the-transformer-drops-recurrence.html",
            "0025-imagenet-for-words.html",
            "0026-the-fork-gpt-1-and-bert.html",
            "0027-tokens-how-text-becomes-numbers.html"
          ]
        },
        {
          "n": "05",
          "title": "The scaling bet",
          "lessons": [
            "0005-spine-the-scaling-bet.html",
            "0028-gpt-2-and-the-bet-on-scale.html",
            "0029-where-the-data-actually-came-from.html",
            "0030-the-model-they-would-not-release.html",
            "0031-predicting-the-future-with-a-straight-line.html",
            "0032-gpt-3-and-learning-without-learning.html",
            "0033-chinchilla-and-data-as-the-new-constraint.html"
          ]
        },
        {
          "n": "06",
          "title": "Teaching a model to be useful",
          "lessons": [
            "0006-spine-teaching-a-model-to-be-useful.html",
            "0034-teaching-a-model-to-answer.html",
            "0035-chain-of-thought-prompting-becomes-a-lever.html",
            "0036-a-text-box-changes-everything.html"
          ]
        },
        {
          "n": "07",
          "title": "When the record closed",
          "lessons": [
            "0007-spine-when-the-record-closed.html",
            "0037-the-disclosure-collapse.html",
            "0038-reading-an-eval-table-like-a-scientist.html"
          ]
        },
        {
          "n": "08",
          "title": "The open-weights turn",
          "lessons": [
            "0008-spine-the-open-weights-turn.html",
            "0039-the-leak-that-started-an-ecosystem.html",
            "0040-four-axes-of-open.html",
            "0041-who-ships-open-weights-now.html"
          ]
        },
        {
          "n": "09",
          "title": "Making it cheap",
          "lessons": [
            "0009-spine-making-it-cheap.html",
            "0042-lora-and-qlora.html",
            "0043-serving-reality.html",
            "0044-mixture-of-experts-the-router.html",
            "0045-mixture-of-experts-why-it-is-hard.html",
            "0046-sparsity-moves-to-attention.html",
            "0047-why-a-small-model-beats-a-huge-one.html",
            "0048-long-context-capacity-is-not-competence.html"
          ]
        },
        {
          "n": "10",
          "title": "The reasoning turn, and where we are",
          "lessons": [
            "0010-spine-the-reasoning-turn.html",
            "0049-thinking-is-just-more-tokens.html",
            "0050-rewards-a-machine-can-check.html",
            "0051-what-did-not-work-and-why-that-matters.html",
            "0052-post-training-after-ppo.html",
            "0053-tools-protocols-and-the-agent-loop.html",
            "0054-why-agents-are-a-systems-problem.html",
            "0055-multimodality-and-the-model-as-an-interface.html",
            "0056-where-we-are-now.html",
            "0057-what-is-still-open.html"
          ]
        }
      ]
    },
    {
      "id": "capability",
      "name": "By capability ladder",
      "blurb": "Six rungs, each one thing machines learned to do, in the order they learned it. The lessons about people, money and licences ride in the rung where they happened.",
      "kinds": [
        "pool"
      ],
      "sections": [
        {
          "n": "01",
          "title": "Machines that pattern-match",
          "lessons": [
            "0011-machines-that-talk-without-understanding.html",
            "0012-the-statistical-turn.html",
            "0013-translation-without-a-linguist.html"
          ]
        },
        {
          "n": "02",
          "title": "Machines that represent meaning",
          "lessons": [
            "0014-what-a-neural-network-actually-is.html",
            "0015-backpropagation-and-the-two-winters.html",
            "0016-sequences-memory-and-the-lstm.html",
            "0017-the-year-the-hardware-caught-up.html",
            "0018-meaning-as-a-direction-in-space.html",
            "0027-tokens-how-text-becomes-numbers.html"
          ]
        },
        {
          "n": "03",
          "title": "Machines that attend",
          "lessons": [
            "0019-sequence-to-sequence-and-the-bottleneck.html",
            "0020-attention-stop-compressing.html",
            "0021-attention-did-not-make-it-fast.html",
            "0022-who-was-in-the-room.html",
            "0023-two-papers-one-day.html",
            "0024-the-transformer-drops-recurrence.html",
            "0025-imagenet-for-words.html",
            "0026-the-fork-gpt-1-and-bert.html"
          ]
        },
        {
          "n": "04",
          "title": "Machines that scale, in both directions",
          "lessons": [
            "0028-gpt-2-and-the-bet-on-scale.html",
            "0029-where-the-data-actually-came-from.html",
            "0030-the-model-they-would-not-release.html",
            "0031-predicting-the-future-with-a-straight-line.html",
            "0032-gpt-3-and-learning-without-learning.html",
            "0033-chinchilla-and-data-as-the-new-constraint.html",
            "0042-lora-and-qlora.html",
            "0043-serving-reality.html",
            "0044-mixture-of-experts-the-router.html",
            "0045-mixture-of-experts-why-it-is-hard.html",
            "0046-sparsity-moves-to-attention.html",
            "0047-why-a-small-model-beats-a-huge-one.html",
            "0048-long-context-capacity-is-not-competence.html"
          ]
        },
        {
          "n": "05",
          "title": "Machines that follow",
          "lessons": [
            "0034-teaching-a-model-to-answer.html",
            "0035-chain-of-thought-prompting-becomes-a-lever.html",
            "0036-a-text-box-changes-everything.html",
            "0037-the-disclosure-collapse.html",
            "0038-reading-an-eval-table-like-a-scientist.html",
            "0039-the-leak-that-started-an-ecosystem.html",
            "0040-four-axes-of-open.html",
            "0041-who-ships-open-weights-now.html"
          ]
        },
        {
          "n": "06",
          "title": "Machines that reason and act",
          "lessons": [
            "0049-thinking-is-just-more-tokens.html",
            "0050-rewards-a-machine-can-check.html",
            "0051-what-did-not-work-and-why-that-matters.html",
            "0052-post-training-after-ppo.html",
            "0053-tools-protocols-and-the-agent-loop.html",
            "0054-why-agents-are-a-systems-problem.html",
            "0055-multimodality-and-the-model-as-an-interface.html",
            "0056-where-we-are-now.html",
            "0057-what-is-still-open.html"
          ]
        }
      ]
    },
    {
      "id": "era",
      "name": "By era",
      "blurb": "Straight chronology, six periods. The same lessons in the order the events happened, with nothing rearranged to make an argument.",
      "kinds": [
        "pool"
      ],
      "sections": [
        {
          "n": "01",
          "title": "Before the neural turn",
          "lessons": [
            "0011-machines-that-talk-without-understanding.html",
            "0012-the-statistical-turn.html",
            "0013-translation-without-a-linguist.html"
          ]
        },
        {
          "n": "02",
          "title": "The neural turn",
          "lessons": [
            "0014-what-a-neural-network-actually-is.html",
            "0015-backpropagation-and-the-two-winters.html",
            "0016-sequences-memory-and-the-lstm.html",
            "0017-the-year-the-hardware-caught-up.html",
            "0018-meaning-as-a-direction-in-space.html",
            "0019-sequence-to-sequence-and-the-bottleneck.html",
            "0020-attention-stop-compressing.html",
            "0021-attention-did-not-make-it-fast.html",
            "0022-who-was-in-the-room.html"
          ]
        },
        {
          "n": "03",
          "title": "The Transformer",
          "lessons": [
            "0023-two-papers-one-day.html",
            "0024-the-transformer-drops-recurrence.html",
            "0025-imagenet-for-words.html",
            "0026-the-fork-gpt-1-and-bert.html",
            "0027-tokens-how-text-becomes-numbers.html"
          ]
        },
        {
          "n": "04",
          "title": "Scale and alignment",
          "lessons": [
            "0028-gpt-2-and-the-bet-on-scale.html",
            "0029-where-the-data-actually-came-from.html",
            "0030-the-model-they-would-not-release.html",
            "0031-predicting-the-future-with-a-straight-line.html",
            "0032-gpt-3-and-learning-without-learning.html",
            "0033-chinchilla-and-data-as-the-new-constraint.html",
            "0034-teaching-a-model-to-answer.html",
            "0035-chain-of-thought-prompting-becomes-a-lever.html",
            "0036-a-text-box-changes-everything.html"
          ]
        },
        {
          "n": "05",
          "title": "Open and efficient",
          "lessons": [
            "0037-the-disclosure-collapse.html",
            "0038-reading-an-eval-table-like-a-scientist.html",
            "0039-the-leak-that-started-an-ecosystem.html",
            "0040-four-axes-of-open.html",
            "0041-who-ships-open-weights-now.html",
            "0042-lora-and-qlora.html",
            "0043-serving-reality.html",
            "0044-mixture-of-experts-the-router.html",
            "0045-mixture-of-experts-why-it-is-hard.html",
            "0046-sparsity-moves-to-attention.html",
            "0047-why-a-small-model-beats-a-huge-one.html",
            "0048-long-context-capacity-is-not-competence.html"
          ]
        },
        {
          "n": "06",
          "title": "The reasoning era",
          "lessons": [
            "0049-thinking-is-just-more-tokens.html",
            "0050-rewards-a-machine-can-check.html",
            "0051-what-did-not-work-and-why-that-matters.html",
            "0052-post-training-after-ppo.html",
            "0053-tools-protocols-and-the-agent-loop.html",
            "0054-why-agents-are-a-systems-problem.html",
            "0055-multimodality-and-the-model-as-an-interface.html",
            "0056-where-we-are-now.html",
            "0057-what-is-still-open.html"
          ]
        }
      ]
    }
  ]
};
