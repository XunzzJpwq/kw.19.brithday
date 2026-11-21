# -*- coding: utf-8 -*-
"""
张凯雯 19 岁生日祝福页 —— 单文件 Flask 应用
背景：紫粉星空感 · 宽幅流动极光 + 星云 + 星光粒子
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
  background:#03040c;
  color: var(--cream);
  font-family:"PingFang SC","Microsoft YaHei","Noto Sans SC",system-ui,sans-serif;
  overflow:hidden;
}

/* ===== 极光层：blur 降低、加亮，让带子更清晰旷阔 ===== */
#bg-aurora{
  position:fixed; inset:-8%;
  z-index:0;
  display:block; pointer-events:none;
  filter: blur(14px) saturate(1.55) brightness(1.08);
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
  background: radial-gradient(900px 700px at 50% 42%, rgba(20,30,60,.35) 0%, rgba(4,8,18,.85) 85%);
  backdrop-filter: blur(2px);
  transition: opacity .9s ease;
  padding:24px;
}
#gate.hide{opacity:0; pointer-events:none;}
.gate-inner{text-align:center; max-width:520px;}
.gate-icon{font-size:54px; margin-bottom:10px; animation:floaty 3s ease-in-out infinite;}
@keyframes floaty{0%,100%{transform:translateY(0);}50%{transform:translateY(-10px);}}
.gate-inner h1{
  font-size:clamp(22px,5.5vw,32px); margin:0 0 10px;
  background:linear-gradient(90deg,var(--gold),var(--teal-l),var(--violet-l));
  -webkit-background-clip:text; background-clip:text; color:transparent;
}
.gate-inner p{color:#a9b8d0; font-size:14px; margin:6px 0 22px;}
.gate-hint{font-size:12px !important; color:#6f7f9a !important; margin-top:16px !important;}

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
#text-canvas{width:100%; height:100%;}

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
  text-shadow:0 0 18px rgba(245,215,110,.35); max-width:420px;
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
.cake-tip{font-size:13px; color:#a394bf; margin:0;}

/* 场景5：常驻 */
.final-wrap{text-align:center; max-width:560px;}
.final-title{
  font-size:clamp(20px,5vw,28px); margin:0 0 8px;
  background:linear-gradient(90deg,var(--gold),var(--pink),var(--violet-l));
  -webkit-background-clip:text; background-clip:text; color:transparent;
}
.final-sub{font-size:15px; color:#c4b8d8; margin:0 0 18px;}
.final-wish{
  font-size:15px; line-height:1.8; color:var(--cream);
  padding:14px 18px; border-radius:14px;
  background:rgba(255,179,198,.10); border:1px solid rgba(255,179,198,.30);
  margin-bottom:22px; word-break:break-word; backdrop-filter: blur(6px);
}
.final-btns{display:flex; flex-wrap:wrap; gap:12px; justify-content:center;}
.final-tip{font-size:12px; color:#7f7495; margin-top:20px;}

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

<!-- 极光层（最底） -->
<canvas id="bg-aurora"></canvas>
<!-- 星光层 -->
<canvas id="bg-stars"></canvas>
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
   极光背景（紫粉星空感 · 宽幅极光带 + 星云）
   ========================================================= */
const auroraCv = document.getElementById('bg-aurora');
const actx     = auroraCv.getContext('2d');
const ADPR     = 1;
let AW = innerWidth, AH = innerHeight;

function sizeAurora(){
  AW = auroraCv.clientWidth  || innerWidth;
  AH = auroraCv.clientHeight || innerHeight;
  auroraCv.width  = Math.round(AW * ADPR);
  auroraCv.height = Math.round(AH * ADPR);
  actx.setTransform(ADPR, 0, 0, ADPR, 0, 0);
}

/* 极光带参数（全部紫粉色系 235~345）
   waves:横向波数  amp:纵向振幅(屏高占比)  spd:流速/方向
   y:中心高度      thick:向下厚度         a:基准透明度
   h1/h2:HSL 色相  phase:相位偏移          */
const AURORA_BANDS = [
  // 主带：紫粉色，最宽最亮，横贯屏幕
  { waves:1.4, amp:0.13, spd: 0.20, y:0.40, thick:0.50, a:0.78, h1:272, h2:318, phase:0.0 },
  // 蓝紫副带：略高
  { waves:2.0, amp:0.10, spd:-0.16, y:0.30, thick:0.44, a:0.64, h1:235, h2:275, phase:1.7 },
  // 粉色带：偏低
  { waves:1.1, amp:0.15, spd: 0.14, y:0.62, thick:0.52, a:0.70, h1:312, h2:346, phase:3.1 },
  // 细节带：细一点，中间层
  { waves:2.8, amp:0.085,spd:-0.24, y:0.48, thick:0.36, a:0.50, h1:255, h2:290, phase:4.6 },
  // 底部粉紫
  { waves:1.7, amp:0.11, spd: 0.18, y:0.72, thick:0.46, a:0.54, h1:290, h2:330, phase:2.4 },
];

/* 远景星云光斑 */
const NEBULAS = [
  { ux:0.22, uy:0.34, ur:0.55, h:285, a:0.20, spdX:0.00035, spdY:0.00020, phase:0.0 },
  { ux:0.78, uy:0.52, ur:0.60, h:325, a:0.16, spdX:-0.00025,spdY:0.00030, phase:2.2 },
  { ux:0.50, uy:0.76, ur:0.68, h:250, a:0.13, spdX:0.00020, spdY:-0.00018,phase:4.1 },
];

function drawAurora(now){
  const t = now * 0.001;
  const W = AW, H = AH;

  /* 深紫夜空底 */
  actx.globalCompositeOperation = 'source-over';
  const sky = actx.createLinearGradient(0, 0, 0, H);
  sky.addColorStop(0,    '#05030f');
  sky.addColorStop(0.42, '#0c0a22');
  sky.addColorStop(0.74, '#080618');
  sky.addColorStop(1,    '#03020a');
  actx.fillStyle = sky;
  actx.fillRect(0, 0, W, H);

  /* —— 远景星云 —— */
  actx.globalCompositeOperation = 'lighter';
  for (const n of NEBULAS){
    const cx = W * n.ux + Math.sin(t * n.spdX * 1000 + n.phase) * W * 0.06;
    const cy = H * n.uy + Math.cos(t * n.spdY * 1000 + n.phase) * H * 0.05;
    const rr = Math.max(W, H) * n.ur;
    const aN = n.a * (0.8 + 0.2 * Math.sin(t * 0.4 + n.phase));
    const g = actx.createRadialGradient(cx, cy, 0, cx, cy, rr);
    g.addColorStop(0.0, `hsla(${n.h}, 90%, 60%, ${aN})`);
    g.addColorStop(0.5, `hsla(${n.h}, 90%, 55%, ${aN * 0.35})`);
    g.addColorStop(1.0, 'rgba(0,0,0,0)');
    actx.fillStyle = g;
    actx.fillRect(0, 0, W, H);
  }

  /* —— 极光带 —— */
  const N = 80;
  for (let bi = 0; bi < AURORA_BANDS.length; bi++){
    const b  = AURORA_BANDS[bi];
    const wf = (b.waves * Math.PI * 2) / W;
    const aMod  = 0.72 + 0.28 * Math.sin(t * 0.55 + b.phase * 1.7);
    const alpha = b.a * aMod;

    const top = [], bot = [], mid = [];
    for (let i = 0; i <= N; i++){
      const u = i / N;
      const x = u * W;
      const w1 = Math.sin(x * wf + t * b.spd + b.phase);
      const w2 = Math.sin(x * wf * 2.7 - t * b.spd * 1.4 + b.phase * 1.9);
      const yc = H * b.y + (w1 * 0.72 + w2 * 0.35) * H * b.amp;
      top.push([x, yc - H * b.thick * 0.38]);
      mid.push([x, yc]);
      bot.push([x, yc + H * b.thick]);
    }

    /* 主带（水平渐变 + 上下略弱） */
    actx.beginPath();
    actx.moveTo(top[0][0], top[0][1]);
    for (let i = 1; i <= N; i++) actx.lineTo(top[i][0], top[i][1]);
    for (let i = N; i >= 0; i--) actx.lineTo(bot[i][0], bot[i][1]);
    actx.closePath();

    const g = actx.createLinearGradient(0, 0, W, 0);
    g.addColorStop(0.00, `hsla(${b.h1}, 95%, 60%, 0)`);
    g.addColorStop(0.20, `hsla(${b.h1}, 95%, 60%, ${alpha * 0.88})`);
    g.addColorStop(0.50, `hsla(${b.h2}, 95%, 70%, ${alpha})`);
    g.addColorStop(0.80, `hsla(${b.h1}, 95%, 60%, ${alpha * 0.85})`);
    g.addColorStop(1.00, `hsla(${b.h1}, 95%, 60%, 0)`);
    actx.fillStyle = g;
    actx.fill();

    /* 亮丝：沿带子中线画一条高光线，形成极光帘幕层次 */
    actx.beginPath();
    actx.moveTo(mid[0][0], mid[0][1]);
    for (let i = 1; i <= N; i++) actx.lineTo(mid[i][0], mid[i][1]);
    const lg = actx.createLinearGradient(0, 0, W, 0);
    lg.addColorStop(0.00, `hsla(${b.h2}, 100%, 80%, 0)`);
    lg.addColorStop(0.25, `hsla(${b.h2}, 100%, 84%, ${alpha * 0.85})`);
    lg.addColorStop(0.50, `hsla(${b.h2}, 100%, 90%, ${alpha})`);
    lg.addColorStop(0.75, `hsla(${b.h2}, 100%, 84%, ${alpha * 0.85})`);
    lg.addColorStop(1.00, `hsla(${b.h2}, 100%, 80%, 0)`);
    actx.strokeStyle = lg;
    actx.lineWidth = 2.6;
    actx.lineCap = 'round';
    actx.stroke();
  }

  /* 顶部氛围辉光 */
  const halo = actx.createRadialGradient(
    W * 0.5, H * 0.14, 0,
    W * 0.5, H * 0.14, Math.max(W, H) * 0.72
  );
  halo.addColorStop(0.0, 'rgba(167,139,250,0.16)');
  halo.addColorStop(0.5, 'rgba(255,179,198,0.07)');
  halo.addColorStop(1.0, 'rgba(0,0,0,0)');
  actx.fillStyle = halo;
  actx.fillRect(0, 0, W, H);

  actx.globalCompositeOperation = 'source-over';
  requestAnimationFrame(drawAurora);
}

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

  const count = Math.min(150, Math.floor(innerWidth * innerHeight / 11000));
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
      alpha: Math.random() * 0.55 + 0.25,
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
    const k = Math.min(1, (now - t0) / dur);
    audio.volume = muted ? 0 : target * k;
    if (k < 1) requestAnimationFrame(step);
  })(t0);
}

function fadeOut(audio, dur){
  dur = dur || 1200;
  const t0 = performance.now(), v0 = audio.volume;
  (function step(now){
    const k = Math.min(1, (now - t0) / dur);
    audio.volume = Math.max(v0 * (1 - k), 0);
    if (k < 1) requestAnimationFrame(step);
    else audio.pause();
  })(t0);
}

document.getElementById('mute-btn').addEventListener('click', function(){
  muted = !muted;
  this.textContent = muted ? '🔇' : '🔊';
  [bgm1, bgm2].forEach(a => { a.muted = muted; });
});

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

  const off = document.createElement('canvas');
  off.width = W; off.height = H;
  const octx = off.getContext('2d');
  octx.fillStyle = '#fff';
  octx.textAlign = 'center';
  octx.textBaseline = 'middle';

  const s1 = Math.min(W * 0.17, 92);
  octx.font = '700 ' + s1 + 'px "PingFang SC","Microsoft YaHei",sans-serif';
  octx.fillText('张凯雯', W / 2, H / 2 - s1 * 0.62);

  const s2 = Math.min(W * 0.115, 64);
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

  const parts = targets.map(t => {
    const r = Math.random();
    return {
      x: Math.random() * W, y: Math.random() * H,
      tx: t.x, ty: t.y,
      color: r < 0.45 ? '#F5D76E' : (r < 0.80 ? '#C4A7FF' : '#FFB3C6'),
      size: Math.random() * 1.5 + 0.6
    };
  });

  const t0 = performance.now();
  function frame(now){
    const elapsed = now - t0;
    ctx.clearRect(0, 0, W, H);
    for (const p of parts){
      p.x += (p.tx - p.x) * 0.065;
      p.y += (p.ty - p.y) * 0.065;
      ctx.globalAlpha = 0.92;
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1;
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
  sizeAurora();
  requestAnimationFrame(drawAurora);

  initStars();
  requestAnimationFrame(drawStars);

  resizeFx();
  fxLoop();

  buildCandles();
  loadWish();
}

window.addEventListener('resize', () => {
  sizeAurora();
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