import streamlit as st
import streamlit.components.v1 as components

# 1. SAYFA GENEL AYARLARI
st.set_page_config(
    page_title="AdnanRadar Arcade",
    page_icon="🕹️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. ÜST BAŞLIK
st.markdown("<h1 style='text-align: center; color: #00FF66; font-family: monospace;'>🕹️ ADNAN RADAR ARCADE v1.2</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-family: monospace;'>PC: Yön Tuşları / W-A-S-D<br>MOBİL: Ekrandaki Dokunmatik Tuşları Kullanın</p>", unsafe_allow_html=True)
st.markdown("---")

# 3. GELİŞMİŞ MOBİL DOKUNMATİK BUTONLU MOTOR
game_code = """
<div id="gameContainer" style="text-align: center; font-family: 'Courier New', Courier, monospace; background-color: #0a0a0a; padding: 15px; border-radius: 10px; user-select: none; -webkit-user-select: none;">
    
    <!-- Skor Paneli -->
    <div style="display: flex; justify-content: space-around; margin-bottom: 15px;">
        <div style="font-size: 20px; color: #ffffff; font-weight: bold;">SKOR: <span id="score" style="color: #00FF66;">0</span></div>
        <div style="font-size: 20px; color: #ffffff; font-weight: bold;">EN YÜKSEK SKOR: <span id="highScore" style="color: #FF3366;">0</span></div>
    </div>
    
    <!-- Oyun Alanı -->
    <canvas id="gameCanvas" width="400" height="400" style="border: 4px solid #00FF66; background-color: #111111; box-shadow: 0px 0px 20px rgba(0, 255, 102, 0.3); border-radius: 5px; max-width: 100%; height: auto;"></canvas>
    
    <!-- 📱 MOBİL DOKUNMATİK YÖN TUŞLARI TAKIMI -->
    <div style="margin-top: 20px; display: flex; flex-direction: column; align-items: center; gap: 10px;">
        <!-- Yukarı Butonu -->
        <button id="btnUp" style="width: 70px; height: 55px; background-color: #222; color: #00FF66; border: 2px solid #00FF66; border-radius: 10px; font-size: 24px; font-weight: bold; font-family: monospace; box-shadow: 0 4px #111; active { transform: translateY(4px); box-shadow: none; }">▲</button>
        
        <!-- Sol - Yeniden Başla - Sağ Butonları -->
        <div style="display: flex; gap: 20px; align-items: center;">
            <button id="btnLeft" style="width: 70px; height: 55px; background-color: #222; color: #00FF66; border: 2px solid #00FF66; border-radius: 10px; font-size: 24px; font-weight: bold; font-family: monospace; box-shadow: 0 4px #111;">◀</button>
            <button id="btnReset" style="width: 60px; height: 45px; background-color: #333; color: #FF3366; border: 2px solid #FF3366; border-radius: 8px; font-size: 12px; font-weight: bold; font-family: monospace;">YENİ</button>
            <button id="btnRight" style="width: 70px; height: 55px; background-color: #222; color: #00FF66; border: 2px solid #00FF66; border-radius: 10px; font-size: 24px; font-weight: bold; font-family: monospace; box-shadow: 0 4px #111;">▶</button>
        </div>
        
        <!-- Aşağı Butonu -->
        <button id="btnDown" style="width: 70px; height: 55px; background-color: #222; color: #00FF66; border: 2px solid #00FF66; border-radius: 10px; font-size: 24px; font-weight: bold; font-family: monospace; box-shadow: 0 4px #111;">▼</button>
    </div>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const scoreElement = document.getElementById("score");
    const highScoreElement = document.getElementById("highScore");

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

        if (++count < 8) { return; }
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

    // --- 💻 KLAVYE KONTROLLERİ ---
    document.addEventListener('keydown', function(e) {
        if ((e.which === 37 || e.which === 65) && snake.dx === 0) { snake.dx = -grid; snake.dy = 0; e.preventDefault(); }
        else if ((e.which === 38 || e.which === 87) && snake.dy === 0) { snake.dy = -grid; snake.dx = 0; e.preventDefault(); }
        else if ((e.which === 39 || e.which === 68) && snake.dx === 0) { snake.dx = grid; snake.dy = 0; e.preventDefault(); }
        else if ((e.which === 40 || e.which === 83) && snake.dy === 0) { snake.dy = grid; snake.dx = 0; e.preventDefault(); }
        else if (e.which === 32) { resetGame(); e.preventDefault(); }
    });

    // --- 📱 DOKUNMATİK BUTON KONTROLLERİ (MOBİL) ---
    document.getElementById('btnUp').addEventListener('touchstart', function(e) {
        if (snake.dy === 0) { snake.dy = -grid; snake.dx = 0; }
        e.preventDefault();
    });
    document.getElementById('btnDown').addEventListener('touchstart', function(e) {
        if (snake.dy === 0) { snake.dy = grid; snake.dx = 0; }
        e.preventDefault();
    });
    document.getElementById('btnLeft').addEventListener('touchstart', function(e) {
        if (snake.dx === 0) { snake.dx = -grid; snake.dy = 0; }
        e.preventDefault();
    });
    document.getElementById('btnRight').addEventListener('touchstart', function(e) {
        if (snake.dx === 0) { snake.dx = grid; snake.dy = 0; }
        e.preventDefault();
    });
    document.getElementById('btnReset').addEventListener('touchstart', function(e) {
        resetGame();
        e.preventDefault();
    });

    // Bilgisayardan fareyle tıklayanlar için de aktif edelim:
    document.getElementById('btnUp').addEventListener('click', function() { if (snake.dy === 0) { snake.dy = -grid; snake.dx = 0; } });
    document.getElementById('btnDown').addEventListener('click', function() { if (snake.dy === 0) { snake.dy = grid; snake.dx = 0; } });
    document.getElementById('btnLeft').addEventListener('click', function() { if (snake.dx === 0) { snake.dx = -grid; snake.dy = 0; } });
    document.getElementById('btnRight').addEventListener('click', function() { if (snake.dx === 0) { snake.dx = grid; snake.dy = 0; } });
    document.getElementById('btnReset').addEventListener('click', resetGame);

    generateApple();
    requestAnimationFrame(loop);
</script>
"""

# HTML Bileşeni
components.html(game_code, height=720)

# FOOTER
st.markdown("---")
st.markdown("<p style='text-align: center; color: #555; font-size: 12px;'>AdnanRadar Projesi kapsamında sıfırdan geliştirilmiştir.</p>", unsafe_allow_html=True)
