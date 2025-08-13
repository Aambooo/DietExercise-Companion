import sqlite3
import os


def clean_database():
    """
    Clean up the database by removing problematic READFILE entries
    """
    db_path = "database/dietexercise_companion.db"

    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check current state
        cursor.execute("SELECT COUNT(*) FROM Dish")
        total_dishes = cursor.fetchone()[0]
        print(f"📊 Total dishes in database: {total_dishes}")

        # Update all image fields to NULL (removes READFILE references)
        cursor.execute("UPDATE Dish SET Image = NULL")
        updated_count = cursor.rowcount

        conn.commit()
        conn.close()

        print(f"✅ Successfully cleaned {updated_count} dish image entries")
        print("💡 All images have been set to NULL. You can now reload them properly.")

        return True

    except Exception as e:
        print(f"❌ Error cleaning database: {e}")
        return False


def check_database_structure():
    """
    Check the current database structure and problematic entries
    """
    db_path = "database/dietexercise_companion.db"

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check table structure
        cursor.execute("PRAGMA table_info(Dish)")
        columns = cursor.fetchall()

        print("📋 Current Dish table structure:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")

        # Check for problematic entries
        cursor.execute("SELECT Id, Name, LENGTH(Image) as img_size FROM Dish LIMIT 10")
        dishes = cursor.fetchall()

        print("\n🔍 Sample dish entries:")
        for dish in dishes:
            img_status = "Has image" if dish[2] and dish[2] > 0 else "No image"
            print(f"   - {dish[0]}: {dish[1]} - {img_status}")

        conn.close()

    except Exception as e:
        print(f"❌ Error checking database: {e}")


def main():
    """
    Main cleanup function
    """
    print("🔧 Database Cleanup Tool")
    print("=" * 40)

    # First, check current state
    print("\n1. Checking current database state...")
    check_database_structure()

    # Ask user if they want to proceed
    proceed = input("\nDo you want to clean all dish images? (y/n): ").lower().strip()

    if proceed == "y":
        print("\n2. Cleaning database...")
        if clean_database():
            print("\n✅ Cleanup completed! Next steps:")
            print("1. Run the fix_database_images.py script to reload images")
            print("2. Make sure your images are in the 'images/dishes/' folder")
            print("3. Test your Streamlit app")
        else:
            print("\n❌ Cleanup failed. Please check the error messages above.")
    else:
        print("\n❌ Cleanup cancelled by user.")


if __name__ == "__main__":
    main()
