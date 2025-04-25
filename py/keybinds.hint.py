import subprocess
from pydantic import BaseModel, TypeAdapter

class KeyBind(BaseModel):
    locked: bool
    mouse: bool
    release: bool
    repeat: bool
    longPress: bool
    non_consuming: bool
    has_description: bool
    modmask: int
    submap: str
    key: str
    keycode: int
    catch_all: bool
    description: str
    dispatcher: str
    arg: str

    @property
    def mods(self):
        """
        Get the modifiers as a string.
        """
        mods = []
        if self.modmask & 0b00000001:
            mods.append("SHIFT")
        if self.modmask & 0b00000010:
            mods.append("CTRL")
        if self.modmask & 0b00000100:
            mods.append("SUPER")
        if self.modmask & 0b00001000:
            mods.append("ALT")
        return "+".join(mods)


key_bindings_adapter = TypeAdapter(list[KeyBind])


def get_hypr_keybinds():
    """
    Get the keybinds from Hyprland configuration.
    """

    with open("output.json", "w") as f:
        json_string = subprocess.run("hyprctl binds -j", stdout=f, text=True, shell=True).stdout
    
    with open("output.json", "r") as f:
        json_string = f.read()
    
    bindings = key_bindings_adapter.validate_json(json_string)

    rofi_choices = map(lambda b: f"{b.mods} + {b.key} | {b.description} | {b.description} | {b.arg}", bindings)
    rofi_choices_str = "\n".join(rofi_choices)

    selected = subprocess.run(f"echo '{rofi_choices_str}' | rofi -dmenu -p 'Select Hyprland keybinding:' -format i", capture_output=True, text=True, shell=True)

    if selected is None or selected.stdout == "":
        return
    
    binding = bindings[int(selected.stdout)]

    print(f"Selected binding: {binding.dispatcher} {binding.arg}")

    subprocess.run(f"hyprctl dispatch '{binding.dispatcher}' '{binding.arg}'", shell=True)

get_hypr_keybinds()