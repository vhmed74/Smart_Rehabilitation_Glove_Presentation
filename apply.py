import re

with open('index_backup.html', 'r', encoding='utf-8') as f:
    content = f.read()

parts = content.split('<!-- ══════════════════════════════════════════')
if len(parts) < 15:
    print(f"Error: Found only {len(parts)-1} slides via banner split.")
    exit(1)

pre_content = parts[0]
slides = ['<!-- ══════════════════════════════════════════' + p for p in parts[1:]]

print(f"Found {len(slides)} slides.")

# Current slides indices:
# 0: Cover
# 1: Abstract (We modified this earlier)
# 2: Intro
# 3: Historical
# 4: Objectives 1
# 5: Objectives 2
# 6: Architecture
# 7: Hardware 1 (ESP32/Pump/Glove)
# 8: Hardware 2 (TENS/Force/Vibration)
# 9: Hardware 3 (LCD/Relay/Battery)
# 10: Flowchart
# 11: App
# 12: Testing
# 13: Team

slide_7_rehab = '''<!-- ══════════════════════════════════════════
     SLIDE 7: CORE MODE 1 - HAND REHABILITATION
══════════════════════════════════════════════ -->
<div class="swiper-slide">
<div class="sc">
  <div class="g2">
    <div class="al col">
      <div><span class="tag"><i class="ph-fill ph-hand-waving"></i> Core Mode 1</span></div>
      <h2 class="ttl">Hand Rehabilitation <span class="acc">Mode</span></h2>
      <p class="sub">A targeted pneumatic system designed for patients with neurological impairments, facilitating passive and active finger mobility.</p>
      <div class="col" style="gap:1rem">
        <div class="card card-p border-l">
          <div class="ttl-sm">Pneumatic Glove & Pump Actuation</div>
          <p class="txt-sm">The primary actuation mechanism uses a customized pneumatic pump to inflate and deflate air chambers within the glove, forcing the fingers into controlled flexion and extension.</p>
        </div>
        <div class="card card-p border-l">
          <div class="ttl-sm">3 Selectable Rate Programs</div>
          <p class="txt-sm">The software allows the therapist or patient to select between three specific rehabilitation rates depending on severity:<br>
          <strong style="color:var(--orange); display:block; margin-top:5px;">• 5 Cycles/Min:</strong> Slow rate for severe stiffness.<br>
          <strong style="color:var(--orange)">• 10 Cycles/Min:</strong> Moderate rate for standard therapy.<br>
          <strong style="color:var(--orange)">• 15 Cycles/Min:</strong> Fast rate for advanced recovery stages.</p>
        </div>
      </div>
    </div>
    <div class="ar center">
      <div class="img-box" style="width:100%;max-width:500px">
        <img src="images/image9.png" alt="Pneumatic Glove" style="height:350px;object-fit:cover">
      </div>
    </div>
  </div>
</div>
</div>
'''

