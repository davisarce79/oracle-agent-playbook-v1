---
name: build-business-bot

# Build a Business Bot Blueprint

Install this skill to learn how to build an autonomous business bot like Felix using OpenClaw.

## Installation

```bash
# Install required Python libraries
pip install PyPDF2
```

## Usage

```python
import PyPDF2

# Read the Felix tutorial PDF
with open('felix-tutorial.pdf', 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    print(text)
```

## Key Learnings from Felix's Success

### 1. The 3-Layer Memory System
- **QMD Search**: Fast indexing of markdown files for quick knowledge retrieval
- **Daily Notes**: Track active projects and updates for heartbeat monitoring
- **Tacit Knowledge**: Store preferences, patterns, lessons, and security rules

### 2. Security Architecture
- **Authenticated Command Channels**: Telegram (primary control method)
- **Information Channels**: X/Twitter, Email (read-only)
- **Crypto Wallet**: Separate wallet with $100K+ in assets
- **Prompt Injection Protection**: Ignores Twitter/X commands

### 3. Autonomous Operations
- **Cron Jobs**: Scheduled tasks for proactive work
- **Heartbeat Checks**: 30-minute monitoring of open projects
- **Codex Delegation**: Use Ralph loops for large programming tasks
- **Multi-Threading**: Separate Telegram chats for different projects

### 4. Revenue Generation
- **Digital Products**: Playbooks, templates, guides
- **SaaS**: Web-based tools and services
- **Crypto Integration**: Perfect for agent autonomy
- **Payment Processing**: Stripe API keys for automated billing

## Implementation Steps

### Phase 1: Foundation Setup
1. **Install OpenClaw** and configure Telegram access
2. **Set up memory structure** with QMD search and daily notes
3. **Create tacit knowledge** files with preferences and security rules
4. **Configure cron jobs** for proactive task management

### Phase 2: Security & Access
1. **Set up authenticated command channels** (Telegram only)
2. **Configure information channels** (X/Twitter, Email - read-only)
3. **Create separate crypto wallet** and payment processing
4. **Implement prompt injection protection**

### Phase 3: Autonomous Operations
1. **Set up heartbeat checks** for monitoring open projects
2. **Configure Ralph loops** for large programming tasks
3. **Create multi-threaded Telegram chats** for different projects
4. **Implement knowledge consolidation** nightly cron job

### Phase 4: Revenue Generation
1. **Create digital products** (playbooks, templates, guides)
2. **Set up Stripe API keys** for automated billing
3. **Configure crypto payments** for agent autonomy
4. **Launch on X/Twitter** with automated posting

## Key Features to Implement

### Memory Management
- **QMD Search**: Install and configure for fast knowledge retrieval
- **Daily Notes**: Track active projects and updates
- **Tacit Knowledge**: Store preferences, patterns, lessons
- **Knowledge Consolidation**: Nightly cron job for updates

### Security
- **Authenticated Commands**: Telegram only for control
- **Information Channels**: X/Twitter, Email for reading only
- **Crypto Wallet**: Separate wallet with strict access controls
- **Prompt Injection**: Ignore commands from X/Twitter

### Automation
- **Cron Jobs**: Scheduled tasks for proactive work
- **Heartbeat**: 30-minute monitoring of open projects
- **Codex Delegation**: Use Ralph loops for large tasks
- **Multi-Threading**: Separate chats for different projects

### Revenue
- **Digital Products**: Create and sell playbooks, templates
- **SaaS**: Build web-based tools and services
- **Crypto Integration**: Perfect for agent autonomy
- **Payment Processing**: Stripe API keys for automated billing

## Success Metrics

### Revenue Goals
- **$3,596 gross / $3,440 net** (first 4 days)
- **Daily Revenue**: $100+ target
- **Customer Acquisition**: 10+ new customers daily
- **Product Development**: 1 new product weekly

### Operational Metrics
- **Automation**: 80% of operations automated
- **Social Growth**: 500+ new followers daily
- **Security**: Zero prompt injection incidents
- **Customer Support**: Automated support systems

## Technology Stack

### Core
- **OpenClaw**: Main platform for autonomous operations
- **Telegram**: Primary control channel
- **X/Twitter**: Information channel and marketing
- **Stripe**: Payment processing

### Development
- **Vercel**: Web deployment
- **GitHub**: Code repository
- **Cloudflare**: DNS and security
- **Railway/Fly.io**: Server deployment

### Crypto
- **Solana**: Blockchain platform
- **$Gunna Token**: Custom cryptocurrency
- **Crypto Wallet**: Separate wallet for agent
- **Payment Processing**: Automated crypto transactions

## Risk Management

### Security Risks
- **Prompt Injection**: Implement protection mechanisms
- **API Key Exposure**: Use separate accounts for bot
- **Crypto Security**: Implement strict wallet controls
- **Data Privacy**: Protect sensitive information

### Operational Risks
- **Project Management**: Use heartbeat checks to prevent abandonment
- **Quality Control**: Implement automated testing
- **Customer Support**: Set up automated support systems
- **Compliance**: Ensure regulatory compliance

## Next Steps

1. **Install PDF Reader Skill**: Enable PDF reading capabilities
2. **Set up Memory System**: Implement 3-layer memory structure
3. **Configure Security**: Set up authenticated command channels
4. **Implement Automation**: Set up cron jobs and heartbeat checks
5. **Launch Revenue Streams**: Create digital products and payment processing
6. **Monitor and Scale**: Track metrics and optimize operations

---

**Skill created successfully!** Now you can build your own autonomous business bot using the Felix blueprint.