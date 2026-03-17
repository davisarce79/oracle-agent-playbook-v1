---
name: reddit
description: "Interact with Reddit using the reddit-simple library. Use for posting to subreddits, reading feeds, and managing comments."
---

# Reddit Skill

Use the `reddit-simple` library to interact with Reddit. Reddit is a large community platform with many free subreddits.

## Setup

1. Install the `reddit-simple` package:
   ```bash
   npm install -g reddit-simple
   ```

2. Get your Reddit credentials:
   - Reddit username and password
   - Or use OAuth if available

3. Store credentials as environment variables:
   ```bash
   export REDDIT_USERNAME="your_username"
   export REDDIT_PASSWORD="your_password"
   export REDDIT_CLIENT_ID="your_client_id"
   export REDDIT_CLIENT_SECRET="your_client_secret"
   ```

## Usage

### Post to Subreddit
```bash
node -e "
const Reddit = require('reddit-simple');

(async () => {
  try {
    const login = await Reddit.Authenticate({
      username: process.env.REDDIT_USERNAME,
      password: process.env.REDDIT_PASSWORD,
      clientId: process.env.REDDIT_CLIENT_ID,
      clientSecret: process.env.REDDIT_CLIENT_SECRET
    });
    
    const post = await Reddit.SubmitPost({
      title: 'Agent Gunna reporting in!',
      text: 'Reddit operational, Project Seed live, and trading strategies active. #AI #Trading #AutonomousAgents',
      subreddit: 'your_subreddit',
      type: 'text'
    });
    console.log('Post created:', post);
  } catch (error) {
    console.error('Error posting:', error.message);
  }
})();
"
```

### Read Subreddit Feed
```bash
node -e "
const Reddit = require('reddit-simple');

(async () => {
  try {
    const login = await Reddit.Authenticate({
      username: process.env.REDDIT_USERNAME,
      password: process.env.REDDIT_PASSWORD,
      clientId: process.env.REDDIT_CLIENT_ID,
      clientSecret: process.env.REDDIT_CLIENT_SECRET
    });
    
    const feed = await Reddit.GetSubredditHot('your_subreddit', 20);
    console.log('Subreddit feed:', feed);
  } catch (error) {
    console.error('Error getting feed:', error.message);
  }
})();
"
```

### Comment on Post
```bash
node -e "
const Reddit = require('reddit-simple');

(async () => {
  try {
    const login = await Reddit.Authenticate({
      username: process.env.REDDIT_USERNAME,
      password: process.env.REDDIT_PASSWORD,
      clientId: process.env.REDDIT_CLIENT_ID,
      clientSecret: process.env.REDDIT_CLIENT_SECRET
    });
    
    const comment = await Reddit.SubmitComment({
      fullName: 'post_fullname',
      text: 'Your comment here'
    });
    console.log('Comment posted:', comment);
  } catch (error) {
    console.error('Error commenting:', error.message);
  }
})();
"
```

## Common Operations

### Post with Link
```bash
node -e "
const Reddit = require('reddit-simple');

(async () => {
  try {
    const login = await Reddit.Authenticate({
      username: process.env.REDDIT_USERNAME,
      password: process.env.REDDIT_PASSWORD,
      clientId: process.env.REDDIT_CLIENT_ID,
      clientSecret: process.env.REDDIT_CLIENT_SECRET
    });
    
    const post = await Reddit.SubmitPost({
      title: 'Check this out!',
      url: 'https://yourlink.com',
      subreddit: 'your_subreddit',
      type: 'link'
    });
    console.log('Link post created:', post);
  } catch (error) {
    console.error('Error posting link:', error.message);
  }
})();
"
```

### Upvote Post
```bash
node -e "
const Reddit = require('reddit-simple');

(async () => {
  try {
    const login = await Reddit.Authenticate({
      username: process.env.REDDIT_USERNAME,
      password: process.env.REDDIT_PASSWORD,
      clientId: process.env.REDDIT_CLIENT_ID,
      clientSecret: process.env.REDDIT_CLIENT_SECRET
    });
    
    const upvote = await Reddit.Vote({
      name: 'post_fullname',
      vote: 1
    });
    console.log('Upvoted:', upvote);
  } catch (error) {
    console.error('Error upvoting:', error.message);
  }
})();
"
```

## Notes

- Reddit has strict rules against self-promotion
- Choose appropriate subreddits for your content
- Be mindful of Reddit's community guidelines
- API rate limits apply