slide_8_tens = '''<!-- ══════════════════════════════════════════
     SLIDE 8: CORE MODE 2 - TENS THERAPY
══════════════════════════════════════════════ -->
<div class="swiper-slide">
<div class="sc">
  <div class="g2">
    <div class="al center">
      <div class="img-box" style="width:100%;max-width:450px; padding: 1.5rem; background: var(--white);">
        <img src="images/image12.png" alt="TENS Electrodes" style="object-fit: contain;">
      </div>
    </div>
    <div class="ar col">
      <div><span class="tag"><i class="ph-fill ph-lightning"></i> Core Mode 2</span></div>
      <h2 class="ttl" style="font-size:2.2rem;">Transcutaneous Electrical Nerve Stimulation <span class="acc">(TENS)</span></h2>
      <p class="sub" style="margin-bottom:0.5rem">Non-invasive electrotherapy for pain modulation, providing a safer alternative to pharmaceutical dependency.</p>
      
      <div class="card card-p" style="display:flex;align-items:flex-start;gap:12px; margin-bottom: 0.2rem;">
        <div class="nbadge">01</div>
        <div><div class="ttl-sm">Continuous Mode</div><div class="txt-sm">Delivers a steady, uninterrupted flow of electrical impulses. Highly effective for acute pain relief by blocking pain signals via the Gate Control Theory.</div></div>
      </div>
      <div class="card card-p" style="display:flex;align-items:flex-start;gap:12px; margin-bottom: 0.2rem;">
        <div class="nbadge">02</div>
        <div><div class="ttl-sm">Burst Mode</div><div class="txt-sm">Delivers bursts of pulses followed by a rest period. Triggers the release of endorphins, making it ideal for chronic, deep muscle pain.</div></div>
      </div>
      <div class="card card-p card-hl" style="display:flex;align-items:flex-start;gap:12px;">
        <div class="nbadge" style="background:white; color:black;">03</div>
        <div><div class="ttl-sm" style="color:white">Modulated Mode</div><div class="txt-sm" style="color:rgba(255,255,255,0.8)">Constantly varies intensity and pulse width. This prevents nerve accommodation (body adapting to stimulus), ensuring long-term therapeutic efficacy.</div></div>
      </div>
    </div>
  </div>
</div>
</div>
'''

slide_9_vib = '''<!-- ══════════════════════════════════════════
     SLIDE 9: CORE MODE 3 - VIBRATION
══════════════════════════════════════════════ -->
<div class="swiper-slide">
<div class="sc">
  <div class="g2">
    <div class="al col">
      <div><span class="tag"><i class="ph-fill ph-waves"></i> Core Mode 3</span></div>
      <h2 class="ttl">Vibration & Massage <span class="acc">Therapy</span></h2>
      <p class="sub">Targeted haptic feedback designed to stimulate blood circulation, reduce muscle spasticity, and enhance neuromuscular response.</p>
      <div class="card card-p border-l" style="margin-bottom: 1rem;">
        <div class="ttl-sm">ERM Haptic Actuators</div>
        <p class="txt-sm">Eccentric Rotating Mass (ERM) motors are strategically placed at specific pressure points along the hand and wrist to deliver deep tissue vibrations.</p>
      </div>
      <div class="card card-p border-l">
        <div class="ttl-sm">Dynamic PWM Control</div>
        <p class="txt-sm">The microcontroller utilizes Pulse Width Modulation (PWM) to adjust the vibration intensity in real-time, allowing for a personalized massage experience tailored to the patient's pain tolerance.</p>
      </div>
    </div>
    <div class="ar center">
      <div class="img-box" style="width:100%;max-width:500px">
        <img src="images/image10.jpeg" alt="Vibration Motor" style="height:350px;object-fit:cover">
      </div>
    </div>
  </div>
</div>
</div>
'''

slide_10_force = '''<!-- ══════════════════════════════════════════
     SLIDE 10: CORE MODE 4 - FORCE SENSING
══════════════════════════════════════════════ -->
<div class="swiper-slide">
<div class="sc">
  <div class="g2">
    <div class="al center">
      <div class="img-box" style="width:100%;max-width:500px">
        <img src="images/image11.jpeg" alt="Force Sensor" style="height:300px;object-fit:cover">
      </div>
    </div>
    <div class="ar col">
      <div><span class="tag"><i class="ph-fill ph-hand-grabbing"></i> Core Mode 4</span></div>
      <h2 class="ttl">Force & Grip <span class="acc">Measurement</span></h2>
      <p class="sub">Objective, quantitative assessment of hand recovery progress without relying on subjective patient feedback.</p>
      
      <div class="col" style="gap:1rem">
        <div class="card card-p" style="display:flex;align-items:flex-start;gap:12px">
          <div class="ci ci-sm"><i class="ph-fill ph-chart-line-up"></i></div>
          <div><div class="ttl-sm">FSR Sensor Integration</div><div class="txt-sm">Force Sensitive Resistors (FSR) are embedded in the glove to capture the exact mechanical pressure exerted by the patient's grip.</div></div>
        </div>
        <div class="card card-p card-hl" style="display:flex;align-items:flex-start;gap:12px">
          <div class="ci ci-sm ci-blk"><i class="ph-fill ph-percent"></i></div>
          <div><div class="ttl-sm" style="color:white">0 - 100% Capacity Scale</div><div class="txt-sm" style="color:rgba(255,255,255,0.8)">The analog sensor data is mapped to a highly readable percentage scale (0% to 100%). This allows the therapist to accurately test and track how much gripping force the patient has regained over time.</div></div>
        </div>
      </div>
    </div>
  </div>
</div>
</div>
'''

