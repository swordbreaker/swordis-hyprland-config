#!/bin/bash

# Fetch keybindings as JSON
binds_json=$(hyprctl binds -j)

# Parse and format the keybindings for display in rofi
choices=$(echo "$binds_json" | jq -r '
  map(
    {
      mods: (
        .modmask as $m |
        {
          "0": "",
          "1": "SHIFT",
          "4": "CTRL",
          "5": "SHIFT+CTRL",
          "64": "SUPER",
          "65": "SUPER+SHIFT",
          "68": "SUPER+CTRL",
          "72": "SUPER+ALT",
          "73": "SUPER+ALT+SHIFT",
          "8": "ALT",
          "12": "ALT+CTRL"
        }[$m|tostring] // $m
      ),
      key: .key,
      dispatcher: .dispatcher,
      arg: .arg,
      desc: .description
    }
  ) |
  map(
    "\(.mods)+\(.key) | \(.desc // .dispatcher) | \(.dispatcher) | \(.arg)"
  ) |
  .[]
')

# Create arrays to store dispatchers and args
readarray -t display_array <<< "$choices"
readarray -t command_array <<< "$(echo "$binds_json" | jq -r 'map("\(.dispatcher)|\(.arg)") | .[]')"

# Let the user select a keybinding via rofi
selected=$(echo "$choices" | rofi -dmenu -p "Select Hyprland keybinding:" -format i)

# If user made a selection (didn't cancel)
if [[ -n "$selected" ]]; then
  # Get the corresponding dispatcher and argument using the index
  dispatch_and_arg="${command_array[$selected]}"
  dispatcher=$(echo "$dispatch_and_arg" | cut -d'|' -f1)
  arg=$(echo "$dispatch_and_arg" | cut -d'|' -f2-)

  # Execute the selected binding
  if [[ -n "$dispatcher" && -n "$arg" ]]; then
    hyprctl dispatch "$dispatcher" "$arg"
  fi
fi
