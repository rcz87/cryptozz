#!/bin/bash

# Crypto Trading AI Platform - Production Deployment Script
# Supports multiple deployment targets: Docker, VPS, Cloud providers

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="crypto-gpts-api"
IMAGE_NAME="ghcr.io/username/$PROJECT_NAME"
DEFAULT_TAG="latest"

# Help function
show_help() {
    cat << EOF
🚀 Crypto Trading AI Platform - Deployment Script

Usage: $0 [OPTIONS] COMMAND

Commands:
    local       Deploy locally using Docker Compose
    staging     Deploy to staging environment
    production  Deploy to production environment
    build       Build Docker image only
    test        Run deployment tests
    rollback    Rollback to previous version
    status      Check deployment status
    logs        View application logs
    clean       Clean up old deployments

Options:
    -t, --tag TAG       Docker image tag (default: latest)
    -e, --env FILE      Environment file path
    -h, --help          Show this help message
    -v, --verbose       Verbose output
    --no-cache          Build without cache
    --force             Force deployment (skip confirmations)

Examples:
    $0 local                    # Deploy locally
    $0 production -t v1.2.3     # Deploy specific version to production
    $0 build --no-cache         # Build fresh image
    $0 status                   # Check current status

Environment Variables:
    DEPLOYMENT_TARGET   Target environment (local/staging/production)
    DOCKER_REGISTRY     Docker registry URL
    SSH_HOST           SSH host for remote deployment
    SSH_USER           SSH username for remote deployment

EOF
}

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    local missing_tools=()
    
    if ! command -v docker &> /dev/null; then
        missing_tools+=("docker")
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        missing_tools+=("docker-compose")
    fi
    
    if [[ ${#missing_tools[@]} -gt 0 ]]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        log_info "Please install the missing tools and try again."
        exit 1
    fi
    
    log_success "All prerequisites met"
}

# Load environment variables
load_environment() {
    local env_file="${1:-}"
    
    if [[ -n "$env_file" && -f "$env_file" ]]; then
        log_info "Loading environment from $env_file"
        set -a
        source "$env_file"
        set +a
    elif [[ -f ".env" ]]; then
        log_info "Loading environment from .env"
        set -a
        source ".env"
        set +a
    elif [[ -f ".env.${DEPLOYMENT_TARGET:-local}" ]]; then
        local target_env=".env.${DEPLOYMENT_TARGET:-local}"
        log_info "Loading environment from $target_env"
        set -a
        source "$target_env"
        set +a
    else
        log_warning "No environment file found, using defaults"
    fi
}

# Build Docker image
build_image() {
    local tag="${1:-$DEFAULT_TAG}"
    local no_cache="${2:-false}"
    
    log_info "Building Docker image: $IMAGE_NAME:$tag"
    
    local build_args=""
    if [[ "$no_cache" == "true" ]]; then
        build_args="--no-cache"
    fi
    
    if docker build $build_args -t "$IMAGE_NAME:$tag" .; then
        log_success "Image built successfully: $IMAGE_NAME:$tag"
    else
        log_error "Failed to build Docker image"
        exit 1
    fi
}

# Deploy locally using Docker Compose
deploy_local() {
    local tag="${1:-$DEFAULT_TAG}"
    
    log_info "Deploying locally using Docker Compose..."
    
    export IMAGE_TAG="$tag"
    
    # Stop existing services
    docker-compose down || true
    
    # Start services
    if docker-compose up -d; then
        log_success "Local deployment completed"
        
        # Wait for services to be ready
        log_info "Waiting for services to be ready..."
        sleep 30
        
        # Run health check
        if run_health_check "http://localhost:5000"; then
            log_success "Local deployment is healthy"
        else
            log_error "Local deployment health check failed"
            docker-compose logs app
            exit 1
        fi
    else
        log_error "Local deployment failed"
        exit 1
    fi
}

# Deploy to remote environment
deploy_remote() {
    local environment="$1"
    local tag="${2:-$DEFAULT_TAG}"
    
    log_info "Deploying to $environment environment..."
    
    # Check if SSH configuration is available
    if [[ -z "${SSH_HOST:-}" || -z "${SSH_USER:-}" ]]; then
        log_error "SSH_HOST and SSH_USER must be set for remote deployment"
        exit 1
    fi
    
    # Deploy via SSH
    ssh "${SSH_USER}@${SSH_HOST}" "
        cd /opt/$PROJECT_NAME &&
        git pull origin main &&
        docker-compose pull &&
        docker-compose up -d --remove-orphans &&
        echo 'Deployment completed on $environment'
    "
    
    # Run remote health check
    local remote_url="https://${SSH_HOST}"
    if run_health_check "$remote_url"; then
        log_success "$environment deployment is healthy"
    else
        log_error "$environment deployment health check failed"
        exit 1
    fi
}

# Run health check
run_health_check() {
    local base_url="$1"
    local max_attempts=30
    local attempt=1
    
    log_info "Running health check against $base_url"
    
    while [[ $attempt -le $max_attempts ]]; do
        if curl -f -s "$base_url/health" > /dev/null; then
            log_success "Health check passed"
            return 0
        fi
        
        log_info "Health check attempt $attempt/$max_attempts failed, retrying..."
        sleep 10
        ((attempt++))
    done
    
    log_error "Health check failed after $max_attempts attempts"
    return 1
}

# Run deployment tests
run_tests() {
    log_info "Running deployment tests..."
    
    # API endpoint tests
    local base_url="http://localhost:5000"
    
    # Test health endpoint
    if curl -f -s "$base_url/health" | grep -q "healthy"; then
        log_success "Health endpoint test passed"
    else
        log_error "Health endpoint test failed"
        return 1
    fi
    
    # Test API status endpoint
    if curl -f -s "$base_url/api/gpts/status" | grep -q "active"; then
        log_success "API status endpoint test passed"
    else
        log_error "API status endpoint test failed"
        return 1
    fi
    
    # Test protected endpoint (should require auth)
    if curl -f -s "$base_url/api/gpts/sinyal/tajam" | grep -q "API key required"; then
        log_success "Authentication test passed"
    else
        log_error "Authentication test failed"
        return 1
    fi
    
    log_success "All deployment tests passed"
}

# Check deployment status
check_status() {
    log_info "Checking deployment status..."
    
    # Check Docker containers
    if docker-compose ps | grep -q "Up"; then
        log_success "Services are running"
        docker-compose ps
    else
        log_warning "Some services may not be running"
        docker-compose ps
    fi
    
    # Check health endpoint
    if curl -f -s "http://localhost:5000/health" > /dev/null; then
        log_success "Application is responding"
    else
        log_warning "Application may not be responding"
    fi
}

# View logs
view_logs() {
    local service="${1:-app}"
    
    log_info "Viewing logs for service: $service"
    docker-compose logs -f "$service"
}

# Clean up old deployments
cleanup() {
    log_info "Cleaning up old deployments..."
    
    # Remove stopped containers
    docker container prune -f
    
    # Remove unused images
    docker image prune -f
    
    # Remove unused volumes (with confirmation)
    log_warning "This will remove unused Docker volumes. Continue? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        docker volume prune -f
    fi
    
    log_success "Cleanup completed"
}

# Main function
main() {
    local command=""
    local tag="$DEFAULT_TAG"
    local env_file=""
    local verbose=false
    local no_cache=false
    local force=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -t|--tag)
                tag="$2"
                shift 2
                ;;
            -e|--env)
                env_file="$2"
                shift 2
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            -v|--verbose)
                verbose=true
                set -x
                shift
                ;;
            --no-cache)
                no_cache=true
                shift
                ;;
            --force)
                force=true
                shift
                ;;
            local|staging|production|build|test|rollback|status|logs|clean)
                command="$1"
                shift
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Validate command
    if [[ -z "$command" ]]; then
        log_error "No command specified"
        show_help
        exit 1
    fi
    
    # Load environment
    load_environment "$env_file"
    
    # Check prerequisites for most commands
    if [[ "$command" != "status" && "$command" != "logs" ]]; then
        check_prerequisites
    fi
    
    # Execute command
    case "$command" in
        local)
            build_image "$tag" "$no_cache"
            deploy_local "$tag"
            ;;
        staging)
            build_image "$tag" "$no_cache"
            deploy_remote "staging" "$tag"
            ;;
        production)
            if [[ "$force" != "true" ]]; then
                log_warning "Deploying to production. Continue? (y/N)"
                read -r response
                if [[ ! "$response" =~ ^[Yy]$ ]]; then
                    log_info "Deployment cancelled"
                    exit 0
                fi
            fi
            build_image "$tag" "$no_cache"
            deploy_remote "production" "$tag"
            ;;
        build)
            build_image "$tag" "$no_cache"
            ;;
        test)
            run_tests
            ;;
        status)
            check_status
            ;;
        logs)
            view_logs "${2:-app}"
            ;;
        clean)
            cleanup
            ;;
        *)
            log_error "Unknown command: $command"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"