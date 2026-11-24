# -*- coding: utf-8 -*-
"""
张凯雯 19 岁生日祝福页 —— 单文件 Flask 应用
背景：实景极光底图（static/bg_aurora.jpg）· 缓慢推拉 + 呼吸光晕 + 星点/流星
流程：星光凝聚开场 → 打字机贺卡 → 许愿卡展开(不可改) → 一口气吹灭蜡烛 → 常驻互动
"""

from flask import Flask, Response

app = Flask(__name__)

HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<title>徒弟，19岁生日快乐！</title>
<style>
:root{
  --blue1:#0A1628; --blue2:#0F2238;
  --violet:#7C5CFF; --violet-l:#A78BFA;
  --teal:#2EC4B6; --teal-l:#4DD0C4;
  --gold:#F5D76E; --pink:#FFB3C6; --cream:#F1F5F9;
}
*{box-sizing:border-box; -webkit-tap-highlight-color:transparent;}
html,body{height:100%; margin:0;}
body{
  background:#04040e;
  color: var(--cream);
  font-family:"PingFang SC","Microsoft YaHei","Noto Sans SC",system-ui,sans-serif;
  overflow:hidden;
}

/* ===== 背景：极光实景底图 + 缓慢推拉 ===== */
#bg-photo{
  position:fixed; inset:-7%;
  z-index:0; pointer-events:none;
  background-image:url("/static/bg_aurora.jpg");
  background-size:cover;
  background-position:center 42%;
  animation: bgDrift 72s ease-in-out infinite alternate;
  will-change: transform;
  transform: translateZ(0);
}
@keyframes bgDrift{
  0%   { transform: scale(1.03) translate3d(-1.2%, -0.4%, 0); }
  100% { transform: scale(1.11) translate3d( 1.2%,  0.9%, 0); }
}
/* 极光呼吸光晕，让画面活起来 */
#bg-glow{
  position:fixed; inset:0; z-index:1; pointer-events:none;
  background:
    radial-gradient(58% 46% at 50% 26%, rgba(196,130,255,.16) 0%, rgba(196,130,255,0) 72%),
    radial-gradient(48% 40% at 78% 18%, rgba(140,255,214,.10) 0%, rgba(140,255,214,0) 74%);
  animation: glowPulse 11s ease-in-out infinite alternate;
}
@keyframes glowPulse{ from{ opacity:.45; } to{ opacity:1; } }
/* 暗角 / 颗粒 */
#bg-vignette{
  position:fixed; inset:0; z-index:2; pointer-events:none;
  background:
    radial-gradient(132% 110% at 50% 42%, rgba(0,0,0,0) 52%, rgba(3,4,12,.16) 82%, rgba(1,2,7,.36) 100%),
    linear-gradient(180deg, rgba(4,4,14,.16) 0%, rgba(4,4,14,0) 18%, rgba(4,4,14,0) 70%, rgba(3,3,10,.22) 100%);
}
#bg-grain{
  position:fixed; inset:0; z-index:3; pointer-events:none;
  opacity:.055;
  background-image:url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)' opacity='0.55'/%3E%3C/svg%3E");
  background-size:160px 160px;
}
/* ===== 星光层 ===== */
#bg-stars{
  position:fixed; inset:0;
  z-index:1;
  display:block; pointer-events:none;
}
/* ===== 烟花 / 特效层 ===== */
#fx-canvas{position:fixed; inset:0; z-index:5; pointer-events:none;}

