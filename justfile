# Build the site
docs:
    hugo

# Serve the site locally with live reload
docs-serve:
    hugo server -D

# Copy the latest resume PDF from the resume_2026 repo into static/
sync:
    python3 scripts/sync_resume.py

# Re-render the social share card from scripts/og-card.html (macOS Chrome)
og-card:
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
      --hide-scrollbars --force-device-scale-factor=1 --window-size=1200,630 \
      --screenshot=static/img/og-card.png "file://$(pwd)/scripts/og-card.html"

# Re-synthesise the DO NOT PRESS buzzer (two detuned square waves, 0.85s)
buzzer:
    ffmpeg -hide_banner -loglevel error -y \
      -f lavfi -i "aevalsrc=0.42*(2*gt(sin(2*PI*138*t)\,0)-1)+0.30*(2*gt(sin(2*PI*145*t)\,0)-1)+0.12*(2*gt(sin(2*PI*277*t)\,0)-1):d=0.85:s=44100:c=mono" \
      -af "afade=t=in:st=0:d=0.008,afade=t=out:st=0.70:d=0.15,alimiter=limit=0.85,aformat=channel_layouts=stereo" \
      -c:a libmp3lame -b:a 96k static/audio/buzzer.mp3
