"""Keybind configuration for intellisense."""

def set_intellisense_pred_view(keybind: str) -> str:
    """Set the keybind for the intellisense prediction view."""
    return f"Set-PSReadLineKeyHandler -Chord {keybind} -Function SwitchPredictionView"

def set_intellisense_accept(keybind: str) -> str:
    """Set the keybind for accepting the intellisense selection."""
    return f"Set-PSReadLineKeyHandler -Chord {keybind} -Function ForwardChar"