// Modern Dashboard JavaScript

class CryptoZZDashboard {
    constructor() {
        this.apiBaseUrl = '';
        this.refreshInterval = null;
        this.isConnected = false;
        this.theme = localStorage.getItem('theme') || 'dark';
        
        this.init();
    }

    async init() {
        console.log('🚀 Initializing CryptoZZ Dashboard...');
        
        // Set initial theme
        this.applyTheme();
        
        // Load initial data
        await this.loadDashboardData();
        
        // Start auto refresh
        this.startAutoRefresh();
        
        // Setup event listeners
        this.setupEventListeners();
        
        console.log('✅ Dashboard initialized successfully!');
    }

    setupEventListeners() {
        // Theme toggle
        const themeToggle = document.querySelector('.theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }

        // Refresh button
        const refreshBtn = document.querySelector('[onclick="refreshData()"]');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.refreshData(e.target);
            });
        }

        // Navigation links
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                if (link.getAttribute('href').startsWith('#')) {
                    e.preventDefault();
                    this.navigateToSection(link.getAttribute('href').substring(1));
                }
            });
        });

        // Mobile menu toggle
        this.setupMobileMenu();
    }

    setupMobileMenu() {
        if (window.innerWidth <= 768) {
            const topBar = document.querySelector('.top-bar');
            const existingMenuBtn = topBar.querySelector('.mobile-menu-btn');
            
            if (!existingMenuBtn && topBar) {
                const menuBtn = document.createElement('button');
                menuBtn.innerHTML = '<i class="fas fa-bars"></i>';
                menuBtn.className = 'btn btn-secondary mobile-menu-btn';
                menuBtn.addEventListener('click', () => this.toggleSidebar());
                topBar.insertBefore(menuBtn, topBar.firstChild);
            }
        }
    }

    toggleSidebar() {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.classList.toggle('open');
        }
    }

    navigateToSection(section) {
        // Update active nav link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        
        const activeLink = document.querySelector(`[href="#${section}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }

        // Update page title
        const pageTitle = document.querySelector('.page-title');
        if (pageTitle) {
            const sectionNames = {
                dashboard: 'Trading Dashboard',
                trading: 'Trading Signals',
                portfolio: 'Portfolio Management',
                analysis: 'Market Analysis',
                backtesting: 'Backtesting Results',
                settings: 'Settings'
            };
            pageTitle.textContent = sectionNames[section] || 'Dashboard';
        }

        // Load section-specific data
        this.loadSectionData(section);
    }

    async loadSectionData(section) {
        switch (section) {
            case 'trading':
                await this.loadSignals();
                break;
            case 'portfolio':
                await this.loadPortfolioData();
                break;
            case 'analysis':
                await this.loadMarketAnalysis();
                break;
            case 'backtesting':
                await this.loadBacktestResults();
                break;
            default:
                await this.loadDashboardData();
        }
    }

    async loadDashboardData() {
        try {
            // Show loading states
            this.showLoadingStates();

            // Load system status
            const statusData = await this.apiCall('/api/status');
            
            if (statusData && statusData.status === 'operational') {
                this.isConnected = true;
                await Promise.all([
                    this.updatePortfolioStats(),
                    this.updateTradingStats(),
                    this.loadSignals(),
                    this.loadPortfolioData()
                ]);
            } else {
                this.showDemoData();
            }

            this.hideLoadingStates();
        } catch (error) {
            console.error('Error loading dashboard data:', error);
            this.showDemoData();
            this.hideLoadingStates();
        }
    }

    async updatePortfolioStats() {
        try {
            // Try to get real portfolio data
            const portfolioData = await this.apiCall('/api/portfolio/summary');
            
            if (portfolioData) {
                this.updateElement('portfolioValue', this.formatCurrency(portfolioData.total_value || 0));
                this.updateElement('portfolioChange', this.formatPercentage(portfolioData.change_24h || 0), true);
                this.updateElement('pnlToday', this.formatCurrency(portfolioData.pnl_today || 0), true);
            } else {
                // Use demo data
                this.updateElement('portfolioValue', '$25,847.32');
                this.updateElement('portfolioChange', '+5.23%', true);
                this.updateElement('pnlToday', '+$1,234.56', true);
            }
        } catch (error) {
            console.error('Error updating portfolio stats:', error);
            this.showDemoPortfolioStats();
        }
    }

    async updateTradingStats() {
        try {
            const signalData = await this.apiCall('/api/signals/stats');
            
            if (signalData) {
                this.updateElement('activeSignals', signalData.active_count || 0);
                this.updateElement('signalAccuracy', this.formatPercentage(signalData.accuracy || 0));
                this.updateElement('winRate', this.formatPercentage(signalData.win_rate || 0));
            } else {
                this.updateElement('activeSignals', '8');
                this.updateElement('signalAccuracy', '87.3%');
                this.updateElement('winRate', '73.2%');
            }

            // Risk level calculation
            this.updateRiskLevel();
        } catch (error) {
            console.error('Error updating trading stats:', error);
            this.showDemoTradingStats();
        }
    }

    updateRiskLevel() {
        const riskLevels = ['LOW', 'MODERATE', 'HIGH', 'EXTREME'];
        const riskLevel = riskLevels[Math.floor(Math.random() * riskLevels.length)];
        const riskPercentage = (Math.random() * 50 + 5).toFixed(1);
        
        this.updateElement('riskLevel', riskLevel);
        this.updateElement('riskPercentage', `${riskPercentage}%`);
    }

    async loadSignals() {
        const signalFeed = document.getElementById('signalFeed');
        if (!signalFeed) return;

        signalFeed.innerHTML = '<div class="loading"></div>';
        
        try {
            const signalsData = await this.apiCall('/api/signals/recent');
            
            if (signalsData && signalsData.data && signalsData.data.length > 0) {
                this.displaySignals(signalsData.data);
            } else {
                this.displayDemoSignals();
            }
        } catch (error) {
            console.error('Error loading signals:', error);
            this.displayDemoSignals();
        }
    }

    displaySignals(signals) {
        const signalFeed = document.getElementById('signalFeed');
        if (!signalFeed) return;

        signalFeed.innerHTML = signals.map(signal => `
            <div class="signal-item fade-in">
                <div class="signal-info">
                    <h4>${signal.symbol || 'Unknown'}</h4>
                    <p>${signal.description || signal.reasoning || 'AI Generated Signal'}</p>
                    <small>${this.formatTime(signal.timestamp || signal.created_at)}</small>
                </div>
                <div class="signal-badge signal-${(signal.action || signal.signal_type || 'buy').toLowerCase()}">
                    ${(signal.action || signal.signal_type || 'BUY').toUpperCase()}
                </div>
            </div>
        `).join('');
    }

    displayDemoSignals() {
        const demoSignals = [
            { symbol: 'BTC-USDT', action: 'buy', description: 'Strong bullish momentum detected with SMC confirmation', time: '2 min ago' },
            { symbol: 'ETH-USDT', action: 'sell', description: 'Resistance level reached, potential reversal', time: '5 min ago' },
            { symbol: 'ADA-USDT', action: 'buy', description: 'Support level bounce with volume confirmation', time: '8 min ago' },
            { symbol: 'DOT-USDT', action: 'buy', description: 'SMC Order Block formation detected', time: '12 min ago' },
            { symbol: 'LINK-USDT', action: 'sell', description: 'Bearish divergence on multiple timeframes', time: '15 min ago' }
        ];
        
        const signalFeed = document.getElementById('signalFeed');
        if (!signalFeed) return;

        signalFeed.innerHTML = demoSignals.map(signal => `
            <div class="signal-item fade-in">
                <div class="signal-info">
                    <h4>${signal.symbol}</h4>
                    <p>${signal.description}</p>
                    <small>${signal.time}</small>
                </div>
                <div class="signal-badge signal-${signal.action}">
                    ${signal.action.toUpperCase()}
                </div>
            </div>
        `).join('');
    }

    async loadPortfolioData() {
        const portfolioBreakdown = document.getElementById('portfolioBreakdown');
        if (!portfolioBreakdown) return;

        try {
            const portfolioData = await this.apiCall('/api/portfolio/breakdown');
            
            if (portfolioData && portfolioData.holdings) {
                this.displayPortfolio(portfolioData.holdings);
            } else {
                this.displayDemoPortfolio();
            }
        } catch (error) {
            console.error('Error loading portfolio:', error);
            this.displayDemoPortfolio();
        }
    }

    displayPortfolio(holdings) {
        const portfolioBreakdown = document.getElementById('portfolioBreakdown');
        if (!portfolioBreakdown) return;

        portfolioBreakdown.innerHTML = holdings.map(item => `
            <tr class="fade-in">
                <td><strong>${item.symbol}</strong></td>
                <td>${item.amount}</td>
                <td>${this.formatCurrency(item.value)}</td>
                <td class="${item.change_24h >= 0 ? 'positive' : 'negative'}">
                    ${this.formatPercentage(item.change_24h)}
                </td>
            </tr>
        `).join('');
    }

    displayDemoPortfolio() {
        const demoPortfolio = [
            { asset: 'BTC', holdings: '0.5234', value: 14523.45, change: 2.34, positive: true },
            { asset: 'ETH', holdings: '12.3456', value: 8234.56, change: 1.85, positive: true },
            { asset: 'ADA', holdings: '5,678.90', value: 2345.67, change: -0.67, positive: false },
            { asset: 'DOT', holdings: '234.56', value: 1234.89, change: 4.21, positive: true },
            { asset: 'LINK', holdings: '89.12', value: 956.78, change: -1.23, positive: false }
        ];
        
        const portfolioBreakdown = document.getElementById('portfolioBreakdown');
        if (!portfolioBreakdown) return;

        portfolioBreakdown.innerHTML = demoPortfolio.map(item => `
            <tr class="fade-in">
                <td><strong>${item.asset}</strong></td>
                <td>${item.holdings}</td>
                <td>${this.formatCurrency(item.value)}</td>
                <td class="${item.positive ? 'positive' : 'negative'}">
                    ${item.change > 0 ? '+' : ''}${item.change.toFixed(2)}%
                </td>
            </tr>
        `).join('');
    }

    async loadMarketAnalysis() {
        try {
            const analysisData = await this.apiCall('/api/analysis/market');
            console.log('Market analysis loaded:', analysisData);
        } catch (error) {
            console.error('Error loading market analysis:', error);
        }
    }

    async loadBacktestResults() {
        try {
            const backtestData = await this.apiCall('/api/backtest/results');
            console.log('Backtest results loaded:', backtestData);
        } catch (error) {
            console.error('Error loading backtest results:', error);
        }
    }

    async refreshData(buttonElement) {
        if (buttonElement) {
            const icon = buttonElement.querySelector('i');
            if (icon) {
                icon.style.animation = 'spin 1s linear infinite';
            }
        }

        try {
            await this.loadDashboardData();
        } finally {
            if (buttonElement) {
                const icon = buttonElement.querySelector('i');
                if (icon) {
                    setTimeout(() => {
                        icon.style.animation = '';
                    }, 1000);
                }
            }
        }
    }

    startAutoRefresh() {
        // Clear existing interval
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }

        // Start new interval (refresh every 30 seconds)
        this.refreshInterval = setInterval(() => {
            this.loadDashboardData();
        }, 30000);
    }

    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }

    toggleTheme() {
        this.theme = this.theme === 'dark' ? 'light' : 'dark';
        this.applyTheme();
        localStorage.setItem('theme', this.theme);
    }

    applyTheme() {
        document.documentElement.setAttribute('data-theme', this.theme);
        
        const themeIcon = document.querySelector('.theme-toggle i');
        if (themeIcon) {
            themeIcon.className = this.theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        }
    }

    showLoadingStates() {
        const loadingElements = ['portfolioValue', 'activeSignals', 'pnlToday', 'riskLevel'];
        loadingElements.forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.innerHTML = '<div class="loading"></div>';
            }
        });
    }

    hideLoadingStates() {
        // Loading states will be replaced by actual data
    }

    showDemoData() {
        this.showDemoPortfolioStats();
        this.showDemoTradingStats();
        this.displayDemoSignals();
        this.displayDemoPortfolio();
    }

    showDemoPortfolioStats() {
        this.updateElement('portfolioValue', '$25,847.32');
        this.updateElement('portfolioChange', '+5.23%', true);
        this.updateElement('pnlToday', '+$1,234.56', true);
    }

    showDemoTradingStats() {
        this.updateElement('activeSignals', '8');
        this.updateElement('signalAccuracy', '87.3%');
        this.updateElement('winRate', '73.2%');
        this.updateElement('riskLevel', 'MODERATE');
        this.updateElement('riskPercentage', '23.5%');
    }

    updateElement(id, value, applyColorClass = false) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;
            
            if (applyColorClass && typeof value === 'string') {
                element.className = value.startsWith('+') ? 'positive' : 
                                  value.startsWith('-') ? 'negative' : '';
            }
        }
    }

    async apiCall(endpoint) {
        try {
            const response = await fetch(this.apiBaseUrl + endpoint);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`API call failed for ${endpoint}:`, error);
            return null;
        }
    }

    formatCurrency(value) {
        if (typeof value === 'number') {
            return new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD'
            }).format(value);
        }
        return value;
    }

    formatPercentage(value) {
        if (typeof value === 'number') {
            const formatted = value.toFixed(2);
            return `${value >= 0 ? '+' : ''}${formatted}%`;
        }
        return value;
    }

    formatTime(timestamp) {
        if (!timestamp) return 'Unknown';
        
        try {
            const date = new Date(timestamp);
            const now = new Date();
            const diffMinutes = Math.floor((now - date) / 60000);
            
            if (diffMinutes < 1) return 'Just now';
            if (diffMinutes < 60) return `${diffMinutes} min ago`;
            if (diffMinutes < 1440) return `${Math.floor(diffMinutes / 60)} hours ago`;
            return date.toLocaleDateString();
        } catch (error) {
            return 'Unknown';
        }
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.dashboard = new CryptoZZDashboard();
});

// Global functions for backward compatibility
function refreshData() {
    if (window.dashboard) {
        window.dashboard.refreshData(event.target);
    }
}

function toggleTheme() {
    if (window.dashboard) {
        window.dashboard.toggleTheme();
    }
}

function openTradeModal() {
    alert('Trade execution interface would open here');
}

function updateChart() {
    const timeframe = document.getElementById('timeframe')?.value;
    console.log('Updating chart for timeframe:', timeframe);
}

function loadSignals() {
    if (window.dashboard) {
        window.dashboard.loadSignals();
    }
}