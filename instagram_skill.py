#!/usr/bin/env python3
"""
Instagram Skill (instaloader-based)
Provides public profile and recent posts for monitoring.
WARNING: Unofficial; use responsibly, rate-limited.
"""

import instaloader
import json
from datetime import datetime
import os

# Create a singleton Instaloader instance (no login)
_loader = instaloader.Instaloader(
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    download_geotags=True,
    download_comments=False,
    save_metadata=False,
    compress_json=False
)

def get_profile(username: str):
    """
    Fetch public profile info.
    Returns dict with: username, full_name, bio, followers, following, is_private, profile_pic_url, external_url, business_category, has_private_profile, etc.
    """
    try:
        profile = instaloader.Profile.from_username(_loader.context, username)
        return {
            "username": profile.username,
            "full_name": profile.full_name,
            "bio": profile.biography,
            "followers": profile.followers,
            "following": profile.followees,
            "is_private": profile.is_private,
            "profile_pic_url": profile.profile_pic_url,
            "external_url": profile.external_url,
            "business_category": profile.business_category_name,
            "has_private_profile": profile.has_private_profile,
            "media_count": profile.mediacount,
            "igtv_count": profile.igtvcount,
            "fbid": profile.fbid,
            "fetched_at": datetime.now().isoformat()
        }
    except instaloader.exceptions.QueryReturnedNotFoundException:
        return {"error": f"User {username} not found"}
    except instaloader.exceptions.ConnectionException as e:
        return {"error": f"Connection error: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}

def get_recent_posts(username: str, limit: int = 10):
    """
    Fetch recent posts (public only). Returns list of dicts with:
    - shortcode, url, date, caption, likes, comments, video_view_count, is_video, location (if geotagged)
    """
    posts = []
    try:
        profile = instaloader.Profile.from_username(_loader.context, username)
        for i, post in enumerate(profile.get_posts()):
            if i >= limit:
                break
            post_data = {
                "shortcode": post.shortcode,
                "url": f"https://www.instagram.com/p/{post.shortcode}/",
                "date": post.date_utc.isoformat(),
                "caption": post.caption if post.caption else "",
                "likes": post.likes,
                "comments": post.comments,
                "is_video": post.is_video,
                "video_view_count": post.video_view_count if post.is_video else None,
                "location": post.location.name if post.location else None,
                "location_lat": post.location.lat if post.location else None,
                "location_lng": post.location.lng if post.location else None,
                "tagged_users": [str(user) for user in post.tagged_users] if post.tagged_users else []
            }
            posts.append(post_data)
        return posts
    except Exception as e:
        return {"error": str(e)}

def get_stories(username: str):
    """
    Attempt to fetch current stories (if user is public and has active stories).
    Returns list of dicts with item url and expiration.
    """
    try:
        profile = instaloader.Profile.from_username(_loader.context, username)
        story_items = []
        # Instaloader doesn't easily expose active stories without login; this may not work for public
        # We'll use high-level: Story items are part of 'get_stories' but requires login
        return {"error": "Stories retrieval requires login; not implemented for public access"}
    except Exception as e:
        return {"error": str(e)}

def search_location_by_coords(lat, lng):
    """
    Reverse-geocode coordinates to a human-readable place.
    Uses free Nominatim (OpenStreetMap) — rate limited but okay for occasional use.
    """
    try:
        import requests
        resp = requests.get("https://nominatim.openstreetmap.org/reverse", params={
            "lat": lat,
            "lon": lng,
            "format": "json"
        }, headers={"User-Agent": "OpenClawAgent/1.0"})
        if resp.status_code == 200:
            data = resp.json()
            return data.get("display_name", f"{lat},{lng}")
        else:
            return f"{lat},{lng} (error {resp.status_code})"
    except Exception as e:
        return f"{lat},{lng} (lookup failed)"

if __name__ == "__main__":
    # Quick test
    import sys
    if len(sys.argv) > 1:
        user = sys.argv[1]
        print("Profile:", json.dumps(get_profile(user), indent=2))
        print("\nRecent posts:")
        for p in get_recent_posts(user, limit=3):
            print(json.dumps(p, indent=2))
