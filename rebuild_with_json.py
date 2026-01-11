#!/usr/bin/env python3
import json
import subprocess
import shutil
from pathlib import Path

STORY_ORDER = {1:"Schneiderlein",2:"Rotkäppchen",3:"Hänsel und Gretel",4:"Aschenputtel",5:"Schneewittchen",6:"Weihnachtsbaum - Nikolaus",7:"der froschkönig",8:"Rapunzel",9:"Rumpelstilzchen",10:"Bremer Stadtmusikanten",11:"das hässliche Entlein",12:"dornröschen",13:"der gestiefelte kater",14:"König Drosselbart",15:"Hans im Glück",16:"Alibaba",17:"die schöne und das biest",18:"Schneeweißchen und Rosenrot",19:"die Eisköniging",20:"Die kleine Meerjungfrau",21:"Pinocchio",22:"peter pan",23:"Der kleine Prinz",24:"Sterntaler"}

def extract_text(f):
    try:
        return subprocess.run(["pandoc","--track-changes=all",str(f),"-t","plain","--wrap=none"],capture_output=True,text=True,check=True).stdout
    except:
        return ""

def get_story(repo,folder,day):
    p=repo/folder
    if not p.exists():return None
    img=audio=txt=None
    for f in p.glob("*"):
        e=f.suffix.lower()
        if e in['.webp','.png','.jpg','.jpeg']:img=f
        elif e=='.mp3':audio=f
        elif e in['.docx','.pdf','.txt']:txt=f
    if not(img and audio and txt):return None
    text=extract_text(txt)if txt.suffix.lower()=='.docx'else open(txt,'r',encoding='utf-8',errors='ignore').read()
    assets=repo/'assets'
    (assets/'images').mkdir(parents=True,exist_ok=True)
    (assets/'audio').mkdir(parents=True,exist_ok=True)
    new_img=f"day_{day:02d}{img.suffix}"
    new_aud=f"day_{day:02d}{audio.suffix}"
    shutil.copy(img,assets/'images'/new_img)
    shutil.copy(audio,assets/'audio'/new_aud)
    return{'image':f'assets/images/{new_img}','audio':f'assets/audio/{new_aud}','text':text,'title':folder,'date':f'{day}. Dezember'}

repo=Path("/Users/martinfischer/Documents/GitHub/adventkalender")
print("📚 Sammle Geschichten...")
stories={}
for day,name in STORY_ORDER.items():
    s=get_story(repo,name,day)
    if s:
        stories[str(day)]=s
        print(f"  Tag {day}: ✓")

print(f"\n✓ {len(stories)} Geschichten")

# Erstelle stories als JSON - SICHER!
stories_json = json.dumps(stories, ensure_ascii=False)

html = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Magischer Adventskalender 2026</title>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Crimson+Pro:wght@400;600&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root { --primary: #d4145a; --secondary: #fbb034; --gold: #ffd700; --dark: #1a1a2e; }
        body { font-family: 'Fredoka', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; overflow-x: hidden; }
        .snowflake { position: fixed; top: -10px; z-index: 1; color: rgba(255,255,255,0.8); font-size: 1.5em; animation: fall linear infinite; pointer-events: none; }
        @keyframes fall { to { transform: translateY(100vh); } }
        #welcome-screen { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); display: flex; justify-content: center; align-items: center; z-index: 1000; }
        #welcome-screen.hidden { display: none; }
        .welcome-content { text-align: center; color: white; padding: 2rem; }
        .welcome-title { font-size: clamp(2rem, 8vw, 5rem); font-weight: 700; margin-bottom: 1rem; text-shadow: 3px 3px 6px rgba(0,0,0,0.3); }
        .start-button { background: white; color: var(--primary); border: none; padding: 1.5rem 3rem; font-size: 1.5rem; font-weight: 700; border-radius: 50px; cursor: pointer; font-family: 'Fredoka', sans-serif; box-shadow: 0 10px 30px rgba(0,0,0,0.3); transition: transform 0.3s; }
        .start-button:hover { transform: scale(1.1); }
        .container { max-width: 1400px; margin: 0 auto; padding: 2rem; }
        header { text-align: center; color: white; margin-bottom: 3rem; }
        h1 { font-size: clamp(2rem, 6vw, 4rem); text-shadow: 3px 3px 6px rgba(0,0,0,0.3); }
        .calendar-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1.5rem; }
        .door { aspect-ratio: 1; cursor: pointer; border-radius: 20px; transition: transform 0.3s; }
        .door:hover { transform: scale(1.05); }
        .door-front { width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%); border: 4px solid white; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        .door.active .door-front { background: linear-gradient(135deg, var(--gold) 0%, var(--secondary) 100%); }
        .door-number { font-size: 3rem; font-weight: 700; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .door-icon { font-size: 2rem; margin-top: 0.5rem; }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 2000; }
        .modal.active { display: flex; justify-content: center; align-items: center; padding: 2rem; }
        .modal-content { background: white; border-radius: 30px; max-width: 900px; max-height: 90vh; overflow-y: auto; }
        .modal-header { padding: 2rem; background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%); color: white; border-radius: 30px 30px 0 0; position: relative; }
        .modal-header h2 { font-size: 2rem; margin-bottom: 0.5rem; }
        .close-button { position: absolute; top: 1rem; right: 1rem; background: white; color: var(--primary); border: none; width: 40px; height: 40px; border-radius: 50%; font-size: 1.5rem; cursor: pointer; font-weight: 700; transition: transform 0.3s; }
        .close-button:hover { transform: rotate(90deg) scale(1.1); }
        .modal-image { width: 100%; height: auto; }
        .modal-body { padding: 2rem; }
        .story-text { font-family: 'Crimson Pro', serif; font-size: 1.2rem; line-height: 1.8; white-space: pre-wrap; color: var(--dark); }
        .audio-player { margin: 2rem 0; text-align: center; }
        .play-button { background: var(--primary); color: white; border: none; width: 60px; height: 60px; border-radius: 50%; font-size: 1.5rem; cursor: pointer; transition: all 0.3s; }
        .play-button:hover { transform: scale(1.1); background: var(--secondary); }
        @media (max-width: 768px) { .calendar-grid { grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 1rem; } .door-number { font-size: 2rem; } }
    </style>
