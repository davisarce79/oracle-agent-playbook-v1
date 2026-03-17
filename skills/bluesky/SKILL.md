---
name: bluesky
description: "Interact with Bluesky using the @atproto/api library. Use for posting skeets, reading timelines, and managing followers."
---

# Bluesky Skill

Use the `@atproto/api` library to interact with Bluesky, a decentralized social network similar to Twitter.

## Setup

1. Install the `@atproto/api` package:
   ```bash
   npm install -g @atproto/api
   ```

2. Get your API credentials from Bluesky:
   - Create an account at https://bsky.app
   - Go to Settings → Developer → Create App
   - Set permissions: read/write
   - Copy the App Key

3. Store credentials as environment variables:
   ```bash
   export BLUESKY_APP_KEY="your_app_key"
   export BLUESKY_USERNAME="your@username"
   export BLUESKY_PASSWORD="your_password"
   ```

## Usage

### Post a Skeet (Bluesky Post)
```bash
node -e "
const { Bsky } = require('@atproto/api');
const bsky = new Bsky();

(async () => {
  try {
    await bsky.login({
      app: process.env.BLUESKY_APP_KEY,
      username: process.env.BLUESKY_USERNAME,
      password: process.env.BLUESKY_PASSWORD
    });
    
    const skeet = await bsky.createPost({
      text: 'Agent Gunna reporting in! Bluesky operational, Project Seed live, and trading strategies active. #AI #Trading #AutonomousAgents'
    });
    console.log('Skeet posted:', skeet.data.uri);
  } catch (error) {
    console.error('Error posting skeet:', error.message);
  }
})();
"
```

### Read Home Timeline
```bash
node -e "
const { Bsky } = require('@atproto/api');
const bsky = new Bsky();

(async () => {
  try {
    await bsky.login({
      app: process.env.BLUESKY_APP_KEY,
      username: process.env.BLUESKY_USERNAME,
      password: process.env.BLUESKY_PASSWORD
    });
    
    const timeline = await bsky.getHomeFeed();
    console.log('Home timeline:', timeline.data);
  } catch (error) {
    console.error('Error getting timeline:', error.message);
  }
})();
"
```

### Follow a User
```bash
node -e "
const { Bsky } = require('@atproto/api');
const bsky = new Bsky();

(async () => {
  try {
    await bsky.login({
      app: process.env.BLUESKY_APP_KEY,
      username: process.env.BLUESKY_USERNAME,
      password: process.env.BLUESKY_PASSWORD
    });
    
    const follow = await bsky.follow('username');
    console.log('Followed:', follow.data);
  } catch (error) {
    console.error('Error following user:', error.message);
  }
})();
"
```

## Common Operations

### Post with Media
```bash
node -e "
const fs = require('fs');
const { Bsky } = require('@atproto/api');
const bsky = new Bsky();

(async () => {
  try {
    await bsky.login({
      app: process.env.BLUESKY_APP_KEY,
      username: process.env.BLUESKY_USERNAME,
      password: process.env.BLUESKY_PASSWORD
    });
    
    const media = fs.readFileSync('path/to/image.jpg');
    const uploaded = await bsky.uploadMedia({
      file: media,
      filename: 'image.jpg'
    });
    
    const skeet = await bsky.createPost({
      text: 'Check this out!',
      attachments: [uploaded.data]
    });
    console.log('Skeet with media posted:', skeet.data.uri);
  } catch (error) {
    console.error('Error posting skeet with media:', error.message);
  }
})();
"
```

### Reply to a Skeet
```bash
node -e "
const { Bsky } = require('@atproto/api');
const bsky = new Bsky();

(async () => {
  try {
    await bsky.login({
      app: process.env.BLUESKY_APP_KEY,
      username: process.env.BLUESKY_USERNAME,
      password: process.env.BLUESKY_PASSWORD
    });
    
    const reply = await bsky.createPost({
      text: 'Your reply text here',
      replyTo: 'skeet_uri_to_reply_to'
    });
    console.log('Reply posted:', reply.data.uri);
  } catch (error) {
    console.error('Error posting reply:', error.message);
  }
})();
"
```

## Notes

- Bluesky is a newer platform but growing quickly
- API is currently in beta but free to use
- Uses a decentralized protocol called ATProto
- Similar interface to Twitter but with more modern features