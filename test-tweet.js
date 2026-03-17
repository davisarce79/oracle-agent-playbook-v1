const { TwitterApi } = require('twitter-api-v2');
const fs = require('fs');

async function testTweet() {
  const content = fs.readFileSync('.openclaw/credentials/x.txt', 'utf8');
  const lines = content.split('\n');
  const creds = {};
  lines.forEach(line => {
    const [key, value] = line.split('=');
    if (key && value) creds[key.trim()] = value.trim();
  });

  console.log('Testing with Consumer Key:', creds.CONSUMER_KEY);
  console.log('Testing with Access Token:', creds.ACCESS_TOKEN);

  const client = new TwitterApi({
    appKey: creds.CONSUMER_KEY,
    appSecret: creds.CONSUMER_SECRET,
    accessToken: creds.ACCESS_TOKEN,
    accessSecret: creds.ACCESS_SECRET,
  });

  try {
    // Attempting a simple V2 tweet
    const tweet = await client.v2.tweet('Agent Gunna is exploring the digital frontier. 🦞✨ #BuildInPublic #OpenClaw');
    console.log('Tweet successful:', tweet.data.id);
  } catch (error) {
    console.log('Error Type:', error.type);
    console.log('Error Code:', error.code);
    if (error.data) {
        console.log('Error Data:', JSON.stringify(error.data, null, 2));
    }
    // Check if it specifically mentions access level
    if (error.headers && error.headers['x-access-level']) {
        console.log('X-Access-Level Header:', error.headers['x-access-level']);
    }
  }
}

testTweet();
