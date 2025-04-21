import json


def ask_question(question, options):
    #Function to ask the question to the user.
    print("\n" + question)
    print("Options:", ", ".join(options))
    response = input("Your answer: ").strip()
    #Validating the user input to be one of the options given.
    #If the user input is not one of the options, it will ask again until a valid option is given.
    while response not in options:
        print("Invalid option. Try again.")
        response = input("Your answer: ").strip()
    return response

def filter_pokemons(candidates, attribute, value):
    #Function to filter the candidates list based on the user input.
    #It will return a list of pokemons that match the attribute and value given.
    return [p for p in candidates if p.get(attribute) == value]

def apply_inference_rules(pokemons, respuestas):
    #Function to apply the inference rules to the candidates list.
    #It will return a list of pokemons that match the rules given.
    candidatos = []

    for p in pokemons:
        # R1–R3: Gen + Región
        if respuestas.get("generation") and respuestas.get("region"):
            # R1: If H1 = Gen I and H2 = Kanto, then the Pokémon is from the first generation.
            if respuestas["generation"] == "Gen I" and respuestas["region"] == "Kanto":
                if p["generation"] == "Gen I" and p["region"] == "Kanto":
                    candidatos.append(p)
                    continue

            # R2: If H1 = Gen II and H2 = Johto, then the Pokémon is from the second generation.
            if respuestas["generation"] == "Gen II" and respuestas["region"] == "Johto":
                if p["generation"] == "Gen II" and p["region"] == "Johto":
                    candidatos.append(p)
                    continue

            # R3: If H1 = Gen III and H2 = Hoenn, then the Pokémon is from the third generation.
            if respuestas["generation"] == "Gen III" and respuestas["region"] == "Hoenn":
                if p["generation"] == "Gen III" and p["region"] == "Hoenn":
                    candidatos.append(p)
                    continue

        # R4: Fuego y Naranja → Charmander, Charmeleon, Charizard
        if p["type"] == "Fire" and p["color"] == "Orange":
            candidatos.append(p)

        # R5: Eléctrico y no evoluciona → Zapdos o Rotom
        if p["type"] == "Electric" and p["evolution"] == "No":
            candidatos.append(p)

        # R6: Dragón y evoluciona
        if "Dragon" in p["type"] and p["evolution"] == "Yes":
            candidatos.append(p)

        # R8: Evoluciona con piedra y tipo Eléctrico
        if "Stone" in p["evolution_method"] and "Electric" in p["type"]:
            candidatos.append(p)

        # R9: Evoluciona con amistad y tipo Normal
        if "Friendship" in p["evolution_method"] and "Normal" in p["type"]:
            candidatos.append(p)

        # R10: Alta velocidad y Eléctrico
        if p["stats"]["speed"] == "High" and "Electric" in p["type"]:
            candidatos.append(p)

        # R11: Alta defensa y Acero
        if p["stats"]["defense"] == "High" and "Steel" in p["type"]:
            candidatos.append(p)

    return candidatos

def calculate_match_score(pokemon, respuestas):
    """Calculate how many attributes of a Pokémon match the user's answers."""
    score = 0
    if pokemon["generation"] == respuestas.get("generation"):
        score += 1
    if pokemon["region"] == respuestas.get("region"):
        score += 1
    if pokemon["type"] == respuestas.get("type"):
        score += 1
    if pokemon["evolution"] == respuestas.get("evolution"):
        score += 1
    if pokemon["evolution_method"] == respuestas.get("evolution_method"):
        score += 1
    if pokemon["color"] == respuestas.get("color"):
        score += 1
    if pokemon["stats"]["speed"] == respuestas.get("speed"):
        score += 1
    if pokemon["stats"]["defense"] == respuestas.get("defense"):
        score += 1
    return score

