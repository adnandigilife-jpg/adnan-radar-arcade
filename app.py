import streamlit as st
import streamlit.components.v1 as components

# 1. SAYFA GENEL AYARLARI
st.set_page_config(
    page_title="AdnanRadar Arcade",
    page_icon="🕹️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. ÜST BAŞLIK VE SKOR ALANI
st.markdown("<h1 style='text-align: center; color: #00FF66; font-family: monospace;'>🕹️ ADNAN RADAR ARCADE v1.1</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-family: monospace;'>PC: Yön Tuşları / W-A-S-D<br>MOBİL: Ekranı Parmağınla İstediğin Yöne Kaydır (Swipe)</p>", unsafe_allow_html=True)
st.markdown("---")

# 3. GELİŞMİŞ MOBİL + PC DOKUNMATİK SNAKE MOTORU
game_html = """
<div id="gameContainer" style="text-align: center; font-family: 'Courier New', Courier, monospace; background-color: #0a0a0a; padding: 15px; border-radius: 10px; touch-action: none;">
    <!-- Skor Paneli -->
    <div style="display: flex; justify-content: space-around; margin-bottom: 15px;">
        <div style="font-size: 20px; color: #ffffff; font-weight: bold;">SKOR: <span id="score" style="color: #00FF66;">0</span></div>
        <div style="font-size: 20px; color: #ffffff; font-weight: bold;">EN YÜKSEK SKOR: <span id="highScore" style="color: #FF3366;">0</span></div>
    </div>
    
    <!-- Oyun Alanı -->
    <canvas id="gameCanvas" width="400" height="400" style="border: 4px solid #00FF66; background-color: #111111; box-shadow: 0px 0px 20px rgba(0, 255, 102, 0.3); border-radius: 5px; max-width: 100%; height: auto;"></canvas>
    
    <div style="margin-top: 15px; color: #555; font-size: 13px; font-weight: bold;">
        [PC] Tuşları Kullan | [MOBİL] Parmağınla Kaydır veya Yeniden Başlamak İçin Ekrana Çift Dokun!
    </div>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const scoreElement = document.getElementById("score");
    const highScoreElement = document.getElementById("highScore");
    const gameContainer = document.getElementById("gameContainer");

    const grid = 20;
    let count = 0;
    let score = 0;
    
    let highScore = localStorage.getItem("snake_high_score") || 0;
    highScoreElement.innerText = highScore;
    
    let snake = {
        x: 160,
        y: 160,
        dx: grid,
        dy: 0,
        cells: [{x: 160, y: 160}, {x: 140, y: 160}, {x: 120, y: 160}],
        maxCells: 3
    };
    
    let apple = { x: 300, y: 300 };

    function getRandomInt(min, max) {
        return Math.floor(Math.random() * (max - min)) + min;
    }

    function resetGame() {
        if (score > highScore) {
            highScore = score;
            localStorage.setItem("snake_high_score", highScore);
            highScoreElement.innerText = highScore;
        }
        
        snake.x = 160;
        snake.y = 160;
        snake.cells = [{x: 160, y: 160}, {x: 140, y: 160}, {x: 120, y: 160}];
        snake.maxCells = 3;
        snake.dx = grid;
        snake.dy = 0;
        score = 0;
        scoreElement.innerText = score;
        generateApple();
    }

    function generateApple() {
        apple.x = getRandomInt(0, 20) * grid;
        apple.y = getRandomInt(0, 20) * grid;
        snake.cells.forEach(function(cell) {
            if (cell.x === apple.x && cell.y === apple.y) {
                generateApple();
            }
        });
    }

    function loop() {
        requestAnimationFrame(loop);

        if (++count < 8) { return; } // Mobil hassasiyeti için hızı çok hafif esnettim
        count = 0;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        snake.x += snake.dx;
        snake.y += snake.dy;

        if (snake.x < 0 || snake.x >= canvas.width || snake.y < 0 || snake.y >= canvas.height) {
            resetGame();
        }

        snake.cells.unshift({x: snake.x, y: snake.y});

        if (snake.cells.length > snake.maxCells) {
            snake.cells.pop();
        }

        // Elma Çiz
        ctx.fillStyle = '#FF3366';
        ctx.fillRect(apple.x, apple.y, grid-1, grid-1);

        // Yılanı Çiz
        snake.cells.forEach(function(cell, index) {
            if (index === 0) {
                ctx.fillStyle = '#00FF66';
            } else {
                ctx.fillStyle = '#00CC52';
            }
            
            ctx.fillRect(cell.x, cell.y, grid-1, grid-1);

            if (cell.x === apple.x && cell.y === apple.y) {
                snake.maxCells++;
                score += 10;
                scoreElement.innerText = score;
                generateApple();
            }

            for (let i = index + 1; i < snake.cells.length; i++) {
                if (cell.x === snake.cells[i].x && cell.y === snake.cells[i].y) {
                    resetGame();
                }
            }
        });
    }

    // --- 💻 PC KLAVYE KONTROLLERİ ---
    document.addEventListener('keydown', function(e) {
        if ((e.which === 37 || e.which === 65) && snake.dx === 0) { snake.dx = -grid; snake.dy = 0; e.preventDefault(); }
        else if ((e.which === 38 || e.which === 87) && snake.dy === 0) { snake.dy = -grid; snake.dx = 0; e.preventDefault(); }
        else if ((e.which === 39 || e.which === 68) && snake.dx === 0) { snake.dx = grid; snake.dy = 0; e.preventDefault(); }
        else if ((e.which === 40 || e.which === 83) && snake.dy === 0) { snake.dy = grid; snake.dx = 0; e.preventDefault(); }
        else if (e.which === 32) { resetGame(); e.preventDefault(); }
    });

    // --- 📱 MOBİL DOKUNMATİK (SWIPE) KONTROLLERİ ---
    let touchStartX = 0;
    let touchStartY = 0;
    let touchEndX = 0;
    let touchEndY = 0;

    gameContainer.addEventListener('touchstart', function(e) {
        touchStartX = e.changedTouches[0].screenX;
        touchStartY = e.changedTouches[0].screenY;
    }, false);

    gameContainer.addEventListener('touchend', function(e) {
        touchEndX = e.changedTouches[0].screenX;
        touchEndY = e.changedTouches[0].screenY;
        handleSwipe();
    }, false);

    function handleSwipe() {
        const xDiff = touchEndX - touchStartX;
        const yDiff = touchEndY - touchStartY;
        
        // Hangi yöne daha uzun çekildiğini hesapla (Yatay mı dikey mi)
        if (Math.abs(xDiff) > Math.abs(yDiff)) {
            // Yatay hareket
            if (xDiff > 30 && snake.dx === 0) {
                snake.dx = grid; snake.dy = 0; // Sağa
            } else if (xDiff < -30 && snake.dx === 0) {
                snake.dx = -grid; snake.dy = 0; // Sola
            }
        } else {
            // Dikey hareket
            if (yDiff > 30 && snake.dy === 0) {
                snake.dy = grid; snake.dx = 0; // Aşağı
            } else if (yDiff < -30 && snake.dy === 0) {
                snake.dy = -grid; snake.dx = 0; // Yukarı
            }
        }
    }

    // Mobil için Çift Dokunma (Double Tap) ile Oyunu Yeniden Başlatma
    let lastTap = 0;
    gameContainer.addEventListener('touchend', function(e) {
        const currentTime = new Date().getTime();
        const tapLength = currentTime - lastTap;
        if (tapLength < 300 && tapLength > 0) {
            resetGame();
            e.preventDefault();
        }
        lastTap = currentTime;
    });

    generateApple();
    requestAnimationFrame(loop);
</script>
