# Instagram Bot – Realistic Automation Study

**Author:** KimikDark  
**Language:** Python + Playwright (Firefox)  
**Goal:** Simulate human-like Instagram interactions (likes + positive comments) on plant hashtags, compare bot vs human behavior.

---

## Features

- Persistent Firefox profile (manual login once → auto after)
- Human-like delays: **5–15 min between actions** 
- Max **15 interactions/day** → safe & undetectable
- Random likes (70%) + comments (60%)
- Anti-detection: real user-agent, scrolling, no pop-ups

---

## Setup

**Bash**
   - pip install playwright
   - playwright install firefox

**Run**

    - python main.py

## First time:

Firefox opens → log in manually
Reject cookies → "Reject all"
Click "Not now" on pop-ups
Press ENTER in terminal when on feed

**Next runs:**

Already logged in → starts automatically