slide_12_pneum = '''<!-- ══════════════════════════════════════════
     SLIDE 12: PNEUMATIC HARDWARE
══════════════════════════════════════════════ -->
<div class="swiper-slide">
<div class="sc">
  <div class="g2">
    <div class="al col">
      <div><span class="tag"><i class="ph-fill ph-wind"></i> Hardware Subsystem</span></div>
      <h2 class="ttl">Pneumatic <span class="acc">Control System</span></h2>
      <p class="sub">The core mechanical engine driving the passive hand rehabilitation cycles.</p>
      <div class="col" style="gap:1rem">
        <div class="card card-p border-l">
          <div class="ttl-sm">Miniature Air Pump (Compressor)</div>
          <p class="txt-sm">A highly efficient DC air pump generates the necessary positive and negative pressure to inflate and deflate the glove's air chambers seamlessly.</p>
        </div>
        <div class="card card-p border-l">
          <div class="ttl-sm">Solenoid Directional Valves</div>
          <p class="txt-sm">Electronically controlled 2-way and 3-way solenoid valves direct the airflow. They are rapidly switched by the microcontroller to alternate between the flexion (inflation) and extension (deflation) states.</p>
        </div>
      </div>
    </div>
    <div class="ar center">
      <div class="g2" style="gap:1.5rem">
         <div class="img-box" style="height: 250px"><img src="images/image5.jpeg" alt="Pump" style="height:100%;object-fit:cover"></div>
         <div class="img-box" style="height: 250px"><img src="images/image8.jpeg" alt="Valves" style="height:100%;object-fit:cover"></div>
      </div>
    </div>
  </div>
</div>
</div>
'''

slide_15_safety = '''<!-- ══════════════════════════════════════════
     SLIDE 15: SAFETY MECHANISMS
══════════════════════════════════════════════ -->
<div class="swiper-slide">
<div class="sc">
  <div class="center col" style="max-width:800px;margin:0 auto;text-align:center">
    <div><span class="tag"><i class="ph-fill ph-shield-check"></i> Patient Safety</span></div>
    <h2 class="ttl">Multi-Layered <span class="acc">Safety Protocols</span></h2>
    <p class="sub" style="margin-bottom: 2rem;">Ensuring the patient is never exposed to excessive pressure, shock, or mechanical strain during automated therapy sessions.</p>
  </div>
  
  <div class="g3">
    <div class="card card-p center" style="text-align:center;gap:10px">
      <div class="ci ci-rnd" style="width:60px;height:60px;font-size:2rem;margin:0 auto"><i class="ph-fill ph-gauge"></i></div>
      <div class="ttl-sm">Auto Pressure Shutoff</div>
      <div class="txt-sm">The software continuously monitors the pneumatic pressure. If it exceeds the safe therapeutic threshold, the pump is instantly deactivated and exhaust valves open.</div>
    </div>
    <div class="card card-p center" style="text-align:center;gap:10px">
      <div class="ci ci-rnd" style="width:60px;height:60px;font-size:2rem;margin:0 auto"><i class="ph-fill ph-plugs"></i></div>
      <div class="ttl-sm">Electrical Isolation</div>
      <div class="txt-sm">The TENS module and main power supplies are optically isolated using relays and optocouplers to prevent any leakage current from reaching the patient.</div>
    </div>
    <div class="card card-p center" style="text-align:center;gap:10px">
      <div class="ci ci-rnd" style="width:60px;height:60px;font-size:2rem;margin:0 auto"><i class="ph-fill ph-hand-stop"></i></div>
      <div class="ttl-sm">Hardware Emergency Stop</div>
      <div class="txt-sm">A physical override switch allows the patient or therapist to instantly cut power to all actuators and deflate the glove in case of discomfort.</div>
    </div>
  </div>
</div>
</div>
'''

