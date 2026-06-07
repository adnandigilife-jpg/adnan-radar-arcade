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
st.markdown("<h1 style='text-align: center; color: #00FF66; font-family: monospace;'>🕹️ ADNAN RADAR ARCADE v1.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-family: monospace;'>Yön tuşları (W, A, S, D veya Ok Tuşları) ile oynamaya başlayabilirsin. Yeniden başlamak için BOŞLUK (Space) tuşuna bas.</p>", unsafe_allow_html=True)
st.markdown("---")

# 3. GELİŞMİŞ RETRO SNAKE OYUN MOTORU (HTML5 + LOCALSTORAGE REKOR SİSTEMİ)
game_html = """
<div style="text-align: center; font-family: 'Courier New', Courier, monospace; background-color: #0a0a0a; padding: 20px; border-radius: 10px;">
    <!-- Skor Paneli -->
    <div style="display: flex; justify-content: space-around; margin-bottom: 15px;">
        <div style="font-size: 22px; color: #ffffff; font-weight: bold;">SKOR: <span id="score" style="color: #00FF66;">0</span></div>
        <div style="font-size: 22px; color: #ffffff; font-weight: bold;">EN YÜKSEK SKOR: <span id="highScore" style="color: #FF3366;">0</span></div>
    </div>
    
    <!-- Oyun Alanı -->
    <canvas id="gameCanvas" width="400" height="400" style="border: 4px solid #00FF66; background-color: #111111; box-shadow: 0px 0px 20px rgba(0, 255, 102, 0.3); border-radius: 5px;"></canvas>
    
    <div style="margin-top: 15px; color: #555; font-size: 13px; font-weight: bold;">
        [W-A-S-D] veya [Ok Tuşları] - HAREKET | [Space] - YENİDEN BAŞLA
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
    
    // Tarayıcı hafızasından rekoru çek
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
        // Skor rekoru kırdıysa hafızaya kaydet
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
        
        // Yemin yılanın üstünde çıkmasını engelle
        snake.cells.forEach(function(cell) {
            if (cell.x === apple.x && cell.y === apple.y) {
                generateApple();
            }
        });
    }

    function loop() {
        requestAnimationFrame(loop);

        // Oyun hızı ayarı (Sayı büyüdükçe yılan yavaşlar, ideal hız 6-7 arasıdır)
        if (++count < 7) { return; }
        count = 0;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Yılanın kafasını ilerlet
        snake.x += snake.dx;
        snake.y += snake.dy;

        // Duvarlardan geçme özelliği yerine çarpmayı ölüm sayıyoruz (Adamakıllı zorluk)
        if (snake.x < 0 || snake.x >= canvas.width || snake.y < 0 || snake.y >= canvas.height) {
            resetGame();
        }

        // Gövde takibi
        snake.cells.unshift({x: snake.x, y: snake.y});

        if (snake.cells.length > snake.maxCells) {
            snake.cells.pop();
        }

        // Yemi Çiz (Neon Kırmızı/Turuncu Elma)
        ctx.fillStyle = '#FF3366';
        ctx.shadowBlur = 10;
        ctx.shadowColor = '#FF3366';
        ctx.fillRect(apple.x, apple.y, grid-1, grid-1);

        // Yılanı Çiz (Neon Yeşil)
        ctx.shadowBlur = 0; // Gövdede parlamayı kapat net görünsün
        snake.cells.forEach(function(cell, index) {
            if (index === 0) {
                ctx.fillStyle = '#00FF66'; // Kafa parlak yeşil
            } else {
                ctx.fillStyle = '#00CC52'; // Gövde koyu yeşil
            }
            
            ctx.fillRect(cell.x, cell.y, grid-1, grid-1);

            // Yılan yemi yedi mi?
            if (cell.x === apple.x && cell.y === apple.y) {
                snake.maxCells++;
                score += 10;
                scoreElement.innerText = score;
                generateApple();
            }

            // Kendine çarpma kontrolü
            for (let i = index + 1; i < snake.cells.length; i++) {
                if (cell.x === snake.cells[i].x && cell.y === snake.cells[i].y) {
                    resetGame();
                }
            }
        });
    }

    // Tuş Kontrolleri (Ters yöne ani dönüş engelli)
    document.addEventListener('keydown', function(e) {
        // Sol (A veya Sol Ok)
        if ((e.which === 37 || e.which === 65) && snake.dx === 0) {
            snake.dx = -grid; snake.dy = 0;
            e.preventDefault();
        }
        // Yukarı (W veya Yukarı Ok)
        else if ((e.which === 38 || e.which === 87) && snake.dy === 0) {
            snake.dy = -grid; snake.dx = 0;
            e.preventDefault();
        }
        // Sağ (D veya Sağ Ok)
        if ((e.which === 39 || e.which === 68) && snake.dx === 0) {
            snake.dx = grid; snake.dy = 0;
            e.preventDefault();
        }
        // Aşağı (S veya Aşağı Ok)
        else if ((e.which === 40 || e.which === 83) && snake.dy === 0) {
            snake.dy = grid; snake.dx = 0;
            e.preventDefault();
        }
        // Space (Boşluk) ile Manuel Reset
        else if (e.which === 32) {
            resetGame();
            e.preventDefault();
        }
    });

    // İlk elmayı üret ve motoru çalıştır
    generateApple();
    requestAnimationFrame(loop);
</script>
"""

# HTML Bileşenini ekrana basıyoruz
components.html(game_html, height=520)

# FOOTER BİLGİSİ
st.markdown("---")
st.markdown("<p style='text-align: center; color: #555; font-size: 12px;'>AdnanRadar Projesi kapsamında sıfırdan geliştirilmiştir. Veriler tarayıcı önbelleğinde saklanır.</p>", unsafe_allow_html=True)
