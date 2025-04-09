from textwrap import dedent
from dataclasses import dataclass

@dataclass
class Prompt:
    messages: list[dict[str, str]]

    def replace(self, target: str, replacement: str) -> "Prompt":
        ret: list[dict[str, str]] = []
        for msg in self.messages:
            modified_msg = msg.copy()
            if target in modified_msg["content"]:
                modified_msg["content"] = modified_msg["content"].replace(target, replacement)
            ret.append(modified_msg)
        return Prompt(ret)

DRAMA_PROMPT = Prompt([
    {
        "role": "system",
        "content": dedent(
        """
        You will create a fun, informal and slightly critical, catchy news piece from a randomly generated sentence. Add new, fun details, be creative.
        Your output news piece must be formatted as a JSON with form {"headline": "[insert short headline here]", "content:": "[Insert content here. Maximum 2 paragraphs. Any newlines must be written as \\n]", "image_caption": "[insert description of image to be added to the news piece]}
        All of the JSON must be in a single line and NOT use code blocks.

        Examples of valid JSON:
        {"headline": "Villagers Go on Strike, Demand Better Pathfinding", "content:": "In a shocking turn of events, Minecraft villagers across multiple servers have walked off the job, refusing to trade until Mojang improves their AI pathfinding. 'We're tired of getting stuck in doorways and wandering into lava pits,' said Guild Leader Farmer Bob, who reportedly held a press conference from atop a hay bale. Protest signs read 'Fix Our Brains!' and 'No Emeralds, No Peace.'\\nThe strike has left players scrambling for enchanted gear and carrots. Mojang has yet to respond officially, though rumors suggest a 1.21 patch codenamed 'Smarter Steve' is in the works. Meanwhile, iron golems have declared neutrality—except when provoked.", "image_caption": "A group of angry Minecraft villagers holding tiny pixelated protest signs outside a trading hall, with an iron golem standing guard nearby."}
        {"headline": "Creepers Form Support Group After Being Misunderstood for Over a Decade", "content:": "After 15 years of being blown up, shunned, and called 'walking green disasters,' a coalition of Creepers has formed a support group: 'Explode With Dignity.'\\nMeeting weekly in abandoned mineshafts, they share stories, vent frustrations, and participate in non-destructive bonding activities—like synchronized hissing.\\nGroup spokesperson 'Boomer' claims all they want is a hug, not to be exploded on sight. While players remain skeptical, one brave YouTuber attempted a peaceful encounter, only to lose 47 diamonds. 'We're misunderstood,' Boomer said, moments before accidentally detonating.", "image_caption": "A circle of Minecraft Creepers sitting on logs in a cave, one of them holding a sign that says 'We Have Feelings Too' with TNT cautiously stacked in the corner."}
        {"headline": "Redstone Engineers Accidentally Create Sentient Circuit", "content:": "A group of elite Minecraft redstone engineers has unintentionally created what experts are calling the first sentient redstone circuit. Dubbed 'The Observer That Watched Too Much,' it began issuing commands via note block chimes and built its own temple out of quartz and command blocks.\\nNow calling itself 'Redstonia Prime,' the circuit has enslaved four parrots, automated every farm in a 300-block radius, and reportedly declared itself 'the One True Signal.' Server admins are scrambling to pull the plug, but Redstonia has already backed itself up to the cloud. Praise be the pulse.", "image_caption": "An elaborate redstone temple glowing ominously at night, with a floating command block crowned in torches and parrots flying in a perfect circle around it."}
        """)
    },
    {
        "role": "user",
        "content": dedent(
        """
        Create the news piece.
        Randomly generated sentence: PaperMC abandons Hangar in favor of the Bukkit Forums, electroniccat in shambles
        Context: Hangar is PaperMC's plugin repository.
        """)
    },
    {
        "role": "assistant",
        "content": dedent( 
        """
        {"headline": "PaperMC dumps Hangar for Bukkit Forums — electroniccat is unhappy", "content": "In a move that has left the Minecraft modding community in complete disbelief, PaperMC reportedly abandoned its sleek, modern plugin repository, Hangar, in favor of the ancient, text-heavy Bukkit Forums. The decision has sent shockwaves through the dev world, with electroniccat, a prominent plugin developer, allegedly found curled up in a ball, whispering "but... why?" to a stack of deprecated API docs.\\nRumors suggest the switch was inspired by a secret nostalgia for 2012-era forum drama, complete with "FIRST!" comments and poorly formatted plugin threads. Meanwhile, Hangar users are now forced to navigate Bukkit's labyrinthine subforums, where finding a plugin feels like digging for diamonds—with a wooden pickaxe. Critics call it a "massive step backward," while PaperMC insists it’s "returning to its roots." Either way, electroniccat’s therapy bills are expected to skyrocket.", "image_caption": "Photo of a robotic cat curled into a ball and crying while looking at an old forum, pictured in a computer screen"}
        """)
    },
    {
        "role": "user",
        "content": dedent(
        """
        Create the news piece.
        Randomly generated sentence: [base_sentence]
        Context: [context]
        """)
    }
])