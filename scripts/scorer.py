import json
import math
import os
from datetime import datetime

def calculate_score(repo):
    score = 0
    
    # 1. Star Count Score (Max 40 pts)
    # Using log scale so that a repo with 100 stars gets a good score, 
    # but a repo with 10,000 doesn't break the scale.
    stars = repo.get('stars', 0)
    if stars > 0:
        # log10(1000) is 3. This formula gives 40 pts at 1000 stars.
        star_score = min(40, (math.log10(stars) / 3) * 40)
        score += star_score

    # 2. Recent Activity Score (Max 30 pts)
    last_push_str = repo.get('last_push', '')
    if last_push_str:
        # Convert GitHub timestamp to datetime object
        last_push = datetime.strptime(last_push_str, '%Y-%m-%dT%H:%M:%SZ')
        days_since_push = (datetime.utcnow() - last_push).days
        
        if days_since_push <= 30:
            score += 30
        elif days_since_push <= 180:
            # Linear decay: Lose points as it gets older
            decay_points = 30 * (1 - (days_since_push - 30) / 150)
            score += max(0, decay_points)

    # 3. Keyword Relevance Score (Max 30 pts)
    keywords = ['privacy', 'zero-knowledge', 'zk', 'payments', 'decentralized', 'anonymous']
    description = (repo.get('description') or "").lower()
    
    matches = sum(1 for word in keywords if word in description)
    # 10 points per keyword match, capped at 30
    keyword_score = min(30, matches * 10)
    score += keyword_score

    return round(score, 2)

def process_scores():
    input_file = 'data/raw_results.json'
    output_file = 'data/scored_results.json'

    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found. Run scraper.py first!")
        return

    with open(input_file, 'r') as f:
        repos = json.load(f)

    scored_list = []
    for repo in repos:
        score = calculate_score(repo)
        if score >= 40:  # Filter out low-quality results
            repo['final_score'] = score
            scored_list.append(repo)

    # Sort by score (highest first)
    scored_list.sort(key=lambda x: x['final_score'], reverse=True)

    with open(output_file, 'w') as f:
        json.dump(scored_list, f, indent=4)

    print(f"✅ Scored {len(repos)} repos.")
    print(f"🎯 Kept {len(scored_list)} high-quality leads (Score >= 40).")
    print(f"📁 Results saved to {output_file}")

if __name__ == "__main__":
    process_scores()