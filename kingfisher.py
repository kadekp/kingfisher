#!/usr/bin/env python3
import os
import json
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

import click
import base64
from openai import OpenAI
from PIL import Image
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
if not OPENROUTER_API_KEY:
    print("Error: OPENROUTER_API_KEY not found in .env file")
    exit(1)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

def validate_models():
    """Validate that required models are available and support the necessary capabilities"""
    required_models = {
        "google/gemini-2.5-flash-image-preview": "image generation and background removal",
        "google/gemini-2.5-flash": "product analysis"
    }
    
    print("🔄 Validating OpenRouter models...")
    for model, purpose in required_models.items():
        try:
            # Test with a simple request to verify model availability
            test_response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=1
            )
            print(f"✓ {model} - Available for {purpose}")
        except Exception as e:
            print(f"❌ {model} - Error: {e}")
            print(f"This model is required for {purpose}")
            return False
    
    print("✓ All required models are available")
    return True

def encode_image_to_base64(image_path):
    """Convert image file to base64 string"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"❌ Error reading image file {image_path}: {type(e).__name__}: {e}")
        raise

def pil_image_to_base64(pil_image):
    """Convert PIL Image to base64 string"""
    try:
        buffered = BytesIO()
        pil_image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    except Exception as e:
        print(f"❌ Error converting PIL image to base64: {type(e).__name__}: {e}")
        raise

def create_output_dir() -> Path:
    """Create timestamped output directory"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_dir = Path("output") / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def copy_original_image(image_path: str, output_dir: Path) -> None:
    """Copy original image to output directory"""
    original_path = output_dir / "original.jpg"
    shutil.copy2(image_path, original_path)
    print(f"✓ Original image saved to {original_path}")

def load_prompt(prompt_file):
    """Load prompt from prompts folder"""
    try:
        with open(f"prompts/{prompt_file}.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"❌ Error: Prompt file prompts/{prompt_file}.txt not found")
        return None
    except Exception as e:
        print(f"❌ Error loading prompt file prompts/{prompt_file}.txt: {type(e).__name__}: {e}")
        return None

def remove_background(image_path: str, output_dir: Path) -> Path:
    """Remove background from product image using OpenRouter"""
    print("🔄 Step 2: Removing background...")
    
    cutout_path = output_dir / "cutout.png"
    
    # Encode input image to base64
    base64_image = encode_image_to_base64(image_path)
    
    # Create background removal prompt
    prompt = load_prompt("background_removal")
    if not prompt:
        return None
    
    try:
        # Generate image with transparent background
        response = client.chat.completions.create(
            model="google/gemini-2.5-flash-image-preview",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }}
                ]
            }],
            modalities=["image", "text"]
        )
        
        # Extract generated image data from response
        message = response.choices[0].message
        if hasattr(message, 'model_extra') and message.model_extra and 'images' in message.model_extra:
            images = message.model_extra['images']
            for img in images:
                if isinstance(img, dict) and 'image_url' in img:
                    url = img['image_url']['url']
                    if url.startswith('data:image'):
                        # Extract base64 from data URL
                        base64_data = url.split(',')[1]
                        image_data = base64.b64decode(base64_data)
                        
                        # Save the generated cutout
                        cutout_image = Image.open(BytesIO(image_data))
                        cutout_image.save(cutout_path, 'PNG')
                        print(f"✓ Background removed, cutout saved to {cutout_path}")
                        return cutout_path
        
        # Fallback: copy original if no image generated
        shutil.copy2(image_path, cutout_path)
        print(f"⚠ Fallback: copied original as cutout to {cutout_path}")
            
    except Exception as e:
        # Check if it's a rate limit error
        if "429" in str(e) or "rate" in str(e).lower():
            print("⏳ Rate limit hit, waiting 15 seconds before retry...")
            time.sleep(15)
            
            try:
                # Retry once
                response = client.chat.completions.create(
                    model="google/gemini-2.5-flash-image-preview",
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }}
                        ]
                    }],
                    modalities=["image", "text"]
                )
                
                retry_message = response.choices[0].message
                if hasattr(retry_message, 'model_extra') and retry_message.model_extra and 'images' in retry_message.model_extra:
                    retry_images = retry_message.model_extra['images']
                    for img in retry_images:
                        if isinstance(img, dict) and 'image_url' in img:
                            url = img['image_url']['url']
                            if url.startswith('data:image'):
                                # Extract base64 from data URL
                                base64_data = url.split(',')[1]
                                image_data = base64.b64decode(base64_data)
                                
                                cutout_image = Image.open(BytesIO(image_data))
                                cutout_image.save(cutout_path, 'PNG')
                                print(f"✓ Background removed after retry, cutout saved to {cutout_path}")
                                return cutout_path
                
                shutil.copy2(image_path, cutout_path)
                print(f"⚠ Retry fallback: copied original as cutout to {cutout_path}")
                    
            except Exception as retry_e:
                print(f"⚠ Retry failed: {retry_e}")
                shutil.copy2(image_path, cutout_path)
                print(f"⚠ Final fallback: copied original as cutout to {cutout_path}")
        else:
            print(f"⚠ Error removing background: {type(e).__name__}: {e}")
            print(f"This might be due to model availability, API limits, or network issues.")
            # Fallback: copy original if other error occurs
            shutil.copy2(image_path, cutout_path)
            print(f"⚠ Fallback: copied original as cutout to {cutout_path}")
            print(f"You may need to manually remove the background from {cutout_path}")
    
    return cutout_path