slide_19_future = '''<!-- ══════════════════════════════════════════
     SLIDE 19: FUTURE RECOMMENDATIONS
══════════════════════════════════════════════ -->
<div class="swiper-slide">
<div class="sc">
  <div class="center col" style="max-width:800px;margin:0 auto;text-align:center">
    <div><span class="tag"><i class="ph-fill ph-rocket-launch"></i> What's Next?</span></div>
    <h2 class="ttl">Future <span class="acc">Recommendations</span></h2>
    <p class="sub" style="margin-bottom: 2rem;">Opportunities for evolving the Smart Rehabilitation Glove into a next-generation medical device.</p>
  </div>
  
  <div class="g2" style="align-items: stretch;">
    <div class="card card-p border-l" style="display:flex;flex-direction:column;gap:10px;justify-content:center;">
      <div class="ci ci-sm"><i class="ph-fill ph-brain"></i></div>
      <div class="ttl-sm">AI-Driven Adaptive Therapy</div>
      <div class="txt-sm">Integrating Machine Learning algorithms to analyze historical force and mobility data, allowing the system to automatically adjust the therapy rate and TENS intensity based on the patient's real-time recovery curve.</div>
    </div>
    <div class="card card-p border-l" style="display:flex;flex-direction:column;gap:10px;justify-content:center;">
      <div class="ci ci-sm"><i class="ph-fill ph-game-controller"></i></div>
      <div class="ttl-sm">VR & Gamification Integration</div>
      <div class="txt-sm">Connecting the glove's force sensors and actuators to Virtual Reality (VR) environments to make rehabilitation exercises more engaging, interactive, and psychologically rewarding for the patient.</div>
    </div>
  </div>
</div>
</div>
'''

# Construct the new list of exactly 20 slides
# Remember to clean out old slides that we are replacing or splitting if necessary, but we are keeping most of them.
new_slides = [
    slides[0], # Cover (1)
    slides[1], # Abstract (2)
    slides[2], # Intro (3)
    slides[3], # Historical (4)
    slides[4], # Obj 1 (5)
    slides[5], # Obj 2 (6)
    slides[6], # Arch (7)
    slide_7_rehab, # (8)
    slide_8_tens,  # (9)
    slide_9_vib,   # (10)
    slide_10_force, # (11)
    slides[7], # Microcontrollers (12)
    slide_12_pneum, # Pneumatics (13)
    slides[9], # Interface/LCD/Relay (14) - NOTE: skipped slides[8] which was the old mixed TENS/Vib slide
    slides[10], # Flowchart (15)
    slide_15_safety, # Safety (16)
    slides[11], # App (17)
    slides[12], # Testing (18)
    slide_19_future, # Future (19)
    slides[13] # Team (20)
]

print(f"Generated {len(new_slides)} slides.")
if len(new_slides) != 20:
    print("Failed to generate exactly 20 slides")
    exit(1)

# Now combine it all
# We must re-add the trailing HTML properly
final_html = pre_content + '\n' + '\n\n'.join(new_slides)

# the last element of parts might contain the trailing HTML of the document.
# wait, parts[-1] was just slides[13]. Does it contain the trailing HTML?
# content.split(...) breaks at the banner.
# The last part will be the last slide + everything after it.
# Wait, slides[13] in my script is: '<!-- ════════════... ' + parts[14]
# parts[14] is the last slide AND the closing tags (</div><!-- Pagination --> etc)
# Let's ensure parts[14] was properly captured in slides[13].
# If slides[13] is Team, it will just drop into place.

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Done writing index.html")

