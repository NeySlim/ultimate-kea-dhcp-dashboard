// System monitoring gauges
function initGauges(themes, settings) {
    let gaugesInterval = null;
    
    function updateGauges() {
        fetch('/api/stats')
            .then(res => res.json())
            .then(stats => {
                const theme = themes[settings.theme] || themes.ember;
                
                // Update CPU core gauges (now static in HTML)
                if (stats.cpu_cores) {
                    stats.cpu_cores.forEach((coreValue, idx) => {
                        const coreFill = document.getElementById(`cpu${idx}GaugeFill`);
                        const coreValueEl = document.getElementById(`cpu${idx}GaugeValue`);
                        if (coreFill && coreValueEl) {
                            const dashArray = (coreValue / 100) * 251;
                            coreFill.setAttribute('stroke-dasharray', `${dashArray} 251`);
                            coreValueEl.textContent = coreValue.toFixed(1) + '%';
                        }
                    });
                }
                
                // Update RAM gauge
                const ramPercent = stats.ram;
                const ramFill = document.getElementById('ramGaugeFill');
                const ramValue = document.getElementById('ramGaugeValue');
                const ramLegend = document.getElementById('ramLegend');
                if (ramFill && ramValue) {
                    const dashArray = (ramPercent / 100) * 251;
                    ramFill.setAttribute('stroke-dasharray', `${dashArray} 251`);
                    ramValue.textContent = ramPercent.toFixed(1) + '%';
                    ramLegend.textContent = `${stats.ram_used_gb} / ${stats.ram_total_gb} GB`;
                }
                
                // Update NET gauge (show both send/recv with dynamic scale)
                // Use a fixed max of 100 Mbps or dynamic if exceeds
                const netAbsMax = Math.max(stats.net_sent, stats.net_recv);
                const netScale = netAbsMax > 100 ? netAbsMax * 1.1 : 100;
                const netSendPercent = (stats.net_sent / netScale) * 100;
                const netRecvPercent = (stats.net_recv / netScale) * 100;
                const netFillSend = document.getElementById('netGaugeFillSend');
                const netFillRecv = document.getElementById('netGaugeFillRecv');
                const netValue = document.getElementById('netGaugeValue');
                const netLegend = document.getElementById('netLegend');
                if (netFillSend && netFillRecv && netValue) {
                    const dashArraySend = (netSendPercent / 100) * 251;
                    const dashArrayRecv = (netRecvPercent / 100) * 251;
                    netFillSend.setAttribute('stroke-dasharray', `${dashArraySend} 251`);
                    netFillRecv.setAttribute('stroke-dasharray', `${dashArrayRecv} 251`);
                    netValue.textContent = Math.max(netSendPercent, netRecvPercent).toFixed(0) + '%';
                    netLegend.textContent = `↑${stats.net_sent.toFixed(2)} ↓${stats.net_recv.toFixed(2)} Mbps`;
                }
                
                // Update DISK gauge
                const diskPercent = stats.disk;
                const diskFill = document.getElementById('diskGaugeFill');
                const diskValue = document.getElementById('diskGaugeValue');
                const diskLegend = document.getElementById('diskLegend');
                if (diskFill && diskValue) {
                    const dashArray = (diskPercent / 100) * 251;
                    diskFill.setAttribute('stroke-dasharray', `${dashArray} 251`);
                    diskValue.textContent = diskPercent.toFixed(1) + '%';
                    diskLegend.textContent = `${stats.disk_used_gb} / ${stats.disk_total_gb} GB`;
                }
            })
            .catch(err => console.error('Stats error:', err));
    }
    
    // Start gauges update cycle
    function startGaugesCycle() {
        // Clear existing interval
        if (gaugesInterval) clearInterval(gaugesInterval);
        
        // Update immediately
        updateGauges();
        
        // Start interval with configured refresh rate
        gaugesInterval = setInterval(updateGauges, settings.refreshInterval || 1000);
        console.log(`Gauges cycle started: ${settings.refreshInterval || 1000}ms`);
    }
    
    // Initial start
    startGaugesCycle();
    
    // Return function to restart cycle when settings change
    return startGaugesCycle;
}
