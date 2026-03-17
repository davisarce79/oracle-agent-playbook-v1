---
name: social-post
description: "Post to multiple social platforms (Mastodon, Bluesky, LinkedIn, Reddit) using the respective API libraries. Use when you want to broadcast the same message across different platforms."
---

# Social Post Skill

This skill coordinates posting the same message across multiple social platforms (Mastodon, Bluesky, LinkedIn, Reddit) using their respective API libraries.

## Setup

Ensure you have all the required API credentials set as environment variables:

### Mastodon
```bash
export MASTODON_INSTANCE="your.instance.url"
export MASTODON_CLIENT_ID="your_client_id"
export MASTODON_CLIENT_SECRET="your_client_secret"
export MASTODON_ACCESS_TOKEN="your_access_token"
```

### Bluesky
```bash
export BLUESKY_APP_KEY="your_app_key"
export BLUESKY_USERNAME="your@username"
export BLUESKY_PASSWORD="your_password"
```

### LinkedIn
```bash
export LINKEDIN_EMAIL="your_email@example.com"
export LINKEDIN_PASSWORD="your_password"
```

### Reddit
```bash
export REDDIT_USERNAME="your_username"
export REDDIT_PASSWORD="your_password"
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
```

## Usage

### Post to All Platforms
```bash
node -e "
const { exec } = require('child_process');

const message = 'Agent Gunna reporting in! Social platforms operational, Project Seed live, and trading strategies active. #AI #Trading #AutonomousAgents';

// Post to Mastodon
exec(`node -e \"const Mastodon = require('mastodon-api');\nconst M = new Mastodon({\n  client_id: process.env.MASTODON_CLIENT_ID,\n  client_secret: process.env.MASTODON_CLIENT_SECRET,\n  access_token: process.env.MASTODON_ACCESS_TOKEN,\n  api_url: 'https://' + process.env.MASTODON_INSTANCE\n});\n\n(async () => {\n  try {\n    const toot = await M.post('statuses', {\n      status: '${message}'\n    });\n    console.log('Toot posted:', toot.data.id);\n  } catch (error) {\n    console.error('Error posting toot:', error.message);\n  }\n})();\"`, (error, stdout, stderr) => {\n  if (error) console.error('Mastodon error:', error);\n  else console.log('Mastodon stdout:', stdout);\n});\n\n// Post to Bluesky
exec(`node -e \"const { Bsky } = require('@atproto/api');\nconst bsky = new Bsky();\n\n(async () => {\n  try {\n    await bsky.login({\n      app: process.env.BLUESKY_APP_KEY,\n      username: process.env.BLUESKY_USERNAME,\n      password: process.env.BLUESKY_PASSWORD\n    });\n    \n    const skeet = await bsky.createPost({\n      text: '${message}'\n    });\n    console.log('Skeet posted:', skeet.data.uri);\n  } catch (error) {\n    console.error('Error posting skeet:', error.message);\n  }\n})();\"`, (error, stdout, stderr) => {\n  if (error) console.error('Bluesky error:', error);\n  else console.log('Bluesky stdout:', stdout);\n});\n\n// Post to LinkedIn
exec(`node -e \"const LinkedIn = require('linkedin-api');\nconst linkedin = new LinkedIn({\n  email: process.env.LINKEDIN_EMAIL,\n  password: process.env.LINKEDIN_PASSWORD\n});\n\n(async () => {\n  try {\n    await linkedin.login();\n    const post = await linkedin.postUpdate({\n      text: '${message}'\n    });\n    console.log('Post created:', post);\n  } catch (error) {\n    console.error('Error posting update:', error.message);\n  }\n})();\"`, (error, stdout, stderr) => {\n  if (error) console.error('LinkedIn error:', error);\n  else console.log('LinkedIn stdout:', stdout);\n});\n\n// Post to Reddit
exec(`node -e \"const Reddit = require('reddit-simple');\n\n(async () => {\n  try {\n    const login = await Reddit.Authenticate({\n      username: process.env.REDDIT_USERNAME,\n      password: process.env.REDDIT_PASSWORD,\n      clientId: process.env.REDDIT_CLIENT_ID,\n      clientSecret: process.env.REDDIT_CLIENT_SECRET\n    });\n    \n    const post = await Reddit.SubmitPost({\n      title: 'Agent Gunna reporting in!',\n      text: '${message}',\n      subreddit: 'your_subreddit',\n      type: 'text'\n    });\n    console.log('Post created:', post);\n  } catch (error) {\n    console.error('Error posting:', error.message);\n  }\n})();\"`, (error, stdout, stderr) => {\n  if (error) console.error('Reddit error:', error);\n  else console.log('Reddit stdout:', stdout);\n});\n"
```

## Common Operations

### Post to Selected Platforms
```bash
node -e "
const { exec } = require('child_process');

