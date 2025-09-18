A. Project Goal & Core User Story

    Project Goal: To build a "one-click" product photography tool. A user uploads one photo, and the app intelligently analyzes the product, devises a complete creative strategy, and generates three distinct, high-quality marketing images with zero further input.

    Core User Story: "As a busy entrepreneur, I want to upload a single photo of my new product. The app should do all the thinking for me and deliver three professional, ready-to-use images that perfectly match my product's category, style, and target audience."

B. The Four-Step Autonomous AI Workflow

Step 1: Product Image Upload

    The user uploads a single product photo. The backend receives the image and initiates the AI workflow.

Step 2: AI Background Removal

    Model: Gemini 2.5 Flash

    Action: The first API call is made to Gemini to perfectly isolate the product from its original background.

    Prompt for Gemini (Cutout):

        "Analyze the provided image. Your task is to perform a perfect, studio-quality cutout of the main subject. Generate a new image that contains only this primary product on a fully transparent background. The output format must be a PNG with a clean alpha channel. Do not crop, resize, or alter the colors of the subject."

    Result: A clean "product asset" (transparent PNG) stored in a app folder.

Step 3: AI Product Analysis & Creative Direction (The "Brain")

    Model: Gemini 2.5 Flash

    Action: This is the most critical step. A second, highly-detailed API call is made to Gemini. It uses the original user image to perform two tasks in one go: first, analyze the product, and second, use that analysis to generate a full creative plan.

    Prompt for Gemini (Analysis & Creative Direction):

        "You are an expert Art Director and Product Marketer. Analyze the product in the provided image. Your task is to return a single, structured JSON object that contains both your detailed analysis and a creative strategy for three distinct product photos based on that analysis.

        The JSON object must have two top-level keys: analysis and scenes.

            The analysis object must contain:

                product_category: (e.g., 'Skincare', 'Electronics', 'Footwear')

                product_type: (e.g., 'Face Serum', 'Wireless Headphones', 'Men's Hiking Boot')

                style_tags: (An array of strings, e.g., ['Minimalist', 'Rugged', 'Luxury', 'Vibrant', 'Natural'])

            The scenes object must be an array of three scene concepts. Each concept in the array must be an object with two keys:

                scene_title: A short, descriptive title for the image.

                detailed_prompt: A complete, highly-detailed text prompt for image generation using Gemini 2.5 Flash Image generation, directly informed by your analysis.

        Crucially, ensure the detailed_prompt for each scene logically follows from the style_tags and product_type in your analysis. For example, if you analyze a product as a 'Rugged' 'Men's Hiking Boot', the scenes should involve mountains, wood, and stone, not modern cafes or minimalist studios."

    Result: A single, comprehensive JSON object containing both the "why" and the "what." Example for a hiking boot:
    code JSON.
        
    {
      "analysis": {
        "product_category": "Footwear",
        "product_type": "Men's Hiking Boot",
        "style_tags": ["Rugged", "Outdoor", "Durable"]
      },
      "scenes": [
        {
          "scene_title": "On the Summit",
          "detailed_prompt": "Create a photorealistic shot of the provided 'Men's Hiking Boot'. Place it firmly on a jagged, mossy rock with a blurred mountain peak in the background. The lighting should be bright, direct morning sun, highlighting its 'durable' texture. The mood is adventurous and 'outdoor'."
        },
        {
          "scene_title": "Product Close-up",
          "detailed_prompt": "A close-up, high-detail product shot of the provided 'Men's Hiking Boot'. Place it on a dark, weathered wooden plank. Use dramatic side-lighting to emphasize the 'rugged' materials and craftsmanship. The background should be dark and out of focus."
        },
        {
          "scene_title": "Ready for Adventure",
          "detailed_prompt": "A top-down, flat-lay style shot. Place the provided 'Men's Hiking Boot' on a canvas background next to a compass and a coiled rope to evoke an 'outdoor' adventure theme. The lighting is even and natural."
        }
      ]
    }

      

Step 4: Batch Image Generation

    Model: Gemini 2.5 Flash Image (nano banana) for each of the three images.

    Action: The backend parses the JSON from Step 3. It then loops through the scenes array. For each scene, it makes a new API call to Gemini, combining the "product asset" PNG (from Step 2) with the corresponding detailed_prompt.

    Result: Three final, high-resolution JPEG images that are perfectly aligned with the product's identity.


This is my AI Studio API key (from https://aistudio.google.com/apikey):
[YOUR_API_KEY_HERE]
