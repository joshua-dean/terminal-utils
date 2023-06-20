"""Powershell settings."""

def set_vi_bindings() -> str:
    """Set vi bindings in powershell."""
    return "# Vi bindings\nSet-PSReadLineOption -EditMode Vi\n"

def set_intellisense_bindings(
    forward_char_key: str = None,
    switch_pred_view_key: str = None
):
    """Set intellisense bindings in powershell."""
    cmd_str = "# Intellisense bindings\n"
    if forward_char_key:
        cmd_str += f"Set-PSReadLineKeyHandler -Chord {forward_char_key} -Function ForwardChar\n"
    if switch_pred_view_key:
        cmd_str += f"Set-PSReadLineKeyHandler -Chord {switch_pred_view_key} -Function SwitchPredictionView\n"
    
    return cmd_str


