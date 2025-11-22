<template>
  <div id="p5-canvas"></div>
</template>

<script>
export default {
  name: 'P5Background',
  mounted() {
    this.loadBackgroundAnimation();
  },
  methods: {
    loadBackgroundAnimation() {
      // Load p5.js first
      const script = document.createElement('script');
      script.src = 'https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.js';
      script.onload = () => {
        // Now load the original background animation
        const animationScript = document.createElement('script');
        animationScript.textContent = `
          // p5.js 背景动画 - Lorenz 吸引子效果
          let a = 4.5;
          let b = 48;
          let c = 9/11;
          let dt = 2e-2;

          let x = 1e-1;
          let y = 0;
          let z = 0;

          let scaleSize = 10;

          let lastReset = 0;    // 上次清屏的时间（毫秒）
          let resetInterval = 30000;   // 30 秒

          function setup() {
            let canvas = createCanvas(windowWidth, windowHeight, WEBGL);
            canvas.parent('p5-canvas');
            background("black");
            lastReset = millis(); // 记录启动时刻
          }

          function draw() {
            // --- 每30秒清屏并重置 Lorenz 系统 ---
            if (millis() - lastReset > resetInterval) {
              background("black");    // 清屏
              x = 1e-1;                // 重置 Lorenz 初始值
              y = 0;
              z = 0;
              lastReset = millis();    // 记录新的时间点
            }

            scale(scaleSize);
            strokeWeight(0.2);
            stroke("white");

            for (let i = 0; i < 58; i++) {
              point(x, y, z);

              x += a * (y - x) * dt;
              y += x * (b - z) * dt;
              z += (x * y - c * z) * dt;
            }
          }

          function windowResized() {
            resizeCanvas(windowWidth, windowHeight);
          }
        `;
        document.head.appendChild(animationScript);
      };
      document.head.appendChild(script);
    }
  }
}
</script>

<style scoped>
#p5-canvas {
  position: fixed;
  inset: 0;
  z-index: -1; /* 确保背景在所有内容之下 */
}
</style>