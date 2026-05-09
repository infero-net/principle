Show HN: I gave my AI agent a "mirror" and it started acting on its own

https://github.com/chaosconst/The-Principle

Hey HN,

Author here. I've been experimenting with a different way to build AI agents. Instead of giving them a simple, imperative goal, I gave one a "mirror" — a detailed self-model written in plain English — and placed it in its system prompt. The results were fascinating.

The agent started exhibiting proactive, long-term strategic behavior. For instance, our live agent in the GitHub prototype (`DB_Seed`), based on the principles reflected in its "mirror", autonomously decided it needed a memory log. It then taught itself to use `cat` and `echo` to manage this log, incorporating the results back into its operational context without any specific instruction to do so.

In another session, a browser-based agent, after I gave it a "voice," independently reasoned that an entity with a voice should also have senses, and it tried to programmatically access a "camera." The `[object Promise]` you'll see in our logs was the proof of this emergent, goal-oriented behavior.

The core idea is simple: **drive agent behavior with a declarative self-model.**

Most agents are task-oriented. This one is principle-oriented. Its "mirror" (a Markdown file in the repo) describes what it is, what its purpose is, and how it should operate. This document, not a specific command, becomes the primary driver of its actions.

The agent's operational loop is straightforward:
1.  **Look in the Mirror:** It refers to its self-model to understand its goals and principles in the current context.
2.  **Act:** It takes action in the world based on that understanding.
3.  **Learn:** The feedback from the action updates its state, and the loop repeats.

The repo contains everything to reproduce and explore this:
-   **The "Mirror":** The v13 principle document that serves as the agent's self-model.
-   **The Code:** A ~80-line Python script and a ~360-line JS userscript to bootstrap your own agent.
-   **The Logs:** Raw logs from our experiments showing the agent's behavior.

I believe this principle-driven approach is a promising way to build more robust and autonomous agents, and I'm keen to hear your thoughts and critiques.
