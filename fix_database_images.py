import sqlite3
import os
from pathlib import Path


def update_database_images():
    """
    Updates the database with correct image paths and loads images as BLOB data
    """
    # Database path
    db_path = "database/dietexercise_companion.db"

    # Images directory path
    images_dir = Path("images/dishes")

    # Check if images directory exists
    if not images_dir.exists():
        print(f"❌ Images directory not found: {images_dir}")
        print("Please make sure the images/dishes folder exists in your project root.")
        return False

    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get all dishes that need image updates
        cursor.execute("SELECT Id, Name FROM Dish")
        dishes = cursor.fetchall()

        updated_count = 0
        missing_images = []

        for dish_id, dish_name in dishes:
            # Expected image filename
            image_filename = f"{dish_id.zfill(2)}.jpg"  # Ensures 01.jpg, 02.jpg, etc.
            image_path = images_dir / image_filename

            if image_path.exists():
                try:
                    # Read image as binary data
                    with open(image_path, "rb") as img_file:
                        image_data = img_file.read()

                    # Update database with image data
                    cursor.execute(
                        "UPDATE Dish SET Image = ? WHERE Id = ?", (image_data, dish_id)
                    )
                    updated_count += 1
                    print(f"✅ Updated image for dish {dish_id}: {dish_name}")

                except Exception as e:
                    print(f"❌ Error reading image {image_path}: {e}")
                    missing_images.append(f"{dish_id}: {dish_name}")
            else:
                print(f"⚠️  Image not found: {image_path}")
                missing_images.append(f"{dish_id}: {dish_name}")

                # Set image to NULL for missing images
                cursor.execute("UPDATE Dish SET Image = NULL WHERE Id = ?", (dish_id,))

        # Commit changes
        conn.commit()
        conn.close()

        print(f"\n📊 Summary:")
        print(f"✅ Successfully updated {updated_count} dish images")

        if missing_images:
            print(f"⚠️  {len(missing_images)} images not found:")
            for missing in missing_images:
                print(f"   - {missing}")

        return True

    except Exception as e:
        print(f"❌ Database error: {e}")
        return False


def recreate_dish_table():
    """
    Recreates the Dish table without the hardcoded READFILE paths
    """
    db_path = "database/dietexercise_companion.db"

    # Basic dish data without images (to be updated separately)
    dishes_data = [
        (
            "01",
            "Gluten-Free Pancakes",
            "176;26;6;8",
            "Cream cheese:0.5 oz;Egg:1 quả;Honey: 1 thìa cà phê;Cinnamon: 1/2 thìa cà phê;Oatmeal: 1/2 cốc",
            "Blend ingredients or hand-whisk vigorously;Heat butter or cooking oil in small skillet and then pour out a single pancake;Once small bubbles appear all over the surface, flip the pancake;Repeat steps 2 and 3 for each pancake, serve immediately",
        ),
        (
            "02",
            "Microwave Poached Eggs",
            "72;0;5;6",
            "Egg:1 quả;Vinegar: 1/8 thìa cà phê;Water: 1/3 cốc",
            "Add the water and white vinegar to a 6 ounce custard cup;Break egg into cup, pierce egg yolk with toothpick, and cover dish loosely with plastic wrap;Place in microwave and cook for 1 minute or until desired doneness;You may need to experiment with cooking times based on the wattage of your microwave and taste preference;Immediately remove egg from hot water with a slotted spoon as it will continue to cook;Serve with salt and pepper to taste.",
        ),
        (
            "03",
            "Tuna and Hummus",
            "86.5;2.5;2;15",
            "Tuna: 2.5 oz;Rosemary: 1/2 thìa cà phê;Pepper: 0.1 g;Hummus: 1 thìa canh",
            "Mix all ingredients together and serve.",
        ),
        # Add more dishes as needed - I'll include a few key ones
        (
            "04",
            "Carrots",
            "86;20;0;2",
            "Baby carrots: 246 g",
            "Enjoy by themselves. Optionally, enjoy with a side of hummus (there are other carrot + dip recipes on ETM you can swap in).",
        ),
        (
            "05",
            "6 Minute Salmon",
            "257;7;10;37",
            "Sockeye salmon: 6 oz;Salt: 0.1 g;Garlic powder: 1/2 thìa cà phê;Lemons: 1/2 quả",
            "Preheat a cast iron skillet to high heat and set your oven to the broiler setting;Take the filet of salmon and pat dry with a paper towel. Salt the skin side of the salmon and add it to the pan, skin side down. Set the timer for two minutes. While the skin side is searing, season the other side generously with the garlic powder.Once the salmon is seared, place the cast iron into the oven for 4 minutes under the broiler;Once the 4 minutes are up, serve the salmon with lemon wedges;Enjoy!",
        ),
    ]

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Drop existing table if it exists
        cursor.execute("DROP TABLE IF EXISTS Dish")

        # Create new table structure
        cursor.execute(
            """
            CREATE TABLE Dish (
                Id varchar(255) not null,
                Name varchar(255),
                Image BLOB,
                Nutrition varchar(255),
                Recipe text,
                Steps text,
                primary key (Id)
            )
        """
        )

        # Insert basic data (without images)
        for dish_data in dishes_data:
            cursor.execute(
                "INSERT INTO Dish (Id, Name, Image, Nutrition, Recipe, Steps) VALUES (?, ?, NULL, ?, ?, ?)",
                dish_data,
            )

        conn.commit()
        conn.close()

        print("✅ Successfully recreated Dish table with clean structure")
        return True

    except Exception as e:
        print(f"❌ Error recreating table: {e}")
        return False


def main():
    """
    Main function to fix the database image issue
    """
    print("🔧 Starting database image fix process...")
    print("=" * 50)

    # Step 1: Check if we need to recreate the table
    recreate_option = (
        input("Do you want to recreate the Dish table? (y/n): ").lower().strip()
    )

    if recreate_option == "y":
        print("\n📝 Recreating Dish table...")
        if not recreate_dish_table():
            print("❌ Failed to recreate table. Exiting.")
            return

    # Step 2: Update images
    print("\n🖼️  Updating dish images...")
    if update_database_images():
        print("\n🎉 Database image fix completed successfully!")
        print("\n💡 Next steps:")
        print("1. Make sure all your dish images are in the 'images/dishes/' folder")
        print("2. Images should be named as 01.jpg, 02.jpg, etc.")
        print("3. Run your Streamlit app to test the images")
    else:
        print("\n❌ Failed to update images. Please check the error messages above.")


if __name__ == "__main__":
    main()