def analyze_product(image_path: str, output_dir: Path, count: int) -> Dict[str, Any]:
    """Analyze product and generate creative direction using OpenRouter"""
    print("🔄 Step 3: Analyzing product and generating creative direction...")
    
    # Encode image to base64
    base64_image = encode_image_to_base64(image_path)
    
    prompt_template = load_prompt("product_analysis")
    if not prompt_template:
        return None
    
    prompt = prompt_template.replace("{count}", str(count))
    
    response = client.chat.completions.create(
        model='google/gemini-2.5-flash',
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }}
            ]
        }]
    )
    
    try:
        # Extract text response
        response_text = response.choices[0].message.content
        
        # Find JSON in the response (it might be wrapped in markdown code blocks)
        if '```json' in response_text:
            start = response_text.find('```json') + 7
            end = response_text.find('```', start)
            json_text = response_text[start:end].strip()
        else:
            json_text = response_text.strip()
        
        analysis_data = json.loads(json_text)
        
        # Save analysis to file
        analysis_path = output_dir / "analysis.json"
        with open(analysis_path, 'w') as f:
            json.dump(analysis_data, f, indent=2)
        
        print(f"✓ Product analysis completed and saved to {analysis_path}")
        print(f"  Product: {analysis_data['analysis']['product_type']}")
        print(f"  Category: {analysis_data['analysis']['product_category']}")
        print(f"  Style: {', '.join(analysis_data['analysis']['style_tags'])}")
        
        return analysis_data
        
    except (json.JSONDecodeError, KeyError) as e:
        print(f"❌ Error parsing analysis response: {type(e).__name__}: {e}")
        print("The AI response was not in the expected JSON format.")
        print(f"Raw response: {response_text[:500]}...")
        print("This might be due to model changes or API issues. Please try again.")
        exit(1)
    except Exception as e:
        print(f"❌ Error during product analysis: {type(e).__name__}: {e}")
        print("This might be due to model availability, API limits, or network issues.")
        exit(1)

