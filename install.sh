#!/bin/bash
# =============================================================================
# Opus Orchestrator AI - One-Line Installer
# =============================================================================
# Usage:
#   curl -sSL https://raw.githubusercontent.com/mrhavens/opus-orchestrator-ai/main/install.sh | bash
#   curl -sSL https://raw.githubusercontent.com/mrhavens/opus-orchestrator-ai/main/install.sh | bash -s -- --help
#
# Or with options:
#   curl -sSL https://raw.githubusercontent.com/mrhavens/opus-orchestrator-ai/main/install.sh | bash -s -- --api-key YOUR_KEY --start
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
API_KEY=""
GITHUB_TOKEN=""
START_SERVICES=false
PORT=8080
REPO_URL="https://github.com/mrhavens/opus-orchestrator-ai.git"
INSTALL_DIR="$HOME/opus-orchestrator"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --api-key)
            API_KEY="$2"
            shift 2
            ;;
        --github-token)
            GITHUB_TOKEN="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --start)
            START_SERVICES=true
            shift
            ;;
        --dir)
            INSTALL_DIR="$2"
            shift 2
            ;;
        --help|-h)
            echo "Opus Orchestrator AI Installer"
            echo ""
            echo "Usage: curl -sSL https://raw.githubusercontent.com/mrhavens/opus-orchestrator-ai/main/install.sh | bash -s -- [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --api-key KEY        Set OpenAI API key"
            echo "  --github-token TOKEN Set GitHub token"
            echo "  --port PORT          Set port (default: 8080)"
            echo "  --start              Start services after install"
            echo "  --dir PATH           Install directory (default: ~/opus-orchestrator)"
            echo "  --help, -h           Show this help"
            echo ""
            echo "Examples:"
            echo "  # Install and start web UI"
            echo "  curl -sSL ... | bash -s -- --api-key sk-... --start"
            echo ""
            echo "  # Install to custom directory"
            echo "  curl -sSL ... | bash -s -- --dir /opt/opus"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  📚 Opus Orchestrator AI - Installer${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "  ✓ Python $PYTHON_VERSION"

if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo -e "${RED}Error: pip is required but not installed.${NC}"
    exit 1
fi

PIP_CMD="pip3"
if command -v pip &> /dev/null; then
    PIP_CMD="pip"
fi
echo "  ✓ pip available"

# Create install directory
echo ""
echo -e "${YELLOW}Installing to $INSTALL_DIR...${NC}"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Clone or update repo
if [ -d ".git" ]; then
    echo "  ✓ Repository already exists, updating..."
    git pull origin main 2>/dev/null || true
else
    echo "  ✓ Cloning repository..."
    git clone --depth 1 "$REPO_URL" .
fi

# Create virtual environment
echo ""
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo ""
echo -e "${YELLOW}Installing dependencies...${NC}"
$PIP_CMD install --upgrade pip --quiet
$PIP_CMD install -e . --quiet 2>/dev/null || true

# Try to install extras
$PIP_CMD install crewai pydantic-ai pydantic autogen fastapi uvicorn boto3 requests python-dotenv --quiet 2>/dev/null || true

echo "  ✓ Dependencies installed"

# Create .env file
echo ""
echo -e "${YELLOW}Configuring...${NC}"

ENV_FILE="$INSTALL_DIR/.env"
touch "$ENV_FILE"

if [ -n "$API_KEY" ]; then
    if ! grep -q "OPENAI_API_KEY" "$ENV_FILE" 2>/dev/null; then
        echo "OPENAI_API_KEY=$API_KEY" >> "$ENV_FILE"
        echo "  ✓ OpenAI API key configured"
    fi
fi

if [ -n "$GITHUB_TOKEN" ]; then
    if ! grep -q "GITHUB_TOKEN" "$ENV_FILE" 2>/dev/null; then
        echo "GITHUB_TOKEN=$GITHUB_TOKEN" >> "$ENV_FILE"
        echo "  ✓ GitHub token configured"
    fi
fi

# Create activation script
ACTIVATION_SCRIPT="$INSTALL_DIR/opus.sh"
cat > "$ACTIVATION_SCRIPT" << 'SCRIPT'
#!/bin/bash
# Opus Orchestrator AI - Quick Start Script

cd "$(dirname "$0")"
source venv/bin/activate

# Default: start web UI
if [ "$1" = "ui" ]; then
    exec python3 -m opus_orchestrator ui --port "${2:-8080}"
elif [ "$1" = "serve" ]; then
    exec python3 -m opus_orchestrator serve --port "${2:-8000}"
elif [ "$1" = "generate" ]; then
    shift
    exec python3 -m opus_orchestrator generate "$@"
elif [ "$1" = "help" ] || [ "$1" = "--help" ] || [ -z "$1" ]; then
    echo "Opus Orchestrator AI - Quick Start"
    echo ""
    echo "Usage:"
    echo "  ./opus.sh ui [port]      # Start web UI (default: 8080)"
    echo "  ./opus.sh serve [port]   # Start API server (default: 8000)"
    echo "  ./opus.sh generate ...   # Run generation"
    echo "  ./opus.sh help           # Show this help"
    echo ""
    echo "Examples:"
    echo "  ./opus.sh ui"
    echo "  ./opus.sh ui 9000"
    echo "  ./opus.sh serve"
    echo "  ./opus.sh generate --concept 'A robot dreams'"
else
    exec python3 -m opus_orchestrator "$@"
fi
SCRIPT

chmod +x "$ACTIVATION_SCRIPT"
echo "  ✓ Activation script created: ./opus.sh"

# Start services if requested
if [ "$START_SERVICES" = true ]; then
    echo ""
    echo -e "${YELLOW}Starting services...${NC}"
    
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  🎉 Installation Complete!${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "  Web UI:    http://localhost:$PORT"
    echo "  API Docs:  http://localhost:$PORT/docs"
    echo ""
    echo "  To start manually:"
    echo "    cd $INSTALL_DIR"
    echo "    ./opus.sh ui $PORT"
    echo ""
    
    source venv/bin/activate
    exec python3 -m opus_orchestrator ui --port "$PORT"
else
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  🎉 Installation Complete!${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "  Next steps:"
    echo "    cd $INSTALL_DIR"
    echo "    ./opus.sh ui"
    echo ""
    echo "  Or start with custom port:"
    echo "    ./opus.sh ui 9000"
    echo ""
    echo "  Full CLI usage:"
    echo "    ./opus.sh help"
    echo ""
fi
