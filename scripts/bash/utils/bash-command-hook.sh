#!/bin/bash

function command_checker() {
    local cmd="${BASH_COMMAND}"

    # Nur in interaktiven Shells
    [[ "$-" != *i* ]] && return 0

    result=$(~/.check_command.py "$cmd")
    if [[ "$result" == EXECUTE:* ]]; then
        fixed_cmd="${result#EXECUTE: }"
        echo "✅ Replacing command with: $fixed_cmd"

        # Verhindere mehrzeilige Ausführung
        if [[ "$fixed_cmd" == *$'\n'* ]]; then
            echo "❌ Multiline commands are not allowed."
            return 1
        fi

        eval "$fixed_cmd"
        return 1
    elif [[ "$result" == ERROR:* ]]; then
        echo "❌ Rejected: ${result#ERROR: }"
        return 1
    fi
    # Ursprünglichen Befehl laufen lassen
}
trap command_checker DEBUG
