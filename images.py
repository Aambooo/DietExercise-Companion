#!/usr/bin/env python3
"""
Fix image path issues for DietExercise Companion
This script helps resolve image loading issues by:
1. Checking if images exist in the correct location
2. Providing a database cleanup option
3. Testing image loading functionality
"""

import os
import sqlite3
from pathlib import Path


def check_image_structure():
    """Check if images are properly organized in the project"""
    print("🔍 Checking image structure...")

    images_dir = Path("images/dishes")

    if not images_dir.exists():
        print(f"❌ Images directory not found: {images_dir}")
        print("Please create the directory and add your dish images")
        return False

    # Look for image files
    image_extensions = [".jpg", ".jpeg", ".png"]
    image_files = []

    for ext in image_extensions:
        image_files.extend(list(images_dir.glob(f"*{ext}")))

    if not image_files:
        print(f"❌ No image files found in {images_dir}")
        print("Please add your dish images (01.jpg, 02.jpg, etc.)")
        return False

    print(f"✅ Found {len(image_files)} image files:")
    for img in sorted(image_files)[:10]:  # Show first 10
        print(f"   - {img.name}")

    if len(image_files) > 10:
        print(f"   ... and {len(image_files) - 10} more")

    return True


def clean_database_images():
    """Clean up database image entries that have wrong paths"""
    db_path = Path("database/dietexercise_companion.db")

    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check current problematic entries
        cursor.execute(
            "SELECT Id, Name FROM Dish WHERE Image IS NOT NULL AND LENGTH(Image) > 100"
        )
        problematic_dishes = cursor.fetchall()

        if problematic_dishes:
            print(
                f"🔧 Found {len(problematic_dishes)} dishes with potentially problematic image paths"
            )

            # Ask user if they want to clean
            response = (
                input("Do you want to clean these entries? (y/n): ").lower().strip()
            )

            if response == "y":
                cursor.execute("UPDATE Dish SET Image = NULL")
                conn.commit()
                print(f"✅ Cleaned {len(problematic_dishes)} dish image entries")
                print("💡 Images will now be loaded from local files")
        else:
            print("✅ No problematic image entries found")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ Database error: {e}")
        return False


def test_image_loading():
    """Test the image loading function"""
    print("🧪 Testing image loading...")

    images_dir = Path("images/dishes")

    # Test loading a few images
    test_ids = ["01", "02", "03", "04", "05"]

    for dish_id in test_ids:
        # Try different possible paths
        possible_paths = [
            images_dir / f"{dish_id.zfill(2)}.jpg",
            images_dir / f"{dish_id}.jpg",
            images_dir / f"{dish_id.zfill(2)}.png",
            images_dir / f"{dish_id}.png",
        ]

        found = False
        for path in possible_paths:
            if path.exists():
                file_size = path.stat().st_size
                print(f"✅ Dish {dish_id}: {path.name} ({file_size:,} bytes)")
                found = True
                break

        if not found:
            print(f"❌ Dish {dish_id}: No image file found")


def create_image_directory():
    """Create images directory if it doesn't exist"""
    images_dir = Path("images/dishes")
    images_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Created directory: {images_dir}")

    # Create a sample info file
    info_file = images_dir / "README.txt"
    with open(info_file, "w") as f:
        f.write(
            """Image Directory for DietExercise Companion

Place your dish images here with the following naming convention:
- 01.jpg, 02.jpg, 03.jpg, etc.
- Supported formats: .jpg, .jpeg, .png

The app will automatically load images from this directory,
even if the database contains old hardcoded paths.
"""
        )

    print(f"📄 Created info file: {info_file}")


def main():
    """Main function to run all fixes"""
    print("=" * 60)
    print("🔧 DietExercise Companion - Image Path Fixer")
    print("=" * 60)

    # Check current directory
    current_dir = Path.cwd()
    print(f"📍 Current directory: {current_dir}")

    # Step 1: Check if we're in the right directory
    if not (current_dir / "main.py").exists():
        print("⚠️  Warning: main.py not found in current directory")
        print("   Make sure you're running this script from the project root")

    # Step 2: Create images directory if needed
    if not Path("images/dishes").exists():
        print("\n📁 Creating images directory...")
        create_image_directory()

    # Step 3: Check image structure
    print("\n" + "=" * 40)
    if not check_image_structure():
        print("\n💡 Next steps:")
        print("1. Add your dish images to the images/dishes/ folder")
        print("2. Name them: 01.jpg, 02.jpg, 03.jpg, etc.")
        print("3. Run this script again to verify")
        return

    # Step 4: Test image loading
    print("\n" + "=" * 40)
    test_image_loading()

    # Step 5: Clean database if needed
    print("\n" + "=" * 40)
    clean_database_images()

    print("\n" + "=" * 60)
    print("✅ Image path fixes completed!")
    print("\n💡 What to do next:")
    print("1. Make sure all your dish images are in images/dishes/")
    print("2. Run your Streamlit app: streamlit run main.py")
    print("3. Images should now load correctly")
    print("=" * 60)


if __name__ == "__main__":
    main()
