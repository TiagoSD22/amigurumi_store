#!/bin/bash
set -e

echo "🧹 Cleaning up Amigurumi Store Docker environment..."

# Stop and remove containers
echo "🛑 Stopping containers..."
docker-compose down --remove-orphans

# Remove volumes (optional)
read -p "Do you want to remove volumes (database data will be lost)? [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Removing volumes..."
    docker-compose down -v
    docker volume prune -f
fi

# Remove images (optional)
read -p "Do you want to remove built images? [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Removing images..."
    docker-compose down --rmi all
fi

# Remove unused Docker resources
echo "🧹 Cleaning up unused Docker resources..."
docker system prune -f

echo "✅ Cleanup completed!"
