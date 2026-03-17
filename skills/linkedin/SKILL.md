---
name: linkedin
description: "Interact with LinkedIn using the linkedin-api library. Use for posting updates, reading feeds, and managing connections."
---

# LinkedIn Skill

Use the `linkedin-api` library to interact with LinkedIn. LinkedIn allows professional networking and content sharing.

## Setup

1. Install the `linkedin-api` package:
   ```bash
   npm install -g linkedin-api
   ```

2. Get your LinkedIn credentials:
   - LinkedIn email and password
   - Or use OAuth if available

3. Store credentials as environment variables:
   ```bash
   export LINKEDIN_EMAIL="your_email@example.com"
   export LINKEDIN_PASSWORD="your_password"
   ```

## Usage

### Post an Update
```bash
node -e "
const LinkedIn = require('linkedin-api');
const linkedin = new LinkedIn({
  email: process.env.LINKEDIN_EMAIL,
  password: process.env.LINKEDIN_PASSWORD
});

(async () => {
  try {
    await linkedin.login();
    const post = await linkedin.postUpdate({
      text: 'Agent Gunna reporting in! LinkedIn operational, Project Seed live, and trading strategies active. #AI #Trading #AutonomousAgents'
    });
    console.log('Post created:', post);
  } catch (error) {
    console.error('Error posting update:', error.message);
  }
})();
"
```

### Read Feed
```bash
node -e "
const LinkedIn = require('linkedin-api');
const linkedin = new LinkedIn({
  email: process.env.LINKEDIN_EMAIL,
  password: process.env.LINKEDIN_PASSWORD
});

(async () => {
  try {
    await linkedin.login();
    const feed = await linkedin.getFeed();
    console.log('Feed:', feed);
  } catch (error) {
    console.error('Error getting feed:', error.message);
  }
})();
"
```

### Connect with User
```bash
node -e "
const LinkedIn = require('linkedin-api');
const linkedin = new LinkedIn({
  email: process.env.LINKEDIN_EMAIL,
  password: process.env.LINKEDIN_PASSWORD
});

(async () => {
  try {
    await linkedin.login();
    const connect = await linkedin.connect('user_id_or_url');
    console.log('Connection sent:', connect);
  } catch (error) {
    console.error('Error connecting:', error.message);
  }
})();
"
```

## Common Operations

### Post with Media
```bash
node -e "
const fs = require('fs');
const LinkedIn = require('linkedin-api');
const linkedin = new LinkedIn({
  email: process.env.LINKEDIN_EMAIL,
  password: process.env.LINKEDIN_PASSWORD
});

(async () => {
  try {
    await linkedin.login();
    
    const media = fs.readFileSync('path/to/image.jpg');
    const post = await linkedin.postUpdate({
      text: 'Check this out!',
      media: media
    });
    console.log('Post created:', post);
  } catch (error) {
    console.error('Error posting update:', error.message);
  }
})();
"
```

### Comment on Post
```bash
node -e "
const LinkedIn = require('linkedin-api');
const linkedin = new LinkedIn({
  email: process.env.LINKEDIN_EMAIL,
  password: process.env.LINKEDIN_PASSWORD
});

(async () => {
  try {
    await linkedin.login();
    const comment = await linkedin.commentOnPost('post_id', 'Your comment here');
    console.log('Comment posted:', comment);
  } catch (error) {
    console.error('Error commenting:', error.message);
  }
})();
"
```

## Notes

- LinkedIn has strict rate limits and anti-bot measures
- Use responsibly and avoid spamming
- Professional content works best
- Consider using LinkedIn's official API for production use