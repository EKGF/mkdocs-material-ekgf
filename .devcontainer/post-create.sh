#!/bin/bash
set -e

echo "🚀 Setting up MKDocs Material EKGF Theme dev container..."

# Install system dependencies
echo "📦 Installing system dependencies..."
apt-get update
apt-get install -y \
  build-essential \
  libcairo2-dev \
  libfreetype6-dev \
  libffi-dev \
  libpango1.0-dev \
  libjpeg-dev \
  libpng-dev \
  zlib1g-dev \
  graphviz \
  curl \
  make

# Install uv
echo "📦 Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH for current session and future sessions
export PATH="$HOME/.cargo/bin:$PATH"
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc

# Verify uv installation
if ! command -v uv &> /dev/null; then
  echo "❌ Failed to install uv"
  exit 1
fi

echo "✅ uv installed: $(uv --version)"

# Install pnpm
echo "📦 Installing pnpm..."
npm install -g pnpm

# Install project dependencies (Python and Node)
echo "📦 Installing project dependencies..."
make install
pnpm install

echo "✅ Dev container setup complete!"
echo ""
echo "You can now run:"
echo "  - make build    (build theme package)"
echo "  - make lint     (run all linters)"
echo "  - make bump     (bump patch version)"
