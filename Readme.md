# Ocarina of Time Randomizer - Reinforcement learning

Test project on the Zelda game: [Ocarina of Time Randomizer](https://ootrandomizer.com). The goal is to finish the traditional OoT Zelda game the fastest.

I wanted to use deep reinforcement learning to optimize path to use depending on the current objects the user posseses ( = the state).


## Generate Seeds
To train a deep learning we generally need tons of good data to make the model converge. The only data we need in this case are seed spoiler logs, the results of the randomization of the game detailing where each item is obtainable.

There exists two main ways to generate those:
- Through the official website: https://ootrandomizer.com/generator
- Programmatically (much faster) with the source code: https://github.com/OoTRandomizer/OoT-Randomizer/tree/Dev


### Programmatically
Clone the source code:
```sh
git clone https://github.com/OoTRandomizer/OoT-Randomizer.git
```

Go into it:
```sh
cd OoT-Randomizer
```

And launch the generation with:
```sh
python3 OoTRandomizer.py --settings_string <setttings-string>
```

The spoiler logs will be generated in the `Output` folder.

To speed up the generation, you use loops (bash) or directly in the code in `OoTRandomizer.py`. Faster solutions to compute only the spoiler logs exist and part of the code can be extracted for this.


### Settings
Default settings from website (Tournament S8): BSAWDNCAX2TB2WCHGAB3L62ANEBSAAAACAASAAAASK7CAAEAUJJASCAJXAAAJADSB4SHAEALV6WL7RANADKWLYAABAEZAAB6VCC2AQGAEGWDGB8AAACACEJGUBC



## Resources
This project contains a lot of resources linked to the game and its logic, items, locations, etc.

- items_pool: list of all items that can unlock checks with their respective upgrades. Each item is represented as (item name, maximum state number, initial state)
