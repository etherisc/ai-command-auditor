#!/bin/bash
#
# Script Name: show-ports.sh
# Description: Show the dynamically assigned ports for the AI Command Auditor devcontainer
# Author: AI Assistant
# Date: $(date +%Y-%m-%d)
# Version: 1.0
#
# Usage: ./show-ports.sh
#

set -euo pipefail

# Constants
readonly SCRIPT_NAME="$(basename "$0")"
readonly CONTAINER_NAME_PATTERN="ai-command-auditor.*devcontainer"

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Functions
log() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')] $*${NC}"
}

error() {
    echo -e "${RED}ERROR: $*${NC}" >&2
    exit 1
}

warning() {
    echo -e "${YELLOW}WARNING: $*${NC}" >&2
}

info() {
    echo -e "${BLUE}INFO: $*${NC}"
}

show_container_ports() {
    local container_id
    container_id=$(docker ps --filter "name=${CONTAINER_NAME_PATTERN}" --format "{{.ID}}" | head -1)

    if [[ -z "$container_id" ]]; then
        error "No running devcontainer found matching pattern: ${CONTAINER_NAME_PATTERN}"
    fi

    local container_name
    container_name=$(docker ps --filter "id=${container_id}" --format "{{.Names}}")

    log "Found devcontainer: ${container_name} (${container_id})"
    echo

    info "Port mappings:"
    docker port "$container_id" | while read -r line; do
        if [[ -n "$line" ]]; then
            local container_port host_mapping
            container_port=$(echo "$line" | cut -d' ' -f1)
            host_mapping=$(echo "$line" | cut -d' ' -f3)

            echo -e "  ${YELLOW}Container Port ${container_port}${NC} -> ${GREEN}Host ${host_mapping}${NC}"
        fi
    done

    echo
    info "Access your services at:"
    docker port "$container_id" | while read -r line; do
        if [[ -n "$line" ]]; then
            local container_port host_port
            container_port=$(echo "$line" | cut -d' ' -f1 | cut -d'/' -f1)
            host_port=$(echo "$line" | cut -d' ' -f3 | cut -d':' -f2)

            case "$container_port" in
                3000)
                    echo -e "  ${BLUE}React/Node.js Dev Server:${NC} http://localhost:${host_port}"
                    ;;
                5000)
                    echo -e "  ${BLUE}Flask Dev Server:${NC} http://localhost:${host_port}"
                    ;;
                8000)
                    echo -e "  ${BLUE}Python Web Server:${NC} http://localhost:${host_port}"
                    ;;
                8080)
                    echo -e "  ${BLUE}Alternative Web Server:${NC} http://localhost:${host_port}"
                    ;;
                9000)
                    echo -e "  ${BLUE}Additional Service:${NC} http://localhost:${host_port}"
                    ;;
                *)
                    echo -e "  ${BLUE}Port ${container_port}:${NC} http://localhost:${host_port}"
                    ;;
            esac
        fi
    done
}

usage() {
    cat << EOF
Usage: $SCRIPT_NAME [OPTIONS]

Show the dynamically assigned ports for the AI Command Auditor devcontainer.

OPTIONS:
    -h, --help      Show this help message

EXAMPLES:
    $SCRIPT_NAME

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        *)
            error "Unknown option: $1"
            ;;
    esac
done

# Main execution
main() {
    log "Checking for AI Command Auditor devcontainer..."
    show_container_ports
}

main "$@"
