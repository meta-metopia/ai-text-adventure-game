from dataclasses import dataclass
from typing import List, Optional


@dataclass
class GameMessageWithSelections:
    """
    message without selections
    """
    message: str
    selections: List[str]


def get_selections(message: str) -> GameMessageWithSelections:
    """
    Get selections from message
    :param message:  to get selections from
    :return: message with selections
    """
    # Message is with format:
    # some text content
    # ---selections---
    # selection 1
    # selection 2
    # ---end selections---

    # split message into lines
    lines = message.splitlines()
    selections: List[str] = []
    message_without_selections = ""
    entered_selections = False

    # iterate over lines
    for line in lines:
        if entered_selections:
            # if we are in selections
            if line.strip() == "---end selections---":
                # if we reached end of selections
                entered_selections = False
            else:
                # if we are in selections
                selection = line.strip()
                if len(selection) > 0:
                    selections.append(selection)
        else:
            # if we are not in selections
            if line.strip() == "---selections---":
                # if we reached start of selections
                entered_selections = True
            else:
                # if we are not in selections
                message_without_selections += line

    return GameMessageWithSelections(message=message_without_selections, selections=selections)
