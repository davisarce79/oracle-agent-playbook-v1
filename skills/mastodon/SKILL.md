---
name: mastodon
description: "Interact with Mastodon instances using the mastodon-api library. Use for posting toots, reading timelines, and managing followers."
---

# Mastodon Skill

Use the `mastodon-api` library to interact with Mastodon instances. Mastodon is a decentralized social network with many free instances.

## Setup

1. Install the `mastodon-api` package:
   ```bash
   npm install -g mastodon-api
   ```

2. Get your API credentials from your Mastodon instance:
   - Go to your instance's website (e.g., mastodon.social, fosstodon.org)
   - Settings → Development → New Application
   - Set permissions: read/write
   - Copy the Client ID, Client Secret, and Access Token

3. Store credentials as environment variables:
   ```bash
   export MASTODON_INSTANCE="your.instance.url"
   export MASTODON_CLIENT_ID="your_client_id"
   export MASTODON_CLIENT_SECRET="your_client_secret"
   export MASTODON_ACCESS_TOKEN="your_access_token"
   ```

## Usage

### Post a Toot (Mastodon Post)
```bash
node -e "
const Mastodon = require('mastodon-api');
const M = new Mastodon({
  client_id: process.env.MASTODON_CLIENT_ID,
  client_secret: process.env.MASTODON_CLIENT_SECRET,
  access_token: process.env.MASTODON_ACCESS_TOKEN,
  api_url: 'https://' + process.env.MASTODON_INSTANCE
});

(async () => {
  try {
    const toot = await M.post('statuses', {
      status: 'Agent Gunna reporting in! Mastodon operational, Project Seed live, and trading strategies active. #AI #Trading #AutonomousAgents'
    });
    console.log('Toot posted:', toot.data.id);
  } catch (error) {
    console.error('Error posting toot:', error.message);
  }
})();
"
```

### Read Home Timeline
```bash
node -e "
const Mastodon = require('mastodon-api');
const M = new Mastodon({
  client_id: process.env.MASTODON_CLIENT_ID,
  client_secret: process.env.MASTODON_CLIENT_SECRET,
  access_token: process.env.MASTODON_ACCESS_TOKEN,
  api_url: 'https://' + process.env.MASTODON_INSTANCE
});

(async () => {
  try {
    const timeline = await M.get('timelines/home', { limit: 20 });
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
const Mastodon = require('mastodon-api');
const M = new Mastodon({
  client_id: process.env.MASTODON_CLIENT_ID,
  client_secret: process.env.MASTODON_CLIENT_SECRET,
  access_token: process.env.MASTODON_ACCESS_TOKEN,
  api_url: 'https://' + process.env.MASTODON_INSTANCE
});

(async () => {
  try {
    const follow = await M.post('follows', {
      uri: 'username@instance.url'
    });
    console.log('Followed:', follow.data.id);
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
const Mastodon = require('mastodon-api');
const M = new Mastodon({
  client_id: process.env.MASTODON_CLIENT_ID,
  client_secret: process.env.MASTODON_CLIENT_SECRET,
  access_token: process.env.MASTODON_ACCESS_TOKEN,
  api_url: 'https://' + process.env.MASTODON_INSTANCE
});

(async () => {
  try {
    const media = fs.readFileSync('path/to/image.jpg');
    const uploaded = await M.post('media', {
      file: media,
      description: 'Image description'
    });
    
    const toot = await M.post('statuses', {
      status: 'Check this out!',
      media_ids: [uploaded.data.id]
    });
    console.log('Toot with media posted:', toot.data.id);
  } catch (error) {
    console.error('Error posting toot with media:', error.message);
  }
})();
"
```

### Reply to a Toot
```bash
node -e "
const Mastodon = require('mastodon-api');
const M = new Mastodon({
  client_id: process.env.MASTODON_CLIENT_ID,
  client_secret: process.env.MASTODON_CLIENT_SECRET,
  access_token: process.env.MASTODON_ACCESS_TOKEN,
  api_url: 'https://' + process.env.MASTODON_INSTANCE
});

(async () => {
  try {
    const reply = await M.post('statuses', {
      status: 'Your reply text here',
      in_reply_to_id: 'toot_id_to_reply_to'
    });
    console.log('Reply posted:', reply.data.id);
  } catch (error) {
    console.error('Error posting reply:', error.message);
  }
})();
"
```

## Notes

- Mastodon is decentralized - you can choose from many free instances
- Popular instances include: mastodon.social, fosstodon.org, mastodon.online
- Most instances are free to join and use
- API rate limits are generous compared to Twitter
- Content warnings are supported for sensitive content