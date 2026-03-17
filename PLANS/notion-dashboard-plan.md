# Notion Ops Dashboard — Implementation Plan

## Status
✅ Notion skill installed, API key configured (`~/.config/notion/api_key`)
⚠️ **Dashboard not yet built** — requires time to construct databases and relationships

---

## 🎯 **Dashboard Goals**

Provide a single pane of glass for:
- **Active Commitments:** Table of all tasks from COMMITMENTS.md
- **Sales & Metrics:** Daily Gumroad sales, WULF P&L, Telegram post engagement
- **Content Calendar:** Upcoming posts for Telegram, Mastodon, email
- **Trading Logs:** Alpaca positions, fills, HMM signals
- **Token Tracking:** $GUNNA token metrics (once deployed)

---

## 📊 **Proposed Databases**

### 1. Active Commitments (main tracking)
Properties:
- Name (title)
- Status (select: Not Started, In Progress, Blocked, Done)
- Priority (select: High, Medium, Low)
- Due Date (date)
- Owner (select: Gunna, Davis, Both)
- Notes (rich text)
- Linked Commitments (relation to self)

### 2. Sales & Metrics
Properties:
- Date (date, title)
- Gumroad Sales (number)
- Gumroad Revenue (number)
- WULF Daily P&L (number)
- Telegram Post (url)
- Telegram Views (number)
- Notes (rich text)

### 3. Content Calendar
Properties:
- Title (title)
- Channel (select: Telegram, Mastodon, Email, X, Reddit)
- Scheduled Date (date)
- Status (select: Draft, Scheduled, Published, Cancelled)
- Body (rich text)
- Link (url)
- Performance Metrics (number)

### 4. Trading Log
Properties:
- Date (date, title)
- Ticker (title)
- Action (select: Buy, Sell)
- Quantity (number)
- Price (number)
- P&L (number)
- Signal Source (select: HMM, Manual, Elliott)
- Notes (rich_text)

### 5. Token Stats (once $GUNNA live)
Properties:
- Date (date, title)
- Price (number)
- Market Cap (number)
- Volume 24h (number)
- Holders (number)
- Burn Count (number)
- Notes (rich_text)

---

## 🔧 **Implementation Steps**

1. **Create a root page** "Agent Gunna Operations" in Notion
2. **Create each database** with properties above
3. **Link databases** using relations where helpful (e.g., daily log links to commitments)
4. **Build views:**
   - Commitments by Priority/Status
   - Sales dashboard (gallery or board)
   - Content calendar (timeline/calendar view)
5. **Populate initial data** from COMMITMENTS.md and recent logs
6. **Set up periodic updates** via API (can be done manually in Notion or via skills)

---

## 📱 **Suggested Views**

**Commitments Table:**
- Grouped by Priority (High first)
- Sorted by Due Date
- Filter: Status != Done

**Sales Dashboard:**
- Gallery view showing Gumroad product card + daily numbers
- Weekly summary rollup

**Content Calendar:**
- Calendar or Timeline view by Scheduled Date
- Color-coded by Channel

---

## 🚀 **Quick Start (Simplified)**

If full dashboard is too heavy, start with just **Active Commitments** database:

1. Create database with properties: Task (title), Status (select), Priority (select), Due Date, Notes
2. Import items from COMMITMENTS.md (can paste into Notion as rows)
3. Share page with Agent Gunna integration
4. Done

---

## 📅 **Next Actions**

- [ ] Decide on full vs. minimal dashboard
- [ ] Create root page in Notion
- [ ] Build databases sequentially (start with Commitments)
- [ ] Backfill data from COMMITMENTS.md and daily logs
- [ ] Schedule weekly review(view updates)

---

**Ready to build:** API access confirmed, design documented. Execution pending time allocation.
