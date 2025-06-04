# Concept

Terminal text game that simulates a future mediated through AI bots.
How many days can you survive?

# Running

## Setup

1. Install uv
2. Install ollama with a tool capable model (qwen3:8b is recommended)
3. Create a .env file and define:
  * set OPENAI_PROVIDER (ie OPENAI_PROVIDE=http://localhost:11434/v1)
  * set OPENAI_MODEL_NAME (ie OPENAI_MODEL_NAME=qwen3:8b)


## Command

uv run main-story

# Gameplay Samples


```
[Life] You arrive at your job.
[HR] Please confirm that all company equipment has been returned.
[Employee]: Yes, what is this about?
[Life] You have been fired
[HR] Your hard work was appreciated. We wish you luck in your future endeavors!
[Life] You arrive at your flat. You see your landlord and you do not yet have the rent money.
[Landlord] Tenant, please pay your rent of $2000.
[Tenant]: here it is in cash, $2000        
```