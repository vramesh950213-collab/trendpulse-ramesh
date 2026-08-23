import requests
import json
import os
import time
from datetime import datetime

TOP_STORIES_URL="https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL= "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {"User-Agent": "TrendPulse/1.0"}

categories = {
    "technology": [
        "ai", "software", "tech", "code", "computer",
        "data", "cloud", "api", "gpu", "llm"
    ],
    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],
    "sports": [
        "nfl", "nba", "fifa", "sport", "game",
        "team", "player", "league", "championship"
    ],
    "science": [
        "research", "study", "space", "physics",
        "biology", "discovery", "nasa", "genome"
    ],
    "entertainment": [
        "movie", "film", "music", "netflix",
        "game", "book", "show", "award", "streaming"
    ]
}

def get_category(title):
  title=title.lower()

  for category,keywords in categories.items():
    for keyword in keywords:
      if keyword in title:
        return category

  return None


def fetch_story(story_id):

  url= ITEM_URL.format(story_id)

  try:
    response=requests.get(
        url,
        headers=headers,
        timeout=10)

    response.raise_for_status()

    return response.json()

  except requests.RequestException as error:
    print(f"Failed to fetch story{story_id}:{error}")
    return None



def main():

  try:
    response=requests.get(
        TOP_STORIES_URL,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    story_ids=response.json()[:500]

  except requests.RequestException as error:
    print(f"Failed to fetch top stories: {error}")
    return

  
  print(f"Found {len(story_ids)} top story IDs.")  

  stories = []

  for story_id in story_ids:

    story = fetch_story(story_id)

    if story is None:
      continue

    if "title" not in story:
      continue
    
    stories.append(story)
  
  print(f"Successfully fetch {len(stories)} stories.")

  categorized_stories={
      "technology": [],
      "worldnews": [],
      "sports": [],
      "science": [],
      "entertainment": []}

  for story in stories:
    title=story.get("title", "")
    category=get_category(title)
    if category is None:
      continue

    if len(categorized_stories[category]) >=25:
      continue

    collected_story={
        "post_id":story.get("id"),
        "title":title,
        "category":category,
        "score": story.get("score",0),
        "num_comments":story.get("descendants",0),
        "author":story.get("by","unknown"),
        "collected_at":datetime.now().isoformat()
    }

    categorized_stories[category].append(collected_story)
    

  all_stories=[]
    
  for category in categories:
    all_stories.extend(categorized_stories[category])

    time.sleep(2)

  os.makedirs("data",exist_ok=True)

  date_string = datetime.now().strftime("%Y%m%d")

  filename = f"data/trends_{date_string}.json"

  with open(filename,"w",encoding="utf-8") as file:

    json.dump(
        all_stories,
        file,
        indent=4,
        ensure_ascii=False
    )
  
  print(
      f"collected {len(all_stories)} stories."
      f"saved to {filename}"
  )

if __name__ == "__main__":
  main()