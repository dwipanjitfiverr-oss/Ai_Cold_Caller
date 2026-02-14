#!/usr/bin/env python3
"""
Demo Website Generator
Generates custom website for each business
"""
import json
import os
import requests
import urllib.parse

# Load config
API_KEY = "AIzaSyAk7MBLlO79elsXw0-D60AoSH6nP-QP-Fo"
TEMPLATE_PATH = "/home/ubuntu/.openclaw/workspace/ai-caller-demo/template.html"
OUTPUT_DIR = "/home/ubuntu/.openclaw/workspace/ai-caller-demo/generated"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_template():
    with open(TEMPLATE_PATH) as f:
        return f.read()

def get_business_data(business_name, location="Delhi"):
    """Get business details from Google Maps"""
    # Search for business
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={urllib.parse.quote(business_name + ' ' + location)}&key={API_KEY}"
    r = requests.get(url)
    places = r.json().get("results", [])
    
    if not places:
        return None
    
    place_id = places[0].get("place_id")
    
    # Get full details
    url2 = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,formatted_phone_number,formatted_address,website,reviews,rating,user_ratings_total&key={API_KEY}"
    r2 = requests.get(url2)
    return r2.json().get("result", {})

def generate_website(business_name, business_data):
    """Generate custom website for business"""
    template = load_template()
    
    name = business_data.get("name", business_name)
    phone = business_data.get("formatted_phone_number", "")
    address = business_data.get("formatted_address", "")
    rating = business_data.get("rating", "4.5")
    reviews = business_data.get("reviews", [])[:3]
    
    # Clean phone for URL
    phone_clean = phone.replace(" ", "").replace("-", "")
    
    # Generate reviews HTML
    reviews_html = ""
    for review in reviews:
        author = review.get("author_name", "Customer")
        text = review.get("text", "")[:100]
        rating_review = review.get("rating", 5)
        stars = "⭐" * rating_review
        reviews_html += f"""
        <div class="bg-white p-6 rounded-xl shadow">
            <div class="flex items-center mb-2">
                <div class="font-semibold">{author}</div>
                <div class="ml-auto">{stars}</div>
            </div>
            <p class="text-gray-600">"{text}"</p>
        </div>
        """
    
    if not reviews_html:
        reviews_html = """
        <div class="bg-white p-6 rounded-xl shadow">
            <p class="text-gray-600">"Great food and excellent service!"</p>
        </div>
        <div class="bg-white p-6 rounded-xl shadow">
            <p class="text-gray-600">"Highly recommended for family dining."</p>
        </div>
        <div class="bg-white p-6 rounded-xl shadow">
            <p class="text-gray-600">"Will definitely come again!"</p>
        </div>
        """
    
    # Replace placeholders
    website = template
    website = website.replace("{{BUSINESS_NAME}}", name)
    website = website.replace("{{PHONE}}", phone)
    website = website.replace("{{PHONE_CLEAN}}", phone_clean)
    website = website.replace("{{ADDRESS}}", address)
    website = website.replace("{{RATING}}", str(rating))
    website = website.replace("{{YEARS}}", "5")
    website = website.replace("{{CUSTOM_ABOUT}}", "We have been serving delicious food to our valued customers for years. Our commitment to quality and hygiene makes us the preferred choice in the area.")
    website = website.replace("{{REVIEWS_HTML}}", reviews_html)
    
    return website

def create_demo(business_name, location="Delhi"):
    """Create demo website for a business"""
    print(f"🔍 Looking up: {business_name}...")
    
    data = get_business_data(business_name, location)
    
    if not data:
        print(f"❌ Business not found!")
        return None
    
    has_website = bool(data.get("website"))
    
    if has_website:
        print(f"❌ Already has website: {data.get('website')}")
        return None
    
    print(f"✅ Found: {data.get('name')}")
    print(f"   Phone: {data.get('formatted_phone_number', 'N/A')}")
    
    # Generate website
    website = generate_website(business_name, data)
    
    # Save
    safe_name = business_name.lower().replace(" ", "-")
    filename = f"{safe_name}.html"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, "w") as f:
        f.write(website)
    
    print(f"   ✅ Website generated: {filename}")
    
    return {
        "name": data.get("name"),
        "phone": data.get("formatted_phone_number"),
        "address": data.get("formatted_address"),
        "filename": filename,
        "filepath": filepath
    }

# Test with one business
if __name__ == "__main__":
    result = create_demo("Olive Bar & Kitchen", "Delhi")
    if result:
        print(f"\n🎉 Demo website ready!")
        print(f"   File: {result['filename']}")
