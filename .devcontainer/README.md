# Development Container Configuration

This directory contains the configuration for the AI Command Auditor development container.

## Files

- `devcontainer.json` - VS Code devcontainer configuration
- `docker-compose.yml` - Docker Compose service definition
- `Dockerfile` - Container image build instructions
- `show-ports.sh` - Helper script to display dynamic port mappings

## Port Configuration

The devcontainer uses **dynamic port allocation** to avoid conflicts when running multiple devcontainers simultaneously. Instead of fixed port mappings like `3000:3000`, the configuration uses dynamic mappings like `3000`, allowing Docker to automatically assign available host ports.

### Available Container Ports

- `3000` - Node.js/React development server
- `5000` - Flask development server
- `8000` - Python web server
- `8080` - Alternative web server
- `9000` - Additional service port

### Finding Your Assigned Ports

After starting the devcontainer, use the helper script to see which host ports were assigned:

```bash
# From inside the devcontainer
./.devcontainer/show-ports.sh

# Or from the host system
cd /path/to/ai-command-auditor
./.devcontainer/show-ports.sh
```

Example output:

```
[16:42:15] Found devcontainer: ai-command-auditor_devcontainer-devcontainer-1 (a1b2c3d4e5f6)

INFO: Port mappings:
  Container Port 3000/tcp -> Host 0.0.0.0:32768
  Container Port 5000/tcp -> Host 0.0.0.0:32769
  Container Port 8000/tcp -> Host 0.0.0.0:32770

INFO: Access your services at:
  React/Node.js Dev Server: http://localhost:32768
  Flask Dev Server: http://localhost:32769
  Python Web Server: http://localhost:32770
```

### Benefits of Dynamic Port Allocation

1. **No Port Conflicts** - Multiple devcontainers can run simultaneously
2. **Automatic Assignment** - Docker handles port allocation automatically
3. **Easy Discovery** - Use the helper script to find assigned ports
4. **Flexible Development** - Work on multiple projects without conflicts

## Troubleshooting

### Port Discovery Issues

If the `show-ports.sh` script can't find your container:

1. Check if the container is running:

   ```bash
   docker ps | grep ai-command-auditor
   ```

2. Verify the container name pattern in the script matches your actual container name

3. Manual port checking:

   ```bash
   docker port <container-name-or-id>
   ```

### Container Startup Issues

If you encounter port binding errors:

1. Stop any conflicting containers:

   ```bash
   docker ps
   docker stop <conflicting-container>
   ```

2. Rebuild the devcontainer:
   - In VS Code: `Ctrl+Shift+P` → "Dev Containers: Rebuild Container"

3. Check Docker daemon status:

   ```bash
   sudo systemctl status docker
   ```
