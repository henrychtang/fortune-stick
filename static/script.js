/**
 * 122車公求籤
 */

document.addEventListener('DOMContentLoaded', function() {
    const drawBtn = document.getElementById('drawBtn');
    const redrawBtn = document.getElementById('redrawBtn');
    const shareBtn = document.getElementById('shareBtn');
    const fortuneTube = document.getElementById('fortuneTube');
    const resultContainer = document.getElementById('resultContainer');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const shareNotification = document.getElementById('shareNotification');
    
    // Fortune history
    let drawHistory = JSON.parse(localStorage.getItem('fortuneHistory') || '[]');
    let currentFortune = null;
    
    // Update draw count display
    updateDrawCount();
    
    // 音效（使用 Web Audio API）
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    
    // 播放搖籤筒聲音 - 使用白噪音模擬竹籤搖晃聲
    function playShakeSound() {
        const duration = 1.5;
        const now = audioContext.currentTime;
        
        // 創建多層聲音模擬竹籤碰撞
        for (let layer = 0; layer < 3; layer++) {
            // 創建白噪音 buffer
            const bufferSize = audioContext.sampleRate * duration;
            const buffer = audioContext.createBuffer(1, bufferSize, audioContext.sampleRate);
            const data = buffer.getChannelData(0);
            
            // 填充隨機噪音
            for (let i = 0; i < bufferSize; i++) {
                data[i] = (Math.random() * 2 - 1);
            }
            
            // 創建 buffer source
            const noise = audioContext.createBufferSource();
            noise.buffer = buffer;
            
            // 使用 bandpass filter 讓聲音像竹籤碰撞
            const filter = audioContext.createBiquadFilter();
            filter.type = 'bandpass';
            filter.frequency.value = 800 + layer * 200;
            filter.Q.value = 1.5;
            
            // 增益控制
            const gainNode = audioContext.createGain();
            
            // 連接節點
            noise.connect(filter);
            filter.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            // 創建搖晃節奏 - 模擬竹籤互相碰撞
            const rhythm = [0, 0.08, 0.15, 0.22, 0.3, 0.38, 0.45, 0.52, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2];
            
            rhythm.forEach((time, index) => {
                const hitTime = now + time;
                const intensity = 0.15 - (index * 0.008) + (Math.random() * 0.05);
                
                // 每次碰撞的音量包絡
                gainNode.gain.setValueAtTime(0, hitTime);
                gainNode.gain.linearRampToValueAtTime(intensity, hitTime + 0.02);
                gainNode.gain.exponentialRampToValueAtTime(0.001, hitTime + 0.1);
            });
            
            // 開始播放
            noise.start(now);
            noise.stop(now + duration);
        }
        
        // 添加低頻撞擊聲（籤筒底部）
        const lowOsc = audioContext.createOscillator();
        const lowGain = audioContext.createGain();
        const lowFilter = audioContext.createBiquadFilter();
        
        lowOsc.type = 'triangle';
        lowFilter.type = 'lowpass';
        lowFilter.frequency.value = 200;
        
        lowOsc.connect(lowFilter);
        lowFilter.connect(lowGain);
        lowGain.connect(audioContext.destination);
        
        // 低頻節奏
        const lowRhythm = [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2];
        lowRhythm.forEach((time, index) => {
            const hitTime = now + time;
            lowOsc.frequency.setValueAtTime(80 + Math.random() * 20, hitTime);
            lowGain.gain.setValueAtTime(0, hitTime);
            lowGain.gain.linearRampToValueAtTime(0.3, hitTime + 0.01);
            lowGain.gain.exponentialRampToValueAtTime(0.001, hitTime + 0.08);
        });
        
        lowOsc.start(now);
        lowOsc.stop(now + duration);
    }
    
    // 播放求得簽文的聲音
    function playSuccessSound() {
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        // Play a pleasant chord
        const now = audioContext.currentTime;
        oscillator.frequency.setValueAtTime(523.25, now); // C5
        oscillator.frequency.setValueAtTime(659.25, now + 0.1); // E5
        oscillator.frequency.setValueAtTime(783.99, now + 0.2); // G5
        oscillator.frequency.setValueAtTime(1046.50, now + 0.3); // C6
        
        gainNode.gain.setValueAtTime(0.2, now);
        gainNode.gain.exponentialRampToValueAtTime(0.01, now + 1);
        
        oscillator.start(now);
        oscillator.stop(now + 1);
    }
    
    // Confetti Effect
    function fireConfetti() {
        const canvas = document.getElementById('confettiCanvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        const particles = [];
        const colors = ['#FFD700', '#FF6B6B', '#4ECDC4', '#FFE66D', '#FF6B9D', '#C7CEEA'];
        
        // Create particles
        for (let i = 0; i < 150; i++) {
            particles.push({
                x: canvas.width / 2,
                y: canvas.height / 2,
                vx: (Math.random() - 0.5) * 20,
                vy: (Math.random() - 0.5) * 20 - 5,
                color: colors[Math.floor(Math.random() * colors.length)],
                size: Math.random() * 10 + 5,
                rotation: Math.random() * 360,
                rotationSpeed: (Math.random() - 0.5) * 10
            });
        }
        
        let animationId;
        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            particles.forEach((p, index) => {
                p.x += p.vx;
                p.y += p.vy;
                p.vy += 0.3; // gravity
                p.rotation += p.rotationSpeed;
                p.vx *= 0.99; // air resistance
                
                ctx.save();
                ctx.translate(p.x, p.y);
                ctx.rotate(p.rotation * Math.PI / 180);
                ctx.fillStyle = p.color;
                ctx.fillRect(-p.size/2, -p.size/2, p.size, p.size);
                ctx.restore();
                
                // Remove particles that fall off screen
                if (p.y > canvas.height + 50) {
                    particles.splice(index, 1);
                }
            });
            
            if (particles.length > 0) {
                animationId = requestAnimationFrame(animate);
            } else {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
            }
        }
        
        animate();
        
        // Stop after 3 seconds
        setTimeout(() => {
            cancelAnimationFrame(animationId);
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }, 3000);
    }
    
    // 搖籤筒動畫
    function shakeTube() {
        fortuneTube.classList.add('shaking');
        
        // 創建隨機震動效果
        let shakeCount = 0;
        const maxShakes = 15;
        
        const shakeInterval = setInterval(() => {
            shakeCount++;
            const rotation = (Math.random() - 0.5) * 20;
            fortuneTube.style.transform = `rotate(${rotation}deg)`;
            
            if (shakeCount >= maxShakes) {
                clearInterval(shakeInterval);
                fortuneTube.classList.remove('shaking');
                fortuneTube.style.transform = '';
            }
        }, 100);
    }
    
    // 顯示加載畫面
    function showLoading() {
        loadingOverlay.classList.remove('hidden');
        // Reset progress bar animation
        const progressBar = document.getElementById('progressBar');
        progressBar.style.animation = 'none';
        setTimeout(() => {
            progressBar.style.animation = '';
        }, 10);
    }
    
    // 隱藏加載畫面
    function hideLoading() {
        loadingOverlay.classList.add('hidden');
    }
    
    // Update draw count
    function updateDrawCount() {
        const drawCountEl = document.getElementById('drawCount');
        if (drawCountEl) {
            drawCountEl.textContent = `📊 已求 ${drawHistory.length} 次`;
        }
    }
    
    // 顯示結果
    function showResult(fortune) {
        currentFortune = fortune;
        
        // 更新籤號
        document.getElementById('fortuneNumber').textContent = `第 ${fortune.number} 籤`;
        
        // 更新籤類型
        const typeElement = document.getElementById('fortuneType');
        typeElement.textContent = fortune.type;
        typeElement.className = 'fortune-type';
        
        // 根據籤類型設置顏色
        if (fortune.type.includes('上')) {
            typeElement.classList.add('good');
            // Fire confetti for good fortune
            setTimeout(fireConfetti, 500);
        } else if (fortune.type.includes('中')) {
            typeElement.classList.add('middle');
        } else {
            typeElement.classList.add('bad');
        }
        
        // 更新籤詩
        document.getElementById('poemText').textContent = fortune.poem;
        
        // 更新解曰
        document.getElementById('fortuneMeaning').textContent = fortune.meaning;
        
        // 更新各個方面
        document.getElementById('aspectCareer').textContent = fortune.career;
        document.getElementById('aspectWealth').textContent = fortune.wealth;
        document.getElementById('aspectLove').textContent = fortune.love;
        document.getElementById('aspectHealth').textContent = fortune.health;
        
        // 更新香港展望連結
        const hkLink = document.getElementById('hkOutlookLink');
        if (hkLink) {
            hkLink.href = `/hk-outlook?fortune=${fortune.number}`;
        }
        
        // 顯示結果容器
        resultContainer.classList.remove('hidden');
        
        // 滾動到結果
        setTimeout(() => {
            resultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
        
        // Save to history
        const historyEntry = {
            ...fortune,
            timestamp: new Date().toISOString()
        };
        drawHistory.unshift(historyEntry);
        if (drawHistory.length > 10) {
            drawHistory = drawHistory.slice(0, 10);
        }
        localStorage.setItem('fortuneHistory', JSON.stringify(drawHistory));
        localStorage.setItem('lastDrawnFortune', JSON.stringify(fortune));
        updateDrawCount();
    }
    
    // 隱藏結果
    function hideResult() {
        resultContainer.classList.add('hidden');
    }
    
    // Share functionality
    function shareFortune() {
        if (!currentFortune) return;
        
        const shareText = `🎋 122車公求籤結果 🎋\n\n` +
            `第 ${currentFortune.number} 籤 - ${currentFortune.type}\n\n` +
            `📜 籤詩:\n${currentFortune.poem}\n\n` +
            `💼 事業: ${currentFortune.career}\n` +
            `💰 財運: ${currentFortune.wealth}\n` +
            `💕 感情: ${currentFortune.love}\n` +
            `🏥 健康: ${currentFortune.health}\n\n` +
            `誠心求籤，心誠則靈！🙏`;
        
        navigator.clipboard.writeText(shareText).then(() => {
            showShareNotification();
        }).catch(err => {
            console.error('Failed to copy:', err);
            // Fallback
            const textarea = document.createElement('textarea');
            textarea.value = shareText;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            showShareNotification();
        });
    }
    
    function showShareNotification() {
        shareNotification.classList.remove('hidden');
        setTimeout(() => {
            shareNotification.classList.add('hidden');
        }, 2000);
    }
    
    // 求籤主函數
    async function drawFortune() {
        // 隱藏之前的結果
        hideResult();
        
        // 播放搖籤筒聲音
        try {
            playShakeSound();
        } catch (e) {
            console.log('Audio play failed:', e);
        }
        
        // 搖籤筒動畫
        shakeTube();
        
        // 顯示加載畫面
        setTimeout(() => {
            showLoading();
        }, 800);
        
        try {
            // 調用 API 獲取籤文
            const response = await fetch('/api/draw');
            const fortune = await response.json();
            
            // 模擬求籤過程（增加儀式感）
            setTimeout(() => {
                hideLoading();
                
                // 播放成功音效
                try {
                    playSuccessSound();
                } catch (e) {
                    console.log('Audio play failed:', e);
                }
                
                // 顯示結果
                showResult(fortune);
                
            }, 2500);
            
        } catch (error) {
            console.error('Error drawing fortune:', error);
            hideLoading();
            alert('求籤過程中出現錯誤，請稍後再試。');
        }
    }
    
    // 事件監聽器
    drawBtn.addEventListener('click', drawFortune);
    
    redrawBtn.addEventListener('click', function() {
        // 滾動到頂部
        window.scrollTo({ top: 0, behavior: 'smooth' });
        
        // 延遲後再求籤
        setTimeout(() => {
            drawFortune();
        }, 500);
    });
    
    // Share button
    if (shareBtn) {
        shareBtn.addEventListener('click', shareFortune);
    }
    
    // 點擊籤筒也可以求籤
    fortuneTube.addEventListener('click', drawFortune);
    
    // 鍵盤快捷鍵（按空格鍵求籤）
    document.addEventListener('keydown', function(e) {
        if (e.code === 'Space' && resultContainer.classList.contains('hidden')) {
            e.preventDefault();
            drawFortune();
        }
    });
    
    // 添加一些視覺效果
    // 隨機飄落的花瓣效果
    function createPetal() {
        const petal = document.createElement('div');
        const emojis = ['🌸', '🌺', '🌻', '🍃', '✨'];
        petal.innerHTML = emojis[Math.floor(Math.random() * emojis.length)];
        petal.style.position = 'fixed';
        petal.style.left = Math.random() * 100 + 'vw';
        petal.style.top = '-50px';
        petal.style.fontSize = (Math.random() * 20 + 10) + 'px';
        petal.style.opacity = Math.random() * 0.5 + 0.3;
        petal.style.pointerEvents = 'none';
        petal.style.zIndex = '1';
        petal.style.animation = `fall ${Math.random() * 3 + 2}s linear forwards`;
        
        document.body.appendChild(petal);
        
        setTimeout(() => {
            petal.remove();
        }, 5000);
    }
    
    // 添加花瓣飄落的 CSS 動畫
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fall {
            to {
                transform: translateY(100vh) rotate(360deg);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // 每隔一段時間創建花瓣
    setInterval(createPetal, 2000);
    
    console.log('🎋 122車公求籤系統已載入');
    console.log('🙏 誠心誠意，心誠則靈');
    console.log(`📊 已載入 ${drawHistory.length} 條求籤記錄`);
});