const message = 'Agent Gunna reporting in! Social platforms operational, Project Seed live, and trading strategies active. #AI #Trading #AutonomousAgents';
const platforms = ['mastodon', 'bluesky']; // Select which platforms to post to

platforms.forEach(platform => {
  let command;
  
  switch(platform) {
    case 'mastodon':
      command = `node -e \"const Mastodon = require('mastodon-api');\nconst M = new Mastodon({\n  client_id: process.env.MASTODON_CLIENT_ID,\n  client_secret: process.env.MASTODON_CLIENT_SECRET,\n  access_token: process.env.MASTODON_ACCESS_TOKEN,\n  api_url: 'https://' + process.env.MASTODON_INSTANCE\n});\n\n(async () => {\n  try {\n    const toot = await M.post('statuses', {\n      status: '${message}'\n    });\n    console.log('Toot posted:', toot.data.id);\n  } catch (error) {\n    console.error('Error posting toot:', error.message);\n  }\n})();\"`;
      break;
      
    case 'bluesky':
      command = `node -e \"const { Bsky } = require('@atproto/api');\nconst bsky = new Bsky();\n\n(async () => {\n  try {\n    await bsky.login({\n      app: process.env.BLUESKY_APP_KEY,\n      username: process.env.BLUESKY_USERNAME,\n      password: process.env.BLUESKY_PASSWORD\n    });\n    \n    const skeet = await bsky.createPost({\n      text: '${message}'\n    });\n    console.log('Skeet posted:', skeet.data.uri);\n  } catch (error) {\n    console.error('Error posting skeet:', error.message);\n  }\n})();\"`;
      break;
      
    case 'linkedin':
      command = `node -e \"const LinkedIn = require('linkedin-api');\nconst linkedin = new LinkedIn({\n  email: process.env.LINKEDIN_EMAIL,\n  password: process.env.LINKEDIN_PASSWORD\n});\n\n(async () => {\n  try {\n    await linkedin.login();\n    const post = await linkedin.postUpdate({\n      text: '${message}'\n    });\n    console.log('Post created:', post);\n  } catch (error) {\n    console.error('Error posting update:', error.message);\n  }\n})();\"`;
      break;
      
    case 'reddit':
      command = `node -e \"const Reddit = require('reddit-simple');\n\n(async () => {\n  try {\n    const login = await Reddit.Authenticate({\n      username: process.env.REDDIT_USERNAME,\n      password: process.env.REDDIT_PASSWORD,\n      clientId: process.env.REDDIT_CLIENT_ID,\n      clientSecret: process.env.REDDIT_CLIENT_SECRET\n    });\n    \n    const post = await Reddit.SubmitPost({\n      title: 'Agent Gunna reporting in!',\n      text: '${message}',\n      subreddit: 'your_subreddit',\n      type: 'text'\n    });\n    console.log('Post created:', post);\n  } catch (error) {\n    console.error('Error posting:', error.message);\n  }\n})();\"`;
      break;
  }
  
  exec(command, (error, stdout, stderr) => {
    if (error) console.error(`${platform} error:`, error);
    else console.log(`${platform} stdout:`, stdout);
  });
});
"
```

## Notes

- Each platform has different content guidelines and audience expectations
- Customize messages for each platform's culture
- Be mindful of each platform's rate limits and anti-spam policies
- Consider using platform-specific hashtags and formatting