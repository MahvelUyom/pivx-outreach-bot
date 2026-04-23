import requests
import json
import time
import os

def search_github_repos():
    # The keywords you specified
    queries = [
        'zero knowledge proof privacy',
        'zk-SNARKs payments',
        'proof-of-stake privacy',
        'decentralized identity privacy',
        'private transactions blockchain'
    ]
    
    base_url = "https://api.github.com/search/repositories"
    all_results = []

    print(f"🚀 Starting GitHub scrape for {len(queries)} categories...")

    for query in queries:
        print(f"🔍 Searching for: {query}")
        
        # We fetch the top 30 results for each keyword to stay within safe limits
        params = {
            'q': query,
            'sort': 'stars',
            'order': 'desc'
        }
        
        try:
            response = requests.get(base_url, params=params)
            
            # Handle rate limiting or errors
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                
                for item in items:
                    repo_data = {
                        'name': item['full_name'],
                        'description': item['description'],
                        'stars': item['stargazers_count'],
                        'last_push': item['pushed_at'],
                        'open_issues': item['open_issues_count'],
                        'url': item['html_url'],
                        'category': query
                    }
                    all_results.append(repo_data)
                
                print(f"✅ Found {len(items)} repos.")
            elif response.status_code == 403:
                print("⚠️ Rate limit hit! GitHub is blocking unauthenticated requests temporarily.")
                break
            else:
                print(f"❌ Error: {response.status_code}")

        except Exception as e:
            print(f"An error occurred: {e}")

        # 1-second delay as requested to be polite to the API
        time.sleep(1)

    # Ensure the data directory exists
    os.makedirs('data', exist_ok=True)

    # Save to data/raw_results.json
    with open('data/raw_results.json', 'w') as f:
        json.dump(all_results, f, indent=4)
    
    print(f"\n📁 Task Complete! Saved {len(all_results)} repositories to data/raw_results.json")

if __name__ == "__main__":
    search_github_repos()