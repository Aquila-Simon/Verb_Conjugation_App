def conjugate_て_form(verb, verb_type):
    # Semi Auto Conjugation Functions for each group of verbs
    def conjugate_て_ichidan(verb):
        # Takes ichidan verbs and replaces the る to て
        return verb[:-1] + "て"

    def conjugate_て_godan(verb):
        # Takes godan verbs and replaces the final character with the   appropriate て-form ending
        if verb.endswith(("う", "つ", "る")):
            return verb[:-1] + "って"
        elif verb.endswith(("む", "ぶ", "ぬ")):
            return verb[:-1] + "んで"
        elif verb == "行く":
            return "行って"
        elif verb == "いく":
            return "いって"
        elif verb.endswith("く"):
            return verb[:-1] + "いて"
        elif verb.endswith("ぐ"):
            return verb[:-1] + "いで"
        elif verb.endswith("す"):
            return verb[:-1] + "して"
        else:
            raise ValueError(f"Unknown godan verb ending for {verb}")

    def conjugate_て_irregular(verb):
        # Handles the two irregular verbs
        if verb == "する":
            return "して"
        elif verb == "来る":
            return "来て"
        elif verb == "くる":
            return "きて"
        else:
            raise ValueError(f"Unknown irregular verb: {verb}")

    if verb_type == "ichidan":
        return conjugate_て_ichidan(verb)
    elif verb_type == "godan":
        return conjugate_て_godan(verb)
    elif verb_type == "irregular":
        return conjugate_て_irregular(verb)
    else:
        raise ValueError(f"Unknown verb type: {verb_type}")
