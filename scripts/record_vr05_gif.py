#!/usr/bin/env python3
from __future__ import annotations

import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT_GIF = ROOT / "vr05.gif"

CSS_W = 256
CSS_H = 160
SCALE = 2
FPS = 16
PERIOD = 2 * math.pi / 1.7
FRAMES = round(PERIOD / 0.011 / 60 * FPS)
OUT_W = CSS_W * SCALE
MAX_COLORS = 256

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
  html,body{margin:0;background:#0A0A0B;}
  #stage{width:256px;height:160px;}
  canvas{
    width:256px;height:160px;display:block;
    border:1px solid #26262B;border-radius:2px;
    background:linear-gradient(180deg,#111113,#0A0A0B);
  }
</style></head><body>
<div id="stage"><canvas id="c" width="512" height="320"></canvas></div>
<script>
  var GOLD='178,58,58', GREY='140,140,147', BONE_RGB='232,227,214';
  var bbase=[0.45,0.64,0.52,0.78,0.60,0.82,0.68];

  function grid(ctx,W,H){
    ctx.strokeStyle='rgba(38,38,43,0.85)'; ctx.lineWidth=1;
    for(var x=0;x<=W;x+=W/8){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke();}
    for(var y=0;y<=H;y+=H/8){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();}
  }
  function dot(ctx,x,y,r,fill){ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fillStyle=fill;ctx.fill();}
  function glow(ctx,x,y,r,rgb,a){
    var g=ctx.createRadialGradient(x,y,0,x,y,r);
    g.addColorStop(0,'rgba('+rgb+','+a+')'); g.addColorStop(1,'rgba('+rgb+',0)');
    ctx.fillStyle=g; ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.fill();
  }

  function drawBars(ctx,W,H,t){
    grid(ctx,W,H);
    var n=bbase.length,padX=W*0.1,plotW=W-2*padX,slot=plotW/n,gap=slot*0.34,bw=slot-gap;
    var baseY=H*0.84,topY=H*0.16,span=baseY-topY,budget=0.74,byv=baseY-budget*span;
    ctx.save();ctx.setLineDash([5,4]);ctx.beginPath();ctx.moveTo(padX,byv);ctx.lineTo(W-padX,byv);ctx.strokeStyle='rgba('+BONE_RGB+',0.42)';ctx.lineWidth=1;ctx.stroke();ctx.restore();
    for(var i=0;i<n;i++){
      var h=bbase[i]+0.17*Math.sin(t*1.7+i*0.8); if(h<0.06)h=0.06; if(h>0.97)h=0.97;
      var x=padX+i*slot+gap*0.5,hpx=h*span,y=baseY-hpx, over=h>budget;
      var g=ctx.createLinearGradient(0,y,0,baseY);
      g.addColorStop(0,'rgba('+GOLD+','+(over?0.60:0.34)+')');
      g.addColorStop(1,'rgba('+GOLD+',0.04)');
      ctx.fillStyle=g;ctx.fillRect(x,y,bw,hpx);
      if(over){ glow(ctx,x+bw/2,y,bw*0.95,GOLD,0.5); }
      ctx.strokeStyle='rgba('+GOLD+','+(over?0.95:0.7)+')';ctx.lineWidth=1.6;
      ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+bw,y);ctx.stroke();
      if(over){ dot(ctx,x+bw/2,y-4,1.8,'rgba('+GOLD+',0.95)'); }
    }
    ctx.beginPath();ctx.moveTo(padX,baseY);ctx.lineTo(W-padX,baseY);ctx.strokeStyle='rgba('+GREY+',0.45)';ctx.lineWidth=1;ctx.stroke();
  }

  var ctx=document.getElementById('c').getContext('2d');
  ctx.scale(2,2);
  window.renderBars=function(t){
    ctx.clearRect(0,0,256,160);
    drawBars(ctx,256,160,t);
  };
  window.renderBars(0);
</script></body></html>"""


def capture_frames(frame_dir: Path) -> int:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": CSS_W, "height": CSS_H},
            device_scale_factor=SCALE,
        )
        page.set_content(PAGE, wait_until="networkidle")
        canvas = page.locator("#c")
        for k in range(FRAMES):
            t = (k / FRAMES) * PERIOD
            page.evaluate(f"window.renderBars({t})")
            canvas.screenshot(path=str(frame_dir / f"frame_{k:04d}.png"))
        browser.close()
    return FRAMES


def build_gif(frame_dir: Path) -> None:
    palette = frame_dir / "palette.png"
    vf = f"fps={FPS},scale={OUT_W}:-1:flags=lanczos"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(frame_dir / "frame_%04d.png"),
            "-vf",
            f"{vf},palettegen=max_colors={MAX_COLORS}:stats_mode=diff",
            str(palette),
        ],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(frame_dir / "frame_%04d.png"),
            "-i",
            str(palette),
            "-lavfi",
            f"{vf}[x];[x][1:v]paletteuse=dither=sierra2_4a",
            "-loop",
            "0",
            str(OUT_GIF),
        ],
        check=True,
        capture_output=True,
    )


def main() -> None:
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg not found on PATH.")
    frame_dir = Path(tempfile.mkdtemp(prefix="vr05_gif_"))
    try:
        n = capture_frames(frame_dir)
        print(f"Captured {n} frames → assembling GIF…")
        build_gif(frame_dir)
        size_mb = OUT_GIF.stat().st_size / 1e6
        print(f"Wrote {OUT_GIF.name} ({size_mb:.2f} MB)")
    finally:
        shutil.rmtree(frame_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