def generate_images(cutout_path: Path, scenes: List[Dict[str, str]], output_dir: Path) -> None:
    """Generate marketing images using Gemini Image generation"""
    print("🔄 Step 4: Generating marketing images...")
    
    # Load the cutout image and convert to base64
    try:
        cutout_image = Image.open(cutout_path)
        base64_cutout = pil_image_to_base64(cutout_image)
    except Exception as e:
        print(f"❌ Error loading cutout image {cutout_path}: {type(e).__name__}: {e}")
        print("Cannot proceed with image generation without a valid cutout.")
        return
    
    for i, scene in enumerate(scenes, 1):
        print(f"  Generating scene {i}: {scene['scene_title']}")
        scene_path = output_dir / f"scene{i}.jpg"
        
        try:
            # Generate marketing image with scene prompt and product cutout
            response = client.chat.completions.create(
                model="google/gemini-2.5-flash-image-preview",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": scene['detailed_prompt']},
                        {"type": "image_url", "image_url": {
                            "url": f"data:image/png;base64,{base64_cutout}"
                        }}
                    ]
                }],
                modalities=["image", "text"]
            )
            
            # Extract generated image data
            scene_message = response.choices[0].message
            if hasattr(scene_message, 'model_extra') and scene_message.model_extra and 'images' in scene_message.model_extra:
                scene_images = scene_message.model_extra['images']
                for img in scene_images:
                    if isinstance(img, dict) and 'image_url' in img:
                        url = img['image_url']['url']
                        if url.startswith('data:image'):
                            # Extract base64 from data URL
                            base64_data = url.split(',')[1]
                            image_data = base64.b64decode(base64_data)
                            
                            # Save the generated scene image
                            generated_image = Image.open(BytesIO(image_data))
                            generated_image.save(scene_path, 'JPEG')
                            print(f"    ✓ {scene['scene_title']} saved to {scene_path}")
                            break
                else:
                    # Fallback: copy cutout if no valid image found
                    shutil.copy2(cutout_path, scene_path)
                    print(f"    ⚠ Fallback: copied cutout as scene{i} to {scene_path}")
            else:
                # Fallback: copy cutout if no image generated
                shutil.copy2(cutout_path, scene_path)
                print(f"    ⚠ Fallback: copied cutout as scene{i} to {scene_path}")
                
        except Exception as e:
            # Check if it's a rate limit error
            if "429" in str(e) or "rate" in str(e).lower():
                print(f"    ⏳ Rate limit hit for scene {i}, waiting 15 seconds before retry...")
                time.sleep(15)
                
                try:
                    # Retry once
                    response = client.chat.completions.create(
                        model="google/gemini-2.5-flash-image-preview",
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": scene['detailed_prompt']},
                                {"type": "image_url", "image_url": {
                                    "url": f"data:image/png;base64,{base64_cutout}"
                                }}
                            ]
                        }],
                        modalities=["image", "text"]
                    )
                    
                    retry_scene_message = response.choices[0].message
                    if hasattr(retry_scene_message, 'model_extra') and retry_scene_message.model_extra and 'images' in retry_scene_message.model_extra:
                        retry_scene_images = retry_scene_message.model_extra['images']
                        for img in retry_scene_images:
                            if isinstance(img, dict) and 'image_url' in img:
                                url = img['image_url']['url']
                                if url.startswith('data:image'):
                                    # Extract base64 from data URL
                                    base64_data = url.split(',')[1]
                                    image_data = base64.b64decode(base64_data)
                                    
                                    generated_image = Image.open(BytesIO(image_data))
                                    generated_image.save(scene_path, 'JPEG')
                                    print(f"    ✓ {scene['scene_title']} saved after retry to {scene_path}")
                                    break
                        else:
                            shutil.copy2(cutout_path, scene_path)
                            print(f"    ⚠ Retry fallback: copied cutout as scene{i} to {scene_path}")
                    else:
                        shutil.copy2(cutout_path, scene_path)
                        print(f"    ⚠ Retry fallback: copied cutout as scene{i} to {scene_path}")
                        
                except Exception as retry_e:
                    print(f"    ⚠ Retry failed for scene {i}: {retry_e}")
                    shutil.copy2(cutout_path, scene_path)
                    print(f"    ⚠ Final fallback: copied cutout as scene{i} to {scene_path}")
            else:
                print(f"    ⚠ Error generating scene {i}: {type(e).__name__}: {e}")
                print(f"    This might be due to model availability, API limits, or network issues.")
                # Fallback: copy cutout if other error occurs
                shutil.copy2(cutout_path, scene_path)
                print(f"    ⚠ Fallback: copied cutout as scene{i} to {scene_path}")
                print(f"    You can manually create scene {i} using: {scene['detailed_prompt'][:100]}...")
            
        print(f"    Prompt: {scene['detailed_prompt'][:100]}...")

@click.command()
@click.argument('image_path', type=click.Path(exists=True))
@click.option('--count', '-c', default=1, type=click.IntRange(1, 5), 
              help='Number of marketing images to generate (1-5, default: 1)')
def main(image_path: str, count: int):
    """Kingfisher: One-click product photography tool
    
    Upload one product photo and get professional marketing images.
    """
    print("🐦 Kingfisher - One-Click Product Photography")
    print("=" * 50)
    
    # Validate models before proceeding
    if not validate_models():
        print("Error: Required models are not available. Please check your OpenRouter setup.")
        return
    
    # Validate image file
    if not image_path.lower().endswith(('.jpg', '.jpeg', '.png')):
        print("Error: Please provide a JPEG or PNG image file")
        return
    
    # Create output directory
    output_dir = create_output_dir()
    print(f"Output directory: {output_dir}")
    print()
    
    # Step 1: Copy original image
    print("🔄 Step 1: Processing image upload...")
    copy_original_image(image_path, output_dir)
    
    # Step 2: Remove background
    cutout_path = remove_background(image_path, output_dir)
    
    # Step 3: Analyze product and generate creative direction
    analysis_data = analyze_product(image_path, output_dir, count)
    
    # Step 4: Generate marketing images
    scenes = analysis_data['scenes']
    generate_images(cutout_path, scenes, output_dir)
    
    print()
    print("🎉 Complete! Your marketing images are ready.")
    print(f"📁 Output folder: {output_dir}")
    print("   📄 original.jpg - Your original image")
    print("   📄 cutout.png - Product with transparent background") 
    print("   📄 analysis.json - AI analysis and creative direction")
    if count == 1:
        print("   📄 scene1.jpg - Marketing image")
    elif count == 2:
        print("   📄 scene1.jpg, scene2.jpg - Marketing images")
    else:
        scene_files = ", ".join([f"scene{i}.jpg" for i in range(1, count + 1)])
        print(f"   📄 {scene_files} - Marketing images")

if __name__ == '__main__':
    main()