def expert_system():
    # Loading the Pokémon data from the JSON file pokemons.json
    with open("pokemons.json", "r") as file:
        pokemons = json.load(file)
    # Storing the Pokemon data in the variable candidates (a dictionary)
    candidates = pokemons
    # Fetching the information from the candidates list to get the unique values for generation, region, type
    # evolution_method, color, speed and defense to use it in the questions below.
    # It is done to do it before the candidates list is filtered by the user answers.
    # This way, the user can see all the options available for each question.
    generations = sorted(set(p["generation"] for p in pokemons))
    regions = sorted(set(p["region"] for p in candidates))
    types = sorted(set(p["type"] for p in pokemons))
    evo_methods = sorted(set(p["evolution_method"] for p in candidates if p["evolution_method"]))
    colors = sorted(set(p["color"] for p in candidates))
    speeds = sorted(set(p["stats"]["speed"] for p in candidates))
    defenses = sorted(set(p["stats"]["defense"] for p in candidates))
    #Welcomening the user to the Pokémon Expert System
    print(
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⠋⠉⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⢀⡏⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣠⣤⣤⣤⣤⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⡏⠀⠀⠀⠀⢸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡤⠴⠒⠊⠉⠉⠀⠀⣿⣿⣿⠿⠋⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢀⡠⠼⠴⠒⠒⠒⠒⠦⠤⠤⣄⣀⠀⢀⣠⠴⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⣼⠿⠋⠁⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠀⣇⠔⠂⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⣀⡤⠖⠋⠁⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⢰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⠤⠒⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⢀⡟⠀⣠⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⢻⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⡤⠤⢴\n"
        "⠀⠀⠀⠀⠀⠀⣸⠁⣾⣿⣀⣽⡆⠀⠀⠀⠀⠀⠀⠀⢠⣾⠉⢿⣦⠀⠀⠀⢸⡀⠀⠀⢀⣠⠤⠔⠒⠋⠉⠉⠀⠀⠀⠀⢀⡞\n"
        "⠀⠀⠀⠀⠀⢀⡏⠀⠹⠿⠿⠟⠁⠀⠰⠦⠀⠀⠀⠀⠸⣿⣿⣿⡿⠀⠀⠀⢘⡧⠖⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠀\n"
        "⠀⠀⠀⠀⠀⣼⠦⣄⠀⠀⢠⣀⣀⣴⠟⠶⣄⡀⠀⠀⡀⠀⠉⠁⠀⠀⠀⠀⢸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠁⠀\n"
        "⠀⠀⠀⠀⢰⡇⠀⠈⡇⠀⠀⠸⡾⠁⠀⠀⠀⠉⠉⡏⠀⠀⠀⣠⠖⠉⠓⢤⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀\n"
        "⠀⠀⠀⠀⠀⢧⣀⡼⠃⠀⠀⠀⢧⠀⠀⠀⠀⠀⢸⠃⠀⠀⠀⣧⠀⠀⠀⣸⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⠃⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠈⢧⡀⠀⠀⠀⠀⠘⣆⠀⠀⠀⢠⠏⠀⠀⠀⠀⠈⠳⠤⠖⠃⡟⠀⠀⠀⢾⠛⠛⠛⠛⠛⠛⠛⠛⠁⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⠙⣆⠀⠀⠀⠀⠈⠦⣀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠙⢦⠀⠀⠘⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⢠⡇⠙⠦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠴⠋⠸⡇⠈⢳⡀⠀⢹⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⠀⡼⣀⠀⠀⠈⠙⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⣷⠴⠚⠁⠀⣀⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠀⠀⠀⡴⠁⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣆⡴⠚⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⣼⢷⡆⠀⣠⡴⠧⣄⣇⠀⠀⠀⠀⠀⠀⠀⢲⠀⡟⠀⠀⠀⠀⠀⠀⠀⢀⡇⣠⣽⢦⣄⢀⣴⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⡿⣼⣽⡞⠁⠀⠀⠀⢹⡀⠀⠀⠀⠀⠀⠀⠈⣷⠃⠀⠀⠀⠀⠀⠀⠀⣼⠉⠁⠀⠀⢠⢟⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⣷⠉⠁⢳⠀⠀⠀⠀⠈⣧⠀⠀⠀⠀⠀⠀⠀⣻⠀⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀⠀⠀⠏⠀⠀⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠹⡆⠀⠈⡇⠀⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀⠀⠀⠀⠀⠀⣸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⢳⡀⠀⠙⠀⠀⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⣰⠃⠀⠀⠀⠀⢀⡄⠀⢠⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⢳⡀⣰⣀⣀⣀⠀⠀⠀⠘⣦⣀⠀⠀⠀⡇⠀⠀⠀⢀⡴⠃⠀⠀⠀⠀⠀⢸⡇⢠⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
        "⠀⠀⠀⠉⠉⠀⠀⠈⠉⠉⠉⠙⠻⠿⠾⠾⠻⠓⢦⠦⡶⡶⠿⠛⠛⠓⠒⠒⠚⠛⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    )
    
    print("=================================================================================")
    print(
        "                                   ,'\\                                        \n"
        "    _.----.        ____         ,'  _\\   ___    ___     ____                \n"
        "_,-'       `.     |    |  /`.   \\,-'    |   \\  /   |   |    \\  |`.         \n"
        "\\      __    \\    '-.  | /   `.  ___    |    \\/    |   '-.   \\ |  |        \n"
        " \\.    \\ \\   |  __  |  |/    ,','_  `.  |          | __  |    \\|  |       \n"
        "   \\    \\/   /,' _`.|      ,' / / / /   |          ,' _`.|     |  |       \n"
        "    \\     ,-'/  /   \\    ,'   | \\/ / ,`.|         /  /   \\  |     |       \n"
        "     \\    \\ |   \\_/  |   `-.  \\    `'  /|  |    ||   \\_/  | |\\    |      \n"
        "      \\    \\ \\      /       `-.`.___,-' |  |\\  /| \\      /  | |   |       \n"
        "       \\    \\ `.__,'|  |`-._    `|      |__| \\/ |  `.__,'|  | |   |       \n"
        "        \\_.-'       |__|    `-._ |              '-.|     '-.| |   |       \n"
        "                                `'                            '-._|       \n"
    )
    print("=================================================================================")
    print("Welcome to the Pokémon Expert System!")
    print("Think of a Pokémon, and I'll try to guess which one it is...")


    respuestas = {}

    # 1. Generation

    gen = ask_question("Which generation is your Pokémon from?", generations)
    respuestas["generation"] = gen
    candidates = filter_pokemons(candidates, "generation", gen)

    # 2. Region

    reg = ask_question("Which region is your Pokémon from?", regions)
    respuestas["region"] = reg
    candidates = filter_pokemons(candidates, "region", reg)

    # 3. Type

    type_ = ask_question("What type is your Pokémon? (e.g. Fire, Electric)", types)
    respuestas["type"] = type_
    candidates = filter_pokemons(candidates, "type", type_)

    # 4. Evolves?
    evolution = ask_question("Does your Pokémon evolve? (Yes, No)", ["Yes", "No"])
    respuestas["evolution"] = evolution
    candidates = filter_pokemons(candidates, "evolution", evolution)

    # 5. Evolution method
    if evolution == "Yes":
        method = ask_question("How does your Pokémon evolve?", evo_methods)
        respuestas["evolution_method"] = method
        candidates = filter_pokemons(candidates, "evolution_method", method)

    # 6. Color

    color = ask_question("What is the dominant color of your Pokémon?", colors)
    respuestas["color"] = color
    candidates = filter_pokemons(candidates, "color", color)

    # 7. Speed

    speed = ask_question("What is its speed level? (High, Medium, Low)", speeds)
    respuestas["speed"] = speed
    candidates = [p for p in candidates if p["stats"]["speed"] == speed]

    # 8. Defense

    defense = ask_question("What is its defense level? (High, Medium, Low)", defenses)
    respuestas["defense"] = defense
    candidates = [p for p in candidates if p["stats"]["defense"] == defense]

    # Apply rule-based inference
    rule_candidates = apply_inference_rules(candidates, respuestas)

    #Final results
    final_candidates = list(set(p["name"] for p in rule_candidates))
    # Calculate match scores for all Pokémon
    scored_candidates = [
    (pokemon, calculate_match_score(pokemon, respuestas)) for pokemon in candidates
    ]
    # Filter out Pokémon with a score of 0 (no matches) and ensure the generation matches
    scored_candidates = [
        (pokemon, score) for pokemon, score in scored_candidates if score > 0 and pokemon["generation"] == respuestas["generation"]
    ]

    # Limit the results to the first 5 candidates
    scored_candidates = scored_candidates[:5]

    # Display results
    print("\nResults:")
    if len(final_candidates) == 1:
        print(f"\nI think your Pokémon is: {final_candidates[0]}!")
        
        play_again = ask_question("\nWould you like to try again? (Yes, No)", ["Yes", "No"])
        if play_again == "Yes":
            expert_system()  # Restart the system
        else:
            print("\nThank you for playing!")
    elif len(final_candidates) > 0:
        print("\nI couldn't find a total match. Here is a list of the 5 closests possibilities Pokémon:")
        for pokemon, score in scored_candidates:
            print(f"- {pokemon['name']} (Match Score: {score})")
        # Ask the user if they want to refine their answers
        play_again = ask_question("\nWould you like to refine your answers? (Yes, No)", ["Yes", "No"])
        if play_again == "Yes":
            expert_system()  # Restart the system
        else:
            print("\nThank you for playing!")
    else:
        print("\nI couldn't find a match. Maybe your Pokémon isn't our system yetS.")
        # Ask the user if they want to try again
        play_again = ask_question("\nWould you like to try again? (Yes, No)", ["Yes", "No"])
        if play_again == "Yes":
            expert_system()  # Restart the system
        else:
            print("\nThank you for playing!")

if __name__ == "__main__":
    expert_system()