/* ========== 进入遮罩（更透，让极光透出来） ========== */
#gate{
  position:fixed; inset:0; z-index:100;
  display:flex; align-items:center; justify-content:center;
  background: radial-gradient(680px 560px at 50% 46%, rgba(8,10,26,.16) 0%, rgba(3,6,16,.56) 90%);
  transition: opacity .9s ease;
  padding:24px;
}
#gate.hide{opacity:0; pointer-events:none;}
.gate-inner{
  text-align:center; max-width:520px;
  padding:30px 34px 26px; border-radius:26px;
  background:linear-gradient(160deg, rgba(34,24,72,.82) 0%, rgba(12,10,32,.88) 65%, rgba(7,7,20,.90) 100%);
  border:1px solid rgba(186,158,255,.34);
  box-shadow:0 24px 70px rgba(0,0,0,.5), 0 0 60px rgba(160,110,255,.14), inset 0 1px 0 rgba(255,255,255,.07);
  backdrop-filter:blur(9px) saturate(1.15);
}
.gate-icon{font-size:54px; margin-bottom:10px; animation:floaty 3s ease-in-out infinite;}
@keyframes floaty{0%,100%{transform:translateY(0);}50%{transform:translateY(-10px);}}
.gate-inner h1{
  text-shadow:0 2px 10px rgba(0,0,0,.75), 0 0 34px rgba(0,0,0,.6);
  font-size:clamp(22px,5.5vw,32px); margin:0 0 10px;
  background:linear-gradient(90deg,#FFE9A8,#86E6D6,#FFC2D6);
  -webkit-background-clip:text; background-clip:text; color:transparent;
}
.gate-inner p{color:#dbe4f3; font-size:14px; margin:6px 0 22px; text-shadow:0 1px 4px rgba(0,0,0,.85), 0 0 18px rgba(0,0,0,.6);}
.gate-hint{font-size:12px !important; color:#9db0c8 !important; margin-top:16px !important; text-shadow:0 1px 4px rgba(0,0,0,.9) !important;}

button{font-family:inherit; cursor:pointer; border:none; outline:none;}

.primary-btn{
  padding:12px 28px; border-radius:999px; font-size:15px; color:#08131f; font-weight:700;
  background:linear-gradient(135deg,var(--gold),var(--teal-l));
  box-shadow:0 0 22px rgba(46,196,182,.45), 0 0 44px rgba(245,215,110,.18);
  transition: transform .18s, box-shadow .18s;
}
.primary-btn:hover{transform:translateY(-2px); box-shadow:0 0 30px rgba(46,196,182,.7), 0 0 60px rgba(245,215,110,.3);}
.primary-btn:active{transform:scale(.97);}
.ghost-btn{
  padding:10px 22px; border-radius:999px; font-size:14px; color:var(--cream);
  background:rgba(167,139,250,.10); border:1px solid rgba(167,139,250,.45);
  transition: background .2s, border-color .2s;
}
.ghost-btn:hover{background:rgba(167,139,250,.22); border-color:var(--violet-l);}
.hidden{display:none !important;}

/* ========== 舞台与场景 ========== */
#stage{position:fixed; inset:0; z-index:10; display:none;}
#stage.show{display:block;}
.scene{
  position:absolute; inset:0;
  display:flex; align-items:center; justify-content:center;
  opacity:0; pointer-events:none; transition:opacity .8s ease;
  padding:22px; overflow-y:auto;
}
.scene.active{opacity:1; pointer-events:auto;}

/* 场景1：粒子文字 */
#scene-intro{cursor:default;}
.intro-scrim{
  position:absolute; inset:0; z-index:0; pointer-events:none;
  background:radial-gradient(62% 46% at 50% 50%, rgba(3,5,16,.60) 0%, rgba(3,5,16,.44) 42%, rgba(3,5,16,.24) 66%, rgba(3,5,16,.08) 86%, rgba(3,5,16,0) 100%);
}
#text-canvas{width:100%; height:100%; position:relative; z-index:1;}

/* 卡片通用 */
.card{
  width:min(560px,92vw);
  background:linear-gradient(160deg, rgba(24,20,50,.82), rgba(10,10,26,.90));
  border:1px solid rgba(167,139,250,.4);
  border-radius:20px;
  padding:26px 24px;
  box-shadow:0 0 40px rgba(167,139,250,.18), 0 0 80px rgba(255,179,198,.10), inset 0 1px 0 rgba(255,255,255,.06);
  backdrop-filter: blur(10px);
}
.card-head{
  font-size:14px; color:var(--violet-l); letter-spacing:.5px; margin-bottom:16px;
  display:flex; align-items:center; gap:8px;
}

/* 场景2：打字机 */
.typewriter{font-size:clamp(14px,3.6vw,16.5px); line-height:1.95; min-height:160px; word-break:break-word;}
.typewriter .line-1{font-size:clamp(18px,4.6vw,22px); font-weight:700; color:var(--gold); display:inline-block; margin-bottom:6px;}
.typewriter .line-3{color:#cfd9ea;}
.typewriter .num{color:var(--pink); font-weight:700; font-variant-numeric:tabular-nums; text-shadow:0 0 12px rgba(255,179,198,.55);}
#to-wish{margin-top:22px; display:block; margin-left:auto;}

/* 场景3：许愿卡 S5 展开 */
.wish-perspective{perspective:1400px; width:min(560px,92vw);}
.wish-card{
  transform-origin:top center; transform:rotateX(-92deg); opacity:0;
  transition:transform 1s cubic-bezier(.2,.85,.25,1), opacity .6s ease;
}
.wish-card.open{transform:rotateX(0); opacity:1;}
.wish-head{font-size:16px; font-weight:700; color:var(--gold); margin-bottom:10px;}
.wish-tip{font-size:13px; color:#a394bf; margin:0 0 16px;}
#wish-input{
  width:100%; min-height:96px; resize:vertical; border-radius:12px; padding:12px 14px;
  background:rgba(16,14,36,.85); color:var(--cream); font-size:14px; line-height:1.7;
  border:1px solid rgba(167,139,250,.45); outline:none; font-family:inherit;
  transition:border-color .2s, box-shadow .2s;
}
#wish-input:focus{border-color:var(--violet-l); box-shadow:0 0 0 3px rgba(167,139,250,.22);}
#seal-wish{margin-top:16px; display:block; margin-left:auto;}
.locked-label{font-size:13px; color:var(--violet-l); margin:0 0 10px;}
.wish-text{
  font-size:clamp(16px,4vw,19px); line-height:1.8; color:var(--cream);
  padding:14px 16px; border-radius:12px; background:rgba(255,179,198,.08);
  border-left:3px solid var(--pink); word-break:break-word;
}
.locked-note{font-size:12.5px; color:#8b7f9f; margin:12px 0 20px;}
#to-cake{display:block; margin-left:auto;}

/* 场景4：蛋糕 */
.cake-area{display:flex; flex-direction:column; align-items:center; gap:18px; text-align:center;}
.cake-hint{
  font-size:clamp(13px,3.4vw,15px); color:var(--gold); margin:0; line-height:1.7;
  text-shadow:0 1px 4px rgba(0,0,0,.9), 0 0 18px rgba(245,215,110,.45); max-width:420px;
}
.cake{display:flex; flex-direction:column; align-items:center; filter:drop-shadow(0 18px 30px rgba(0,0,0,.5));}
.candle-row{display:flex; justify-content:space-around; align-items:flex-end; height:46px; padding:0 6px;}
#row-upper{width:180px;}
#row-lower{width:262px;}
.layer{border-radius:10px 10px 6px 6px; position:relative;}
.layer-upper{
  width:180px; height:58px;
  background:linear-gradient(180deg,#3b2c66,#211a42);
  border-top:6px solid rgba(241,245,249,.9);
  box-shadow:0 0 26px rgba(167,139,250,.45);
}
.layer-lower{
  width:262px; height:72px;
  background:linear-gradient(180deg,#4a3670,#1e1738);
  border-top:7px solid rgba(241,245,249,.9);
  box-shadow:0 0 34px rgba(255,179,198,.28);
}
.candle{position:relative; width:9px; display:flex; flex-direction:column; align-items:center; justify-content:flex-end; cursor:pointer;}
.stick{
  width:7px; height:27px; border-radius:3px;
  background:repeating-linear-gradient(45deg,#F1F5F9,#F1F5F9 4px,var(--pink) 4px,var(--pink) 8px);
}
.flame{
  width:12px; height:17px; margin-bottom:2px;
  border-radius:50% 50% 50% 50% / 62% 62% 38% 38%;
  background:radial-gradient(ellipse at 50% 68%, var(--gold) 0%, var(--gold) 40%, var(--pink) 74%, rgba(255,179,198,0) 100%);
  box-shadow:0 0 12px var(--gold), 0 0 24px rgba(255,179,198,.85);
  transform-origin:bottom center;
  animation:flicker 1.15s infinite alternate ease-in-out;
}
@keyframes flicker{
  0%{transform:scale(1) rotate(-2deg); opacity:.95;}
  50%{transform:scale(1.1) rotate(2deg); opacity:1;}
  100%{transform:scale(.94) rotate(-1deg); opacity:.9;}
}
.candle.out .flame{animation:blowout .5s forwards ease-out;}
@keyframes blowout{
  0%{transform:scale(1); opacity:1;}
  60%{transform:scale(.7) translateY(-8px); opacity:.5;}
  100%{transform:scale(.1) translateY(-18px); opacity:0;}
}
.cake-tip{font-size:13px; color:#c3b8d8; margin:0; text-shadow:0 1px 4px rgba(0,0,0,.85);}

/* 场景4/5 的暗底，保证亮极光上文字可读 */
#scene-cake{
  background:radial-gradient(46% 40% at 50% 50%, rgba(3,4,12,.74) 0%, rgba(3,4,12,.42) 52%, rgba(3,4,12,.10) 76%, rgba(3,4,12,0) 100%);
}
#scene-final{
  background:radial-gradient(40% 34% at 50% 50%, rgba(2,3,10,.82) 0%, rgba(2,3,10,.50) 54%, rgba(2,3,10,.14) 78%, rgba(2,3,10,0) 100%);
}

/* 场景5：常驻 */
.final-wrap{text-align:center; max-width:560px;}
.final-title{
  font-size:clamp(20px,5vw,28px); margin:0 0 8px;
  background:linear-gradient(90deg,var(--gold),var(--pink),var(--violet-l));
  -webkit-background-clip:text; background-clip:text; color:transparent;
  filter:drop-shadow(0 2px 6px rgba(0,0,0,.8));
}
.final-sub{font-size:15px; color:#efe6ff; margin:0 0 18px; text-shadow:0 1px 6px rgba(0,0,0,.85);}
.final-wish{
  font-size:15px; line-height:1.8; color:var(--cream);
  padding:14px 18px; border-radius:14px;
  background:rgba(255,179,198,.10); border:1px solid rgba(255,179,198,.30);
  margin-bottom:22px; word-break:break-word; backdrop-filter: blur(6px);
}
.final-btns{display:flex; flex-wrap:wrap; gap:12px; justify-content:center;}
.final-tip{font-size:12px; color:#c2b6d8; margin-top:20px; text-shadow:0 1px 4px rgba(0,0,0,.85);}

/* 页脚重置 */
.site-footer{
  position:fixed; left:0; right:0; bottom:8px; z-index:20;
  text-align:center; pointer-events:none;
}
.reset-link{
  pointer-events:auto; font-size:11px; color:#5a4e78; cursor:pointer;
  letter-spacing:.5px; transition:color .2s;
}
.reset-link:hover{color:var(--violet-l);}

/* 二次确认弹窗 */
.modal{
  position:fixed; inset:0; z-index:200; display:flex; align-items:center; justify-content:center;
  background:rgba(4,6,16,.80); backdrop-filter:blur(4px);
  animation:fadeIn .25s ease;
}
@keyframes fadeIn{from{opacity:0;}to{opacity:1;}}
.modal-box{
  width:min(360px,86vw); text-align:center; padding:26px 22px; border-radius:18px;
  background:linear-gradient(160deg,#241c48,#100c26);
  border:1px solid rgba(167,139,250,.5);
  box-shadow:0 0 50px rgba(167,139,250,.30);
}
.modal-box p{font-size:15px; line-height:1.8; margin:0 0 22px; color:var(--cream);}
.modal-btns{display:flex; gap:12px; justify-content:center;}

/* 静音按钮 */
#mute-btn{
  position:fixed; top:14px; right:14px; z-index:150;
  width:40px; height:40px; border-radius:50%; font-size:17px;
  background:rgba(28,22,56,.7); border:1px solid rgba(167,139,250,.4);
  color:var(--cream); backdrop-filter:blur(4px);
  display:flex; align-items:center; justify-content:center;
  transition:background .2s;
}
#mute-btn:hover{background:rgba(255,179,198,.25);}
</style>
</head>
<body>

<!-- 极光底图 -->
<div id="bg-photo"></div>
<div id="bg-glow"></div>
<div id="bg-vignette"></div>
<!-- 星光层 -->
<canvas id="bg-stars"></canvas>
<div id="bg-grain"></div>
<!-- 烟花 / 特效层 -->
<canvas id="fx-canvas"></canvas>

<!-- 进入遮罩 -->
<div id="gate">
  <div class="gate-inner">
    <div class="gate-icon">🎂</div>
    <h1>张凯雯 · 19 岁生日快乐</h1>
    <p>一份来自地球 online 的特殊贺卡，正在等你查收</p>
    <button id="enter-btn" class="primary-btn">点击进入 ✨</button>
    <p class="gate-hint">建议打开声音，效果更好哦</p>
  </div>
</div>

<!-- 主舞台 -->
<main id="stage">

  <!-- 场景1：S1 星光凝聚字幕 -->
  <section id="scene-intro" class="scene active">
    <div class="intro-scrim"></div>
    <canvas id="text-canvas"></canvas>
  </section>

  <!-- 场景2：S3 打字机贺卡 -->
  <section id="scene-card" class="scene">
    <div class="card">
      <div class="card-head">📨 地球 online · 梦想成真贺卡</div>
      <div id="typewriter" class="typewriter"></div>
      <button id="to-wish" class="primary-btn hidden">拆开贺卡 ✉️</button>
    </div>
  </section>

  <!-- 场景3：S5 许愿卡展开 -->
  <section id="scene-wish" class="scene">
    <div class="wish-perspective">
      <div id="wish-card" class="card wish-card">
        <div class="wish-head">🌠 梦想成真贺卡</div>
        <p class="wish-tip">把愿望写下来，封存后不可修改。烛光会替你记住。</p>
        <div id="wish-input-area">
          <textarea id="wish-input" maxlength="120" placeholder="写下你的愿望…（封存后不可修改）"></textarea>
          <button id="seal-wish" class="primary-btn">封存愿望 🔒</button>
        </div>
        <div id="wish-locked" class="hidden">
          <p class="locked-label">你的愿望已封存</p>
          <div id="wish-text" class="wish-text"></div>
          <p class="locked-note">烛光会替你记住 ✨</p>
          <button id="to-cake" class="primary-btn">去吹蜡烛 →</button>
        </div>
      </div>
    </div>
  </section>

  <!-- 场景4：蛋糕 + 19 根蜡烛 -->
  <section id="scene-cake" class="scene">
    <div class="cake-area">
      <p class="cake-hint">把愿望说给烛光听，吹灭的那一刻，它会升上去。</p>
      <div class="cake">
        <div class="candle-row" id="row-upper"></div>
        <div class="layer layer-upper"></div>
        <div class="candle-row" id="row-lower"></div>
        <div class="layer layer-lower"></div>
      </div>
      <p class="cake-tip">点击任意蜡烛，一口气吹灭它们 🕯️</p>
    </div>
  </section>

  <!-- 场景5：常驻互动 -->
  <section id="scene-final" class="scene">
    <div class="final-wrap">
      <h2 class="final-title">愿望已升空 ✨</h2>
      <p class="final-sub">张凯雯，19 岁生日快乐！</p>
      <div class="final-wish" id="final-wish"></div>
      <div class="final-btns">
        <button id="btn-replay-card" class="ghost-btn">重看贺卡</button>
        <button id="btn-fireworks" class="primary-btn">放烟花 🎆</button>
        <button id="btn-back-cake" class="ghost-btn">回到蛋糕</button>
      </div>
      <p class="final-tip">点击页面任意位置，还能放烟花</p>
    </div>
  </section>

</main>

<footer class="site-footer">
  <span id="reset-wish" class="reset-link">重置愿望</span>
</footer>

<!-- 二次确认弹窗 -->
<div id="modal" class="modal hidden">
  <div class="modal-box">
    <p>确认后愿望将不可修改，<br>极光会替你记住。</p>
    <div class="modal-btns">
      <button id="modal-cancel" class="ghost-btn">再想想</button>
      <button id="modal-ok" class="primary-btn">确认封存</button>
    </div>
  </div>
</div>

<button id="mute-btn" title="静音/取消静音">🔊</button>

<audio id="bgm1" src="/static/music/bgm_stage1.mp3" loop preload="auto"></audio>
<audio id="bgm2" src="/static/music/bgm_stage2.mp3" loop preload="auto"></audio>

<script>
/* ================= 工具 ================= */
const sleep = ms => new Promise(r => setTimeout(r, ms));
const DPR = Math.min(window.devicePixelRatio || 1, 2);
const state = { scene:'intro', cardRunning:false, introDone:false, musicStage2:false };

/* =========================================================
   星光粒子（紫粉为主 + 一点白/青点缀）
   ========================================================= */
const starCv  = document.getElementById('bg-stars');
const starCtx = starCv.getContext('2d');
let starParticles = [];

function initStars(){
  starCv.width  = Math.round(innerWidth  * DPR);
  starCv.height = Math.round(innerHeight * DPR);
  starCv.style.width  = innerWidth  + 'px';
  starCv.style.height = innerHeight + 'px';
  starCtx.setTransform(DPR, 0, 0, DPR, 0, 0);

  const count = Math.min(120, Math.floor(innerWidth * innerHeight / 16000));
  starParticles = [];
  for (let i = 0; i < count; i++){
    const r = Math.random();
    starParticles.push({
      x: Math.random() * innerWidth,
      y: Math.random() * innerHeight,
      r: Math.random() * 1.6 + 0.4,
      vx: (Math.random() - 0.5) * 0.14,
      vy: -Math.random() * 0.20 - 0.03,
      color: r < 0.42 ? '#C4A7FF'
           : r < 0.70 ? '#FFB3C6'
           : r < 0.88 ? '#F1F5F9'
           : '#4DD0C4',
      alpha: Math.random() * 0.35 + 0.18,
      phase: Math.random() * Math.PI * 2,
      speed: Math.random() * 0.02 + 0.008
    });
  }
}

function drawStars(){
  starCtx.clearRect(0, 0, innerWidth, innerHeight);
  for (const p of starParticles){
    p.x += p.vx; p.y += p.vy; p.phase += p.speed;
    if (p.y < -12){ p.y = innerHeight + 12; p.x = Math.random() * innerWidth; }
    if (p.x < -12) p.x = innerWidth + 12;
    if (p.x > innerWidth + 12) p.x = -12;
    const a = p.alpha * (0.55 + 0.45 * Math.sin(p.phase));
    starCtx.globalAlpha = Math.max(a, 0);
    starCtx.fillStyle = p.color;
    starCtx.beginPath();
    starCtx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    starCtx.fill();
  }
  starCtx.globalAlpha = 1;
  requestAnimationFrame(drawStars);
}

/* =========================================================
   烟花
   ========================================================= */
const fx     = document.getElementById('fx-canvas');
const fxCtx  = fx.getContext('2d');
let fwParticles = [];

function resizeFx(){
  fx.width  = Math.round(innerWidth  * DPR);
  fx.height = Math.round(innerHeight * DPR);
  fx.style.width  = innerWidth  + 'px';
  fx.style.height = innerHeight + 'px';
  fxCtx.setTransform(DPR, 0, 0, DPR, 0, 0);
}

const FW_COLORS = ['#F5D76E','#4DD0C4','#C4A7FF','#FFB3C6','#A78BFA','#7C5CFF'];

function spawnBurst(x, y){
  const color = FW_COLORS[Math.floor(Math.random() * FW_COLORS.length)];
  const n = 46 + Math.floor(Math.random() * 22);
  for (let i = 0; i < n; i++){
    const a  = Math.PI * 2 * i / n + Math.random() * 0.22;
    const sp = 1.6 + Math.random() * 3.4;
    fwParticles.push({
      x, y,
      vx: Math.cos(a) * sp,
      vy: Math.sin(a) * sp,
      life: 1,
      decay: 0.011 + Math.random() * 0.012,
      color,
      size: Math.random() * 1.8 + 1
    });
  }
}

function burstFireworks(times){
  for (let i = 0; i < times; i++){
    setTimeout(() => {
      spawnBurst(
        innerWidth  * (0.18 + Math.random() * 0.64),
        innerHeight * (0.12 + Math.random() * 0.42)
      );
    }, i * 170);
  }
}

function fxLoop(){
  fxCtx.clearRect(0, 0, innerWidth, innerHeight);
  for (let i = fwParticles.length - 1; i >= 0; i--){
    const p = fwParticles[i];
    p.vy += 0.045; p.vx *= 0.985; p.vy *= 0.985;
    p.x += p.vx; p.y += p.vy; p.life -= p.decay;
    if (p.life <= 0){ fwParticles.splice(i, 1); continue; }
    fxCtx.globalAlpha = Math.max(p.life, 0);
    fxCtx.fillStyle = p.color;
    fxCtx.beginPath();
    fxCtx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
    fxCtx.fill();
  }
  fxCtx.globalAlpha = 1;
  requestAnimationFrame(fxLoop);
}

/* =========================================================
   音乐
   ========================================================= */
const bgm1  = document.getElementById('bgm1');
const bgm2  = document.getElementById('bgm2');
let muted   = false;

function fadeIn(audio, target, dur){
  target = target || 0.5; dur = dur || 2200;
  audio.volume = 0;
  const p = audio.play();
  if (p && p.catch) p.catch(() => {});
  const t0 = performance.now();
  (function step(now){
    // 双重保险：锁定 k 在 0 到 1 之间
    const k = Math.max(0, Math.min(1, (now - t0) / dur));
    // 绝对不允许出现负数音量
    audio.volume = muted ? 0 : Math.max(0, target * k);
    if (k < 1) requestAnimationFrame(step);
  })(t0);
}

function fadeOut(audio, dur){
  dur = dur || 1200;
  const t0 = performance.now(), v0 = audio.volume;
  (function step(now){
    // 双重保险：锁定 k 在 0 到 1 之间
    const k = Math.max(0, Math.min(1, (now - t0) / dur));
    // 绝对不允许出现负数音量
    audio.volume = muted ? 0 : Math.max(0, v0 * (1 - k));
    if (k < 1) requestAnimationFrame(step);
    else audio.pause();
  })(t0);
}

/* =========================================================
   场景切换
   ========================================================= */
const SCENES = ['intro','card','wish','cake','final'];

function goScene(name){
  SCENES.forEach(s => {
    const el = document.getElementById('scene-' + s);
    if (el) el.classList.toggle('active', s === name);
  });
  state.scene = name;

  if (name === 'card') runTypewriter();

  if (name === 'wish'){
    setTimeout(() => document.getElementById('wish-card').classList.add('open'), 140);
    if (!state.musicStage2){
      state.musicStage2 = true;
      fadeOut(bgm1, 900);
      setTimeout(() => fadeIn(bgm2, 0.5, 2000), 700);
    }
  }

  if (name === 'cake') resetCandles();

  if (name === 'final'){
    const w = localStorage.getItem('zkw_wish') || '';
    document.getElementById('final-wish').textContent =
      w ? '你的愿望：' + w : '愿望已随风升空。';
    burstFireworks(3);
  }
}

/* =========================================================
   场景1：S1 粒子文字凝聚
   ========================================================= */
let introRaf = 0;

function playIntroText(){
  const canvas = document.getElementById('text-canvas');
  const ctx = canvas.getContext('2d');
  const W = canvas.clientWidth || innerWidth;
  const H = canvas.clientHeight || innerHeight;
  canvas.width  = W * DPR;
  canvas.height = H * DPR;
  ctx.setTransform(DPR, 0, 0, DPR, 0, 0);

  const s1 = Math.min(W * 0.17, 92);
  const s2 = Math.min(W * 0.12, 66);

  /* 取样：把两行字画到离屏画布，再按像素取点当作粒子目标 */
  const off = document.createElement('canvas');
  off.width = W; off.height = H;
  const octx = off.getContext('2d');
  octx.fillStyle = '#fff';
  octx.textAlign = 'center';
  octx.textBaseline = 'middle';

  octx.font = '700 ' + s1 + 'px "PingFang SC","Microsoft YaHei",sans-serif';
  octx.fillText('张凯雯', W / 2, H / 2 - s1 * 0.62);

  octx.font = '700 ' + s2 + 'px "PingFang SC","Microsoft YaHei",sans-serif';
  octx.fillText('19 岁生日快乐', W / 2, H / 2 + s1 * 0.55);

  const data = octx.getImageData(0, 0, W, H).data;
  const targets = [];
  const gap = 3;
  for (let y = 0; y < H; y += gap){
    for (let x = 0; x < W; x += gap){
      if (data[(y * W + x) * 4 + 3] > 128) targets.push({ x, y });
    }
  }

  /* 彩色星空：金 / 珊瑚粉 / 薄荷青 / 薰衣草紫 / 月白 */
  const PALETTE = [
    { c:'#FFC061', w:0.24 },  // 琥珀金
    { c:'#FF8FB2', w:0.22 },  // 桃粉
    { c:'#6FE7D6', w:0.22 },  // 青绿
    { c:'#A896FF', w:0.20 },  // 紫罗兰
    { c:'#FFFFFF', w:0.12 }   // 少量高光
  ];
  function pickColor(){
    let r = Math.random(), acc = 0;
    for (const p of PALETTE){ acc += p.w; if (r <= acc) return p.c; }
    return PALETTE[PALETTE.length - 1].c;
  }

  const parts = targets.map(t => {
    const starry = Math.random() < 0.12;   /* 少量做成小十字星 */
    const small = t.y > H / 2;             /* 第二行字更小，粒子给粗一点 */
    return {
      x: Math.random() * W, y: Math.random() * H,
      tx: t.x, ty: t.y,
      color: pickColor(),
      size: starry ? Math.random() * 1.2 + 2.2
                   : (small ? Math.random() * 0.9 + 1.45 : Math.random() * 1.0 + 1.15),
      starry,
      ph: Math.random() * 6.283,
      tw: Math.random() * 0.6 + 0.4        /* 闪烁幅度 */
    };
  });

  const t0 = performance.now();
  const CONV = 0.065;

  function frame(now){
    const elapsed = now - t0;
    const t = elapsed * 0.001;
    ctx.clearRect(0, 0, W, H);

    /* 先收敛位置 */
    for (const p of parts){
      p.x += (p.tx - p.x) * CONV;
      p.y += (p.ty - p.y) * CONV;
    }

    /* ① 极淡的彩色辉光（lighter，透明度压很低，避免叠成一团白） */
    ctx.globalCompositeOperation = 'lighter';
    for (const p of parts){
      const a = 0.07 + 0.04 * Math.sin(t * 2.1 + p.ph) * p.tw;
      ctx.globalAlpha = a;
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size * 1.95, 0, Math.PI * 2);
      ctx.fill();
    }

    /* ② 一层很淡的暗底，把笔画从亮星云上分离出来 */
    ctx.globalCompositeOperation = 'source-over';
    ctx.fillStyle = 'rgba(4,6,18,1)';
    /* 汇集中途不压暗（否则像一串圆环），字成形后才逐渐托底 */
    const darkA = 0.26 * Math.min(1, Math.max(0, (elapsed - 700) / 900));
    ctx.globalAlpha = darkA;
    for (const p of parts){
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size * 1.5, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1;

    /* ③ 实心粒子本体（source-over，颜色不被加亮洗掉） */
    for (const p of parts){
      const pulse = 0.86 + 0.14 * Math.sin(t * 2.6 + p.ph);
      ctx.globalAlpha = Math.min(1, pulse);
      ctx.fillStyle = p.color;
      if (p.starry){
        const r = p.size * 0.95;
        ctx.beginPath();
        ctx.arc(p.x, p.y, r * 0.42, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = p.color;
        ctx.lineWidth = 0.9;
        ctx.beginPath();
        ctx.moveTo(p.x - r, p.y); ctx.lineTo(p.x + r, p.y);
        ctx.moveTo(p.x, p.y - r); ctx.lineTo(p.x, p.y + r);
        ctx.stroke();
      } else {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size * 0.95, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    ctx.globalAlpha = 1;
    ctx.globalCompositeOperation = 'source-over';

    if (elapsed < 4200){
      introRaf = requestAnimationFrame(frame);
    } else {
      cancelAnimationFrame(introRaf);
      finishIntro();
    }
  }
  introRaf = requestAnimationFrame(frame);

  setTimeout(() => { canvas.parentElement.style.cursor = 'pointer'; }, 1600);
  canvas.parentElement.onclick = () => { finishIntro(); };
}

function finishIntro(){
  if (state.introDone) return;
  state.introDone = true;
  cancelAnimationFrame(introRaf);
  setTimeout(() => goScene('card'), 500);
}

/* =========================================================
   场景2：S3 打字机
   ========================================================= */
const SEGMENTS = [
  { type:'text', value:'您好，052x玩家！', cls:'line-1', preDelay:600 },
  { type:'br' },
  { type:'text', value:'地球🌍online服务器显示，您于2007.11.28注册该账号，在线累计', cls:'line-2' },
  { type:'num', value:6941, suffix:'天，换算为小时为' },
  { type:'num', value:166584, suffix:'h。' },
  { type:'br' },
  { type:'text', value:'这边为您特别申请了一封梦想成真贺卡（写了一定会实现哦～），请注意查收(^_^)a', cls:'line-3' }
];

async function runTypewriter(){
  if (state.cardRunning) return;
  state.cardRunning = true;

  const el = document.getElementById('typewriter');
  el.innerHTML = '';
  document.getElementById('to-wish').classList.add('hidden');

  const SPEED = 52;

  for (const seg of SEGMENTS){
    if (seg.type === 'br'){
      el.appendChild(document.createElement('br'));
      await sleep(260);
      continue;
    }
    if (seg.type === 'text'){
      if (seg.preDelay) await sleep(seg.preDelay);
      const span = document.createElement('span');
      if (seg.cls) span.className = seg.cls;
      el.appendChild(span);
      for (const ch of seg.value){
        span.textContent += ch;
        await sleep(SPEED + Math.random() * 28);
      }
      continue;
    }
    if (seg.type === 'num'){
      const span = document.createElement('span');
      span.className = 'num';
      el.appendChild(span);
      const dur = 900, t0 = performance.now();
      await new Promise(res => {
        (function tick(now){
          const k = Math.min(1, (now - t0) / dur);
          const eased = 1 - Math.pow(1 - k, 3);
          span.textContent = Math.round(seg.value * eased).toLocaleString('en-US');
          if (k < 1) requestAnimationFrame(tick);
          else { span.textContent = seg.value.toLocaleString('en-US'); res(); }
        })(t0);
      });
      const suf = document.createElement('span');
      suf.textContent = seg.suffix;
      el.appendChild(suf);
      await sleep(220);
    }
  }

  const btn = document.getElementById('to-wish');
  btn.classList.remove('hidden');
  btn.onclick = () => goScene('wish');
}

/* =========================================================
   场景3：许愿
   ========================================================= */
function lockWish(v){
  document.getElementById('wish-input-area').classList.add('hidden');
  document.getElementById('wish-locked').classList.remove('hidden');
  document.getElementById('wish-text').textContent = v;
}

function loadWish(){
  const saved = localStorage.getItem('zkw_wish');
  if (saved) lockWish(saved);
}

document.getElementById('seal-wish').addEventListener('click', () => {
  const v = document.getElementById('wish-input').value.trim();
  if (!v){ document.getElementById('wish-input').focus(); return; }
  document.getElementById('modal').classList.remove('hidden');
});

document.getElementById('modal-cancel').addEventListener('click', () => {
  document.getElementById('modal').classList.add('hidden');
});

document.getElementById('modal-ok').addEventListener('click', () => {
  const v = document.getElementById('wish-input').value.trim();
  localStorage.setItem('zkw_wish', v);
  document.getElementById('modal').classList.add('hidden');
  lockWish(v);
});

document.getElementById('to-cake').addEventListener('click', () => goScene('cake'));

/* =========================================================
   场景4：蛋糕与蜡烛（一口气吹灭）
   ========================================================= */
let litCount = 19;
let blowing  = false;   // 防止"一口气"动画期间重复触发

function makeCandle(){
  const d = document.createElement('div');
  d.className = 'candle lit';
  d.innerHTML = '<div class="flame"></div><div class="stick"></div>';
  d.addEventListener('click', blowAll);
  return d;
}

function buildCandles(){
  const up  = document.getElementById('row-upper');
  const low = document.getElementById('row-lower');
  for (let i = 0; i < 7;  i++) up.appendChild(makeCandle());
  for (let i = 0; i < 12; i++) low.appendChild(makeCandle());
  litCount = 19;
}

function resetCandles(){
  blowing = false;
  document.querySelectorAll('.candle').forEach(c => {
    c.classList.add('lit');
    c.classList.remove('out');
  });
  litCount = 19;
}

/* 点击任意蜡烛 → 一口气吹灭全部
   按屏幕 x 坐标从左到右依次快速熄灭，模拟"一口气扫过去" */
function blowAll(e){
  if (blowing) return;
  const candles = Array.from(document.querySelectorAll('.candle.lit'));
  if (candles.length === 0) return;
  blowing = true;

  /* 点击位置的小爆发：作为"气口"起点 */
  if (e && typeof e.clientX === 'number'){
    spawnBurst(e.clientX, e.clientY);
  }

  /* 按屏幕 x 坐标排序，风从左向右扫 */
  const sorted = candles
    .map(el => ({ el, x: el.getBoundingClientRect().left }))
    .sort((a, b) => a.x - b.x);

  /* 依次快速熄灭：每根错开 30ms，19 根约 570ms 扫完 */
  sorted.forEach((item, i) => {
    setTimeout(() => {
      const c = item.el;
      if (!c.classList.contains('lit')) return;
      c.classList.remove('lit');
      c.classList.add('out');
      litCount--;
      /* 每根熄灭时的微粒，形成"气流扫过"的轨迹 */
      const r = c.getBoundingClientRect();
      spawnBurst(r.left + r.width / 2, r.top + 4);
    }, i * 30);
  });

  /* 全部熄灭 → 大烟花 → 转场 */
  const totalDelay = sorted.length * 30 + 220;
  setTimeout(() => {
    litCount = 0;
    burstFireworks(6);
    setTimeout(() => {
      goScene('final');
      blowing = false;
    }, 1700);
  }, totalDelay);
}

/* =========================================================
   场景5：常驻
   ========================================================= */
document.getElementById('btn-fireworks').addEventListener('click', () => burstFireworks(4));
document.getElementById('btn-back-cake').addEventListener('click', () => goScene('cake'));

document.getElementById('btn-replay-card').addEventListener('click', () => {
  state.cardRunning = false;
  document.getElementById('typewriter').innerHTML = '';
  goScene('card');
});

document.getElementById('scene-final').addEventListener('click', (e) => {
  if (e.target.tagName === 'BUTTON') return;
  spawnBurst(e.clientX, e.clientY);
});

/* =========================================================
   重置入口
   ========================================================= */
document.getElementById('reset-wish').addEventListener('click', () => {
  if (confirm('确定要重置愿望吗？这将清除本地保存的愿望内容。')){
    localStorage.removeItem('zkw_wish');
    document.getElementById('wish-input-area').classList.remove('hidden');
    document.getElementById('wish-locked').classList.add('hidden');
    document.getElementById('wish-input').value = '';
    location.reload();
  }
});

/* =========================================================
   进入按钮
   ========================================================= */
document.getElementById('enter-btn').addEventListener('click', () => {
  const gate = document.getElementById('gate');
  gate.classList.add('hide');
  setTimeout(() => { gate.style.display = 'none'; }, 950);

  document.getElementById('stage').classList.add('show');
  fadeIn(bgm1, 0.5, 2400);
  loadWish();
  goScene('intro');
  setTimeout(() => {
    if (state.scene === 'intro' && !state.introDone) playIntroText();
  }, 220);
});

/* =========================================================
   初始化
   ========================================================= */
function boot(){
  initStars();
  requestAnimationFrame(drawStars);

  resizeFx();
  fxLoop();

  buildCandles();
  loadWish();
}

window.addEventListener('resize', () => {
  initStars();
  resizeFx();
});

boot();
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return Response(HTML, mimetype="text/html")


@app.route("/healthz")
def healthz():
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)