</head>
<body>
    <script>
        setInterval(() => {
            const s = document.createElement('div');
            s.classList.add('snowflake');
            s.textContent = '❄';
            s.style.left = Math.random() * 100 + '%';
            s.style.animationDuration = Math.random() * 3 + 2 + 's';
            document.body.appendChild(s);
            setTimeout(() => s.remove(), 5000);
        }, 300);
    </script>
    <div id="welcome-screen">
        <div class="welcome-content">
            <h1 class="welcome-title">🎄 Willkommen! 🎄</h1>
            <p style="font-size: 1.5rem; margin-bottom: 2rem;">Entdecke jeden Tag eine neue magische Geschichte</p>
            <button class="start-button" onclick="startAdvent()">Los geht's! ✨</button>
        </div>
    </div>
    <div class="container">
        <header><h1>🌟 Magischer Adventskalender 2026 🌟</h1><p style="font-size: 1.5rem; opacity: 0.9;">24 zauberhafte Geschichten für dich</p></header>
        <div class="calendar-grid" id="calendar-grid"></div>
    </div>
    <div id="story-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <button class="close-button" onclick="closeModal()">×</button>
                <h2 id="modal-title"></h2>
                <p id="modal-date"></p>
            </div>
            <img id="modal-image" class="modal-image" style="display:none;">
            <div class="modal-body">
                <div class="audio-player">
                    <button class="play-button" id="play-button" onclick="toggleAudio()">▶️</button>
                    <p style="font-size: 0.9rem; color: #666; margin-top: 1rem;">Klicke auf Play, um die Geschichte zu hören 🎧</p>
                    <audio id="story-audio" style="display:none;"></audio>
                </div>
                <div class="story-text" id="story-text"></div>
            </div>
        </div>
    </div>
    <script>
        const stories = """ + stories_json + """;
        let currentAudio = null;
        const icons = ['🧞','🎁','⭐','🎅','🔔','🕯️','❄️','⛄','🎄','🌟'];
        
        function startAdvent() {
            document.getElementById('welcome-screen').classList.add('hidden');
        }
        
        function generateDoors() {
            const grid = document.getElementById('calendar-grid');
            for (let day = 1; day <= 24; day++) {
                const door = document.createElement('div');
                door.className = 'door' + (stories[day] ? ' active' : '');
                if (stories[day]) door.onclick = () => openDoor(day);
                door.innerHTML = '<div class="door-front"><div class="door-number">' + day + '</div><div class="door-icon">' + icons[day % icons.length] + '</div></div>';
                grid.appendChild(door);
            }
        }
        
        function openDoor(day) {
            const story = stories[day];
            if (!story) return;
            document.getElementById('modal-title').textContent = story.title;
            document.getElementById('modal-date').textContent = story.date;
            document.getElementById('story-text').textContent = story.text;
            const img = document.getElementById('modal-image');
            img.onload = () => img.style.display = 'block';
            img.onerror = () => img.style.display = 'none';
            img.src = story.image;
            currentAudio = document.getElementById('story-audio');
            currentAudio.src = story.audio;
            document.getElementById('story-modal').classList.add('active');
            setTimeout(() => currentAudio.play().catch(() => {}), 800);
            currentAudio.onplay = () => document.getElementById('play-button').textContent = '⏸️';
            currentAudio.onpause = () => document.getElementById('play-button').textContent = '▶️';
        }
        
        function closeModal() {
            document.getElementById('story-modal').classList.remove('active');
            if (currentAudio) { currentAudio.pause(); currentAudio.currentTime = 0; document.getElementById('play-button').textContent = '▶️'; }
        }
        
        function toggleAudio() {
            if (!currentAudio) return;
            currentAudio.paused ? currentAudio.play() : currentAudio.pause();
        }
        
        document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });
        generateDoors();
    </script>
</body>
</html>"""

with open(repo / "index.html", 'w', encoding='utf-8') as f:
    f.write(html)

print("✓ index.html erstellt mit JSON (sicher!)")
print("\ngit add index.html")
print("git commit -m 'Fix mit JSON'")
print("git push")
