import json
import os
from django.shortcuts import render

def review_list(request):
    reviews = []
    reviews_dir = os.path.join(os.path.dirname(__file__), 'reviews')
    
    print(f"Looking for reviews in: {reviews_dir}")
    
    # check if the directory exists
    if not os.path.exists(reviews_dir):
        print(f"Directory not found: {reviews_dir}")
        return render(request, 'reviews/review_list.html', {'reviews': reviews})
    
    # list all json files in the reviews directory
    json_files = [f for f in os.listdir(reviews_dir) if f.endswith('.json')]
    print(f"Found JSON files: {json_files}")
    
    # process each JSON file
    for json_file in json_files:
        file_path = os.path.join(reviews_dir, json_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:  # specify UTF-8 encoding
                data = json.load(file)
                # Ensure the expected fields are present
                if 'username' in data and 'review' in data:
                    reviews.append(data)
        except (json.JSONDecodeError, IOError) as e:
            # for debugging test: print which files were skipped and why
            print(f"Skipping {json_file}: {str(e)}")
            continue
    
    # sort reviews by username alphabet
    reviews.sort(key=lambda x: x['username'].lower())
    
    return render(request, 'reviews/review_list.html', {'reviews': reviews})
