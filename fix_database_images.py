import sqlite3
import os
from pathlib import Path


def update_database_images():
    """
    Updates the database with correct image paths and loads images as BLOB data
    """
    # Database path
    db_path = "database/dietexercise_companion.db"

    # Images directory path (updated to your laptop's path)
    images_dir = Path("C:/DietExercise-Companion/images/dishes")

    # Check if images directory exists
    if not images_dir.exists():
        print(f"❌ Images directory not found: {images_dir}")
        print(
            "Please make sure the images/dishes folder exists at C:\\DietExercise-Companion\\images\\dishes"
        )
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
                print(f"⚠️ Image not found: {image_path}")
                missing_images.append(f"{dish_id}: {dish_name}")

                # Set image to NULL for missing images
                cursor.execute("UPDATE Dish SET Image = NULL WHERE Id = ?", (dish_id,))

        # Commit changes
        conn.commit()
        conn.close()

        print(f"\n📊 Summary:")
        print(f"✅ Successfully updated {updated_count} dish images")

        if missing_images:
            print(f"⚠️ {len(missing_images)} images not found:")
            for missing in missing_images:
                print(f"   - {missing}")

        return True

    except Exception as e:
        print(f"❌ Database error: {e}")
        return False


def recreate_dish_table():
    """
    Recreates the Dish table with all 94 dishes and no hardcoded READFILE paths
    """
    db_path = "database/dietexercise_companion.db"

    # Full list of dish data (without images, to be updated separately)
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
        (
            "06",
            "Green Kale Salad",
            "72;10;2;4",
            "Kale: 44.8 g;Olive oil: 1/2 thìa cà phê;Garlic: 0.5 g;Salt: 0.8 g;Pepper: 0.35 g;Celery: 22 g;Green bell pepper: 26 g;Zucchini: 16 g;Cucumber: 17 g;Broccoli: 12 g;Peas: 2 thìa canh;Alfalfa sprouts: 2 thìa canh",
            "Microwave peas until just defrosted set aside. Chop and prep other vegetables. Add kale, olive oil, garlic, salt and black pepper to a large bowl. Mix kale and olive oil together well so that kale is fully coated;Add remaining ingredients to the bowl and mix. Serve.",
        ),
        (
            "07",
            "Cream Cheese Omelet",
            "295;1;27;12",
            "Olive oil: 1 thìa canh;Egg: 2 quả;Salt: 0.4 g;Pepper: 0.1 g;Cream cheese: 1 thìa canh",
            "Heat 1 tbsp oil in a non-stick skillet over medium heat;Whisk together eggs, salt, and pepper in a small bowl;Once pan is hot and nicely coated, pour eggs into pan and cover base. Allow to cook until eggs begin to look dry; redistributing egg mixture as needed;Fold 1/3 of the egg toward the middle. Repeat with opposite side of egg, folding another 1/3 toward the middle;Slide onto plate seam side down;Top with a dollop of cream cheese and enjoy!",
        ),
        ("08", "Strawberries", "46;11;0;1", "Strawberries: 144 g", "Wash and eat."),
        (
            "09",
            "Cottage Cheese and Black Bean Tuna Salad",
            "171;8;2;31",
            "Tuna: 4 oz;Cottage cheese: 56 g;Celery: 20 g;Canned black beans: 2 thìa canh",
            "Mix all ingredients together well in a bowl. Serve as desired and enjoy!",
        ),
        (
            "10",
            "Spinach Tomato Salad",
            "186;13;14;6",
            "Spinach: 150 g;Scallions: 50 g;Tomatoes: 62 g;Olive oil: 1 thìa canh;Pepper: 0.1 g;Lemon juice: 1/2 quả",
            "Wash spinach well, drain, and chop. Squeeze out excess water. Chop green onions and tomato;Put spinach in a mixing bowl and add the tomato, scallions, oil, pepper, and the juice from 1 squeezed lemon. Toss and serve.",
        ),
        (
            "11",
            "Pasta with Red Sauce and Mozzarella",
            "309;48;7;16",
            "Whole wheat pasta: 140 g;Pasta sauce: 130 g;Mozzarella cheese: 1 oz",
            "Prepare pasta as per package directions, drain;Put pasta in bowl, drizzle pasta sauce on top, mix in, put shredded mozzarella cheese on top, and heat in microwave for 2 minutes. Enjoy!",
        ),
        (
            "12",
            "Blackberry Chocolate Shake",
            "214;17;17;2",
            "Ice cubes: 7 cục;Blackberries: 38 g;Cocoa: 1 thìa canh;Stevia Sweetener: 0.3 g;Coconut oil: 1 thìa canh;Almond milk: 240 g",
            "Combine all ingredients in a blender and pulse until smooth. Enjoy!",
        ),
        (
            "13",
            "Oranges",
            "62;15;0;1",
            "Oranges: 1 quả",
            "Peel or slice orange and eat.",
        ),
        (
            "14",
            "Curried Cabbage and Carrot Slaw",
            "61;9;0;6",
            "Onions: 18 g;Spearmint: 2 g;Carrots: 36 g;Nonfat greek yogurt: 47 g;Curry powder: 1/2 thìa cà phê;Lemon juice: 1/4 thìa cà phê;Cabbage: 24 g;Salt: 0.067 g;Pepper: 0.02 g",
            "Chop onion. Chop fresh mint. Peel and coarsely grate carrots;Combine all ingredients (excluding salt and pepper) in a bowl, toss together well. Season with salt and pepper to taste. Enjoy!",
        ),
        (
            "15",
            "Fresh Jicama Salad",
            "76;18;0;2",
            "Yambean (jicama): 180 g;Chili powder: 1/2 thìa cà phê;Lime juice: 1 thìa canh;Fresh cilantro: 1 g;Salt: 3g",
            "Cut jicama into sticks. Toss with lime juice, chili powder, salt, and chopped cilantro. Enjoy!",
        ),
        (
            "16",
            "Cinnamon Roll Smoothie",
            "303;34;14;12",
            "Almond milk: 120 g;Greek yogurt: 120 g;Rolled oats: 10 g;Brown sugar: 1/2 thìa canh;Cinnamon: 1/8 thìa cà phê;Banana: 1/2 quả",
            "Combine all ingredients in a blender and pulse until smooth. Enjoy!",
        ),
        (
            "17",
            "Buttered Toast",
            "121;12;7;4",
            "Whole-wheat bread: 1 lát;Butter: 1/2 thìa canh",
            "Toast bread to desired doneness;Spread butter across until evenly distributed;Enjoy!",
        ),
        (
            "18",
            "Sun-Dried Tomato Turkey Roll-up",
            "330;36;15;15",
            "Sun-dried tomatoes: 5 miếng;Tortillas: 1 bánh;Cream cheese: 2 thìa canh;Deli cut turkey: 57 g;Spinach: 30 g",
            "Chop sun-dried tomatoes into thin strips;Spread cream cheese on tortilla, then place turkey, spinach and sun-dried tomatoes inside. Roll up, cut in half, and enjoy!",
        ),
        (
            "19",
            "Roasted Salmon",
            "242;0;14;28",
            "Atlantic salmon: 142 g;Olive oil: 1 thìa cà phê;Tarragon: 0.3 g;Chives: 1.5 g",
            "PREPARATION: Chop chives;Preheat oven to 425°F;Rub salmon all over with 1 teaspoon oil and season with salt and pepper. Roast, skin side down, on a foil-lined baking sheet in upper third of oven until fish is just cooked through, about 12 minutes. Cut salmon in half crosswise, then lift flesh from skin with a metal spatula and transfer to a plate. Discard skin, then drizzle salmon with oil and sprinkle with herbs.",
        ),
        (
            "20",
            "Veggie Omelet",
            "149;11;1;24",
            "Spinach: 30 g;Salt: 0.4 g;Pepper: 0.1 g;Onions: 40 g;Red bell pepper: 40 g;Mushrooms: 70 g;Egg white: 180 g;Almond milk: 1 thìa canh",
            "Clean the spinach off and place it into a pan while still wet. Cook on medium heat and season with salt and pepper;Once the spinach is wilted (2-3 minutes), add the onion, bell pepper, and mushroom, and cook until the onions are translucent, the pepper chunks are soft, and mushrooms are tender;Whisk the egg whites with the almond milk;Add the eggs to the pan and scramble until cooked. Top with salt and pepper. Enjoy!",
        ),
        (
            "21",
            "Tuna Poke",
            "164;1;4;29",
            "Tuna: 4 oz;Sesame seeds: 1 thìa cà phê;Sesame oil: 1/2 thìa cà phê;Soy sauce: 1 thìa cà phê;Stevia Sweetener: 0.5 g;Salt: 0.2 g",
            "Cut fish into cubes. Toss all ingredients and enjoy!",
        ),
        (
            "22",
            "Green salad",
            "70;1;7;1",
            "Lettuce: 23 g;Spinach: 8 g;Arugula: 5 g;Basil: 1.5 g;Olive oil: 1/2 thìa canh;Red wine vinegar: 1/2 thìa canh;Salt: 0.1 g;Pepper: 0.025 g;Dijon mustard: 1/4 thìa cà phê",
            "Any 4 cups of greens should be fine. In a serving bowl, combine the greens and basil;To make the dressing, place all ingredients in a screw-top jar and shake well to combine. Just before serving, pour dressing evenly over the leaves and gently toss.",
        ),
        (
            "23",
            "Thai Pork Salad",
            "399;9;24;35",
            "Pork shoulder, blade: 127 g;Oyster sauce: 3/4 thìa canh;Soy sauce: 3/4 thìa canh;Lettuce: 35 g;Carrots: 15 g;Red bell pepper: 60 g;Light mayonnaise: 3/4 thìa canh",
            "Mix the pork with the oyster and soy sauce in a mixing bowl, and marinade overnight if desired;Fry the pork in a saucepan over a high heat, cooking in 2 portions if necessary - making sure not to overcrowd the pan;Combine all ingredients in a salad bowl (or Tupperware container if storing for later);This recipe can easily be doubled or halved by frying up the meat first and storing in the refrigerator or freezer until ready to eat.",
        ),
        (
            "24",
            "Orange Breakfast Fruit Smoothie",
            "371;59;2;34",
            "Strawberries: 150 g;Banana: 1 quả;Oranges: 1 quả;Whey protein powder: 30 g;Nonfat greek yogurt: 4 thìa canh",
            "Combine all ingredients in a blender and pulse until smooth. Enjoy!",
        ),
        (
            "25",
            "Tomato and Cheese Wrap",
            "302;29;16;11",
            "Tortillas: 1 bánh;Mayonnaise-like dressing: 1 thìa canh;Tomatoes: 60 g;Lettuce: 36 g;Cheddar cheese: 1 oz",
            "Lightly spread mayo on tortilla shell;Cut tomatoes however you like them;Layer ingredients, spreading them over the tortilla;Tuck up about an inch the side of the shell you"
            "ve decided is the bottom and roll up wrap. Enjoy!",
        ),
        (
            "26",
            "Yogurt with Papaya",
            "194;23;1;24",
            "Nonfat greek yogurt: 8 oz;Papayas: 140 g",
            "Peel and seed papaya and slice. Mix into yogurt and enjoy!",
        ),
        (
            "27",
            "Vietnamese Tofu and Noodle Salad",
            "321;29;19;12",
            "Sunflower oil: 1/2 thìa canh;Tofu: 63 g;Rice noodles: 14 g;Rice wine vinegar: 1 thìa canh;Sugar: 1 thìa cà phê;Red peppers: 11 g;Carrots: 30 g;Cucumber: 26 g;Red bell pepper: 23 g;Scallions: 11 g;Peppermint: 1 g;Basil: 1.5 g;Lettuce: 2 g;Peanuts: 18 g",
            "Soak rice noodles in lukewarm water until tender. Drain. Heat the oil in a medium-sized frying pan over a medium heat and fry the tofu for 8–10 minutes, turning regularly, until golden and crisp. Drain on kitchen paper;Add the noodles to the pan, with a splash of water and heat until warmed and cooked through;Meanwhile, mix together the ingredients for the dressing (rice vinegar, sugar, chopped red peppers), set aside;Combine the noodles, carrots, cucumber, cabbage, red pepper, spring onions, and half the herbs in a bowl, spoon the dressing over and mix together;Arrange the Little Gem lettuce leaves on a large, flat serving plate and top with the noodle salad, tofu, remaining herbs and peanuts before serving.",
        ),
        (
            "28",
            "Sea Salt Edamame",
            "147;11;7;13",
            "Salt: 0.4 g;Soybeans: 100 g",
            "Cook edamame in microwave, about 2 minutes;Sprinkle salt over;Just eat the beans, not the pods.",
        ),
        (
            "29",
            "Egg White and Mushroom Omelet",
            "142;5;6;17",
            "Egg white: 130 g;Whole milk: 2 thìa canh;Salt: 0.4 g;Pepper: 0.1 g;Olive oil: 1 thìa cà phê;Mushrooms: 70 g",
            "Whisk the egg whites, milk, salt, and pepper in a medium bowl until thoroughly combined. Set a serving plate aside;Heat oil in an 8-inch nonstick frying pan over medium heat until foaming. Add mushrooms to the pan and cook until tender, about 5-10 minutes. Remove frmo pan. Add the egg mixture to the pan and stir constantly with a rubber spatula, moving the eggs around the pan until they form small curds, about 2 to 3 minutes;Gently shake the pan and use the spatula to spread the egg mixture evenly across the pan;Remove the pan from heat. Top eggs with the mushrooms. Using the spatula, fold a third of the omelet over and onto itself. Gently push the folded side of the omelet toward the edge of the pan;Tilt the pan over the serving plate and roll the omelet onto the plate, seam side down. Serve;Enjoy!",
        ),
        (
            "30",
            "Turkey Wrap",
            "391;29;22;20",
            "Tortillas: 1 bánh;Sliced turkey: 58 g;Lettuce: 56 g;Avocados: 68 g;Tomatoes: 62 g;sliced cheese: 2 lát;Hummus: 1 thìa canh",
            "Slather hummus onto tortilla;Layer with turkey, lettuce, avocado, tomato, and cheese;Roll up and enjoy!",
        ),
        (
            "31",
            "Shrimp Cakes",
            "110;5;4;12",
            "Shrimp: 80 g;Scallions: 4 g;Red bell pepper: 6 g;Bread crumbs: 5 g;Egg Whites: 12 g;Olive oil: 1 thìa cà phê",
            "Purée about 5-6 medium shrimp, majority of scallions, and the bell pepper in a food processor. Chop remaining shrimp and mix together with purée, breadcrumbs, and egg whites. Form into 4 patties and refrigerate for about a hour;Heat oil in a pan over medium-high heat. Add patties and cook about 5 minutes per side until patties are cooked through and golden brown. Enjoy!",
        ),
        (
            "32",
            "Tuna Apple Salad",
            "482;29;13;65",
            "Tuna: 330 g;Apples: 112 g;Pickle relish: 1 thìa canh;Mayonnaise-like dressing: 3 thìa canh;Garlic powder: 1 thìa cà phê",
            "Drain water from cans and place tuna in a bowl;Finely chop apple and add to bowl;Stir in sweet relish, mayonnaise, and garlic powder. Use as desired and enjoy!",
        ),
        (
            "33",
            "Basic Parmesan Egg White Omelet",
            "228;4;15;18",
            "Egg white: 132 g;Reduced fat milk: 2 thìa canh;Salt: 0.4 g;Pepper: 0.1 g;Butter: 1 thìa canh;Parmesan cheese: 2 thìa canh",
            "Whisk the egg whites, cheese, milk, salt, and pepper in a medium bowl until thoroughly combined. Set a serving plate aside;Melt the butter in an 8-inch nonstick frying pan over medium heat until foaming. Add the egg mixture and stir constantly with a rubber spatula, moving the eggs around the pan until they form small curds, about 2 to 3 minutes;Gently shake the pan and use the spatula to spread the egg mixture evenly across the pan;Remove the pan from heat. Using the spatula, fold a third of the omelet over and onto itself. Gently push the folded side of the omelet toward the edge of the pan;Tilt the pan over the serving plate and roll the omelet onto the plate, seam side down. Serve.",
        ),
        (
            "34",
            "Turkey, Goat Cheese, and Avocado Roll",
            "120;4;9;6",
            "Lettuce: 17 g;Deli cut turkey: 10 g;Goat cheese: 14 g;Walnuts: 8 g;Avocados: 8 g;Red bell pepper: 19 g",
            "Top each lettuce leaf with a turkey slice;Spread each turkey slice with 1 tablespoon goat cheese;Sprinkle 1 teaspoon walnuts on each roll and top with 1 slice avocado;Roll and garnish with chopped bell pepper, if desired.",
        ),
        (
            "35",
            "Chicken Soup",
            "318;22;10;33",
            "Olive oil: 1/2 thìa cà phê;Onions: 75 g;Carrots: 46 g;Thyme: 0.6 g;Chicken stock: 180 g;Chicken breast: 75 g;Mushrooms: 50 g;Salt: 0.1 g;Pepper: 0.025 g;Greek yogurt: 2 thìa canh;Garlic: 0.75 g;Lemon juice: 1/2 thìa cà phê",
            "Spray a pan with non-stick spray and cook chicken for 8-10 minutes per side or until cooked through, no longer pink, and the juices run clear. Let rest 5 minutes before cutting into bite sized pieces;Heat oil in a large heavy-based pan over medium heat. Add onions, carrots, and thyme, then gently fry for 15 minutes. Stir in stock, bring to a boil, cover, then simmer for 10 minutes;Remove half the mixture, then purée with a stick blender (or in a regular blender). Tip back into the pan with the rest of the soup, mushrooms and salt and pepper, to taste. Add the chicken, then simmer for 5 minutes until heated through;Mix in the yogurt, garlic, and lemon juice, swirl into the soup in bowls, then serve.",
        ),
        (
            "36",
            "Salsa salad",
            "187;37;2;10",
            "Lettuce: 140 g;Salsa: 65 g;Fresh cilantro: 5 g;Parsley: 8 g;Pinto beans: 120 g;Carrots: 30 g;Corn: 40 g",
            "Combine everything except the corn, beans and salsa and toss with the parsely and cilantro;Mix together the pinto beans, corn, salsa and top the salad",
        ),
        (
            "37",
            "Easy Steamed Green Beans",
            "31;7;0;2",
            "Water: 60 g;Salt: 1.5 g;Green beans: 100 g",
            "Bring salted water to boil in a large frying pan or sauté pan;Add green beans, cover, and cook until green beans are tender to the bite and water has evaporated. Serve hot and enjoy!",
        ),
        (
            "38",
            "Peanut Butter Banana Oatmeal",
            "309;47;11;11",
            "Oatmeal: 40 g;Water: 276 g;Salt: 0.2 g;Peanut butter: 1 thìa canh;Banana: 1/2 quả;Reduced fat milk: 3 thìa canh;Butter: 1/4 thìa cà phê",
            "Combine the oatmeal, water and salt in a medium saucepan. Bring to a boil;Cook for 5 minutes stirring occasionally. Add the peanut butter, banana, milk and butter and mix gently. Cook for another minute and serve.",
        ),
        (
            "39",
            "Tuna Avocado Salad",
            "124;4;6;15",
            "Avocados: 34 g;Tuna: 74 g;Salt: 0.4 g;Pepper: 1.5 g",
            "Using a fork, mash up the tuna really well until the consistency is even;Mix in the avocado until smooth;Add salt and pepper to taste. Enjoy!",
        ),
        (
            "40",
            "Spicy Yogurt Dip with Carrots",
            "120;16;1;13",
            "Pepper or hot sauce: 1 thìa cà phê;Carrots: 130 g;Nonfat greek yogurt: 4 oz",
            "Stir hot sauce into yogurt to combine. Enjoy with carrot strips.",
        ),
        (
            "41",
            "Simple Steak",
            "293;0;15;38",
            "Beef tenderloin: 170 g;Salt: 1 thìa cà phê;Pepper: 1/4 thìa cà phê;Olive oil: 1 thìa cà phê",
            "Remove the steak from the refrigerator and let it come to room temperature, about 30 to 45 minutes;Season the steak on both sides with the salt and pepper. Rub both sides with the olive oil and set aside;Heat a medium heavy-bottomed frying pan (not nonstick!) over high heat until very hot but not smoking, about 3 to 4 minutes. (If the pan gets too hot and starts to smoke, take it off the heat to cool a bit.) Place the steak in the pan and let it cook undisturbed until a dark crust forms on the bottom, about 3 to 4 minutes;Flip the steak using tongs or a spatula and cook until it"
            "s medium rare, about 3 to 4 minutes more. To check for doneness, use your finger to press on the steak: It should be firm around the edges but still give in the center. You can also use an instant-read thermometer, it should read about 125°F to 130°F;Transfer the steak to a cutting board and let it rest for at least 5 minutes before serving.",
        ),
        (
            "42",
            "Mediterranean Salad",
            "74;18;0;2",
            "Spinach: 15 g;Pickles: 7.5 g;Mangos: 41 g;Cherry tomatoes: 50 g;Onions: 55 g;Lemon juice: 3 g;Salt: 0.2 g;Pepper: 0.05 g;Garlic powder: 1/2 thìa cà phê",
            "Chop and assemble all the ingredients. Toss with your favorite dressing and enjoy!",
        ),
        (
            "43",
            "Cottage Cheese & Applesauce",
            "214;20;2;28",
            "Applesauce: 120 g;Cottage cheese: 225 g",
            "Mix together and enjoy!",
        ),
        (
            "44",
            "Turkey Salad",
            "276;4;9;42",
            "Turkey, dark meat: 140 g;Lettuce: 47 g;Mayonnaise-like dressing: 1 thìa canh;Table Blend Salt Free Seasoning Blend: 1 g;Salt: 0.4 g;Pepper: 0.1 g;Lemon juice: 1 thìa cà phê",
            "Put seasonings, lemon juice, turkey, and mayo in a bowl. Mix well. Serve on top of lettuce.",
        ),
        (
            "45",
            "Cinnamon Yogurt with Sliced Apple",
            "165;35;1;8",
            "Apples: 1 quả;Nonfat yogurt: 120 g;Cinnamon: 1/4 thìa cà phê",
            "Slice apple;Sprinkle cinnamon on yogurt, dip slices of apple into yogurt and enjoy!",
        ),
        (
            "46",
            "Greek Spaghetti",
            "687;86;27;25",
            "Butter: 1 1/2 thìa cà phê;Spaghetti: 4 oz;Salt: 0.75 g;Oregano: 1/4 thìa cà phê;Parmesan cheese: 25 g",
            "Preheat oven to 250 degrees F (120 degrees C);Bring a large pot of lightly salted water to a boil. Add pasta and cook for 8 to 10 minutes or until al dente, drain;In a medium skillet over medium heat, melt butter with salt and cook until just brown. Remove from heat and toss with pasta, cheese and oregano. Pour into a 7x11 inch baking dish;Bake in preheated oven 10 to 15 minutes, until hot and bubbly.",
        ),
        (
            "47",
            "Spinach and Poached Egg Muffins",
            "375;38;15;25",
            "Vinegar: 2 thìa canh;English muffins: 1 bánh;Spinach: 195 g;Nutmeg: 1 thìa cà phê;Sour cream: 2 thìa canh;Egg: 2 quả;Salt: 0.4 g;Pepper: 0.1 g",
            "Put a pan of water on to boil and add the vinegar;Toast the muffin halves until lightly browned. Meanwhile, heat the spinach through on a saucepan, just a few minutes, season to taste and add some freshly ground nutmeg and the sour cream;When the water is at a simmer, break the eggs into a small cup and then carefully slide them into the water. Turn the heat down and simmer for 3 minutes until the white has set and it"
            "s firm, but the yolks are still soft and runny;Remove the eggs from the water with a slotted spoon. Spoon the warm, cooked spinach on top of the muffin halves and then put the eggs on top of the spinach. Season with salt and freshly ground black pepper and serve straight away.",
        ),
        (
            "48",
            "Whole Wheat Toast",
            "71;12;1;3",
            "Whole-wheat bread: 1 lát",
            "Put a slice of whole wheat bread into the toaster. Eat by itself or as a side.",
        ),
        (
            "49",
            "Cucumber Apple Salad",
            "98;24;1;2",
            "Apples: 1/2 quả;Cucumber: 1 quả;Vinegar: 1 thìa canh;Water: 1 thìa canh;Garlic Salt: 1/2 thìa cà phê;Pepper: 0.1 g;Stevia Sweetener: 1 g",
            "Chop apple and thinly slice cucumber. Combine vinegar and water. Season with garlic salt, pepper, and stevia to taste. Enjoy!",
        ),
        (
            "50",
            "Broccoli Potato Soup",
            "184;34;4;7",
            "Olive oil: 3/4 thìa cà phê;Leeks: 22 g;Carrots: 30 g;Potato: 92 g;Garlic: 4 g;Salt: 1/4 thìa cà phê;Broccoli: 150 g",
            "Cut the leek and fry in oil in a skillet over medium heat;After few minutes add chopped carrots, potato, and salt;Add hot water to cover and bring to a boil. Cook until potatoes are fork tender;Add chopped garlic and broccoli;Boil for few minutes until broccoli is tender;Transfer mixture to a blender or use a stick blender to pulse until smooth. Serve hot and enjoy!",
        ),
        (
            "51",
            "Cinnamon Toast",
            "130;19;5;4",
            "Whole-wheat bread: 1 lát;Butter: 1 thìa cà phê;Sugar: 1/2 thìa canh;Cinnamon: 1/4 thìa cà phê",
            "Use a toaster to toast the bread to desired darkness. Spread butter or margarine onto one side of each slice. In a cup or small bowl, stir together the sugar and cinnamon, sprinkle generously over hot buttered toast.",
        ),
        (
            "52",
            "Yogurt with Almonds & Honey",
            "259;18;10;27",
            "Nonfat greek yogurt: 8 oz;Almonds: 18 g;Honey: 1 thìa cà phê",
            "Rough-chop almonds and mix into yogurt and honey. Enjoy!",
        ),
        (
            "53",
            "Stuffed Sweet Potato with Hummus",
            "364;64;6;15",
            "Sweet potato: 1 củ;Kale: 50 g;Canned black beans: 130 g;Hummus: 62 g;Water: 2 thìa canh",
            "Prick sweet potato all over with a fork. Microwave on high until cooked through, 7 to 10 minutes;Meanwhile, wash kale and drain. Place in a medium saucepan, cover and cook over medium-high heat, stirring once or twice, until wilted. Add beans and water. Continue cooking, uncovered, stirring occasionally, until the mixture is steaming hot, 1 to 2 minutes;Split the sweet potato open and top with the kale and bean mixture. Top with hummus.",
        ),
        (
            "54",
            "Mango Smoothie",
            "170;40;1;3",
            "Mangos: 1 quả;Coconut water: 240 g;Ice cubes: 1 cục",
            "Combine all ingredients in a blender and pulse until smooth. Enjoy!",
        ),
        (
            "55",
            "Yogurt & Cantaloupe",
            "188;21;1;24",
            "Nonfat greek yogurt: 8 oz;Melons: 160 g",
            "Cut cantaloupe into pieces and mix with yogurt. Enjoy!",
        ),
        (
            "56",
            "Monte Cristo sandwich",
            "551;30;31;36",
            "Sliced ham: 3 lát;Swiss cheese: 1 oz;Egg: 1 quả;Reduced fat milk: 1 1/3 thìa canh;Butter: 3/4 thìa canh;Whole-wheat bread: 2 lát",
            "For each sandwich, place about 2 slices ham and 1 slice Swiss cheese between 2 slices of bread. In a mixing bowl whisk together the eggs and milk;Dip sandwiches in the egg mixture, turning carefully, until well coated and all of the mixture is absorbed. Melt butter in a large skillet or on griddle;When skillet is hot and butter is bubbly, place sandwiches in skillet and cook slowly for 8-10 minutes, turn and continue cooking until cheese is melted and both sides are golden brown.",
        ),
        (
            "57",
            "Nonfat greek yogurt",
            "142;9;1;24",
            "Nonfat greek yogurt: 240 g",
            "Scoop yogurt into a cup or bowl. To sweeten, try adding a sugar-free sweetener or a tiny bit of honey and stir.",
        ),
        (
            "58",
            "Broccoli and Apple Salad",
            "55;9;2;1",
            "Vinegar: 10 g;Sugar: 1 thìa cà phê;Dijon mustard: 3/4 thìa cà phê;Canola oil: 1/2 thìa cà phê;Pepper: 0.1 g;Salt: 0.2 g;Broccoli: 23 g;Apples: 20 g;Onions: 5 g",
            "Combine vinegar, sugar, dijon mustard, canola oil, salad and pepper in a large bowl. Stir well with a whisk;Add apple, broccoli and onion to mixture, and toss to coat.",
        ),
        (
            "59",
            "Cottage Cheese with Dill Tuna",
            "223;3;3;46",
            "Cottage cheese: 113 g;Dill: 1/2 thìa cà phê;Tuna: 165 g",
            "Drain tuna. Mix in bowl with cottage cheese and dill. Enjoy!",
        ),
        (
            "60",
            "Carrot and Orange Juice",
            "81;19;0;2",
            "Carrots: 2 củ;Oranges: 1/2 quả",
            "Peel orange. Juice carrots and orange. Mix together well just before serving. Enjoy!",
        ),
        (
            "61",
            "Tomato Basil Pasta",
            "277;47;8;10",
            "Whole wheat pasta: 2 oz;Tomatoes: 90 g;Spinach: 15 g;Pepper: 1/8 thìa cà phê;Salt: 1/4 thìa cà phê;Basil: 1 lá;Olive oil: 1/2 thìa canh",
            "Start water boiling;In second pot add tomato (diced/chopped), basil leaves, spinach (chopped), salt, pepper, and olive oil and put on medium heat for 10 minutes. Stir occasionally;Boil pasta (I prefer rotini) for ~8 minutes (follow directions on box). Then drain;Mix cooked pasta with sauce mixture.",
        ),
        (
            "62",
            "Strawberry Mango Shake",
            "152;24;4;7",
            "Reduced fat milk: 180 g;Mangos: 41 g;Strawberries: 36 g;Sugar: 1/2 thìa canh",
            "Blend milk, mangos, strawberries, and sugar together well. Enjoy!",
        ),
        (
            "63",
            "Yogurt Artichoke Dip with Rye Crisps",
            "169;26;1;15",
            "Artichoke Hearts, Quarters: 200 g;Dill weed: 1/2 thìa cà phê;Nonfat greek yogurt: 4 oz;Garlic: 3 g;Crispbread crackers: 20 g",
            "Chop drained artichoke hearts and mince garlic. Combine with dill and yogurt. Mix well. Serve with rye crackers. Enjoy!",
        ),
        (
            "64",
            "Mini Flatbread Pizza",
            "158;22;5;9",
            "Pita bread: 1 bánh;Pizza sauce: 1 thìa canh;Basil (chopped): 2.5 g;Ricotta cheese: 1 thìa canh;Mozzarella cheese: 14 g;Cherry tomatoes: 37 g;Green bell pepper: 30 g;Onions: 10 g;Basil: 4 lá",
            "Preheat oven to 400 degrees F;Spread 1 tbsp pizza sauce on top of each pita. Sprinkle evenly with basil. Stir together cheeses, and dollop on pizza. Arrange tomatoes, peppers and onion evenly on top;Bake for 5 minutes, or until cheese melts and vegetables are tender. Garnish with basil leaves, if desired. Enjoy!",
        ),
        (
            "65",
            "Tofu Salad",
            "207;10;16;8",
            "Lettuce: 94 g;Cherry tomatoes: 75 g;Tofu: 85 g;Olive oil: 1 thìa canh;Red Onion: 18 g",
            "Gently mix the ingredients in a bowl;Enjoy!",
        ),
        (
            "66",
            "Banana and Kale Smoothie",
            "278;54;6;9",
            "Coconut water: 240 g;Banana: 75 g;Kale: 67 g;Chia seeds: 14 g;Blueberries: 111 g",
            "Combine all ingredients in a blender and pulse until smooth. Enjoy!",
        ),
        (
            "67",
            "Rice Cake with Strawberries and Honey",
            "125;31;0;1",
            "Strawberries: 83 g;Honey: 1 thìa canh;Rice cakes: 1 bánh",
            "Slice strawberries. Place on rice cake and drizzle with honey. Enjoy!",
        ),
        (
            "68",
            "Bologna Caesar Wraps",
            "224;31;8;7",
            "Lettuce: 35 g;Parmesan cheese: 1 1/4 thìa canh;Caesar salad dressing: 2 thìa canh;Bologna Chicken/ pork: 7 g;Tortillas: 1 bánh",
            "Chop lettuce. Mix in a large bowl with the parmesan, dressing, and chopped bologna. Add filling to tortilla and roll up. Enjoy!",
        ),
        (
            "69",
            "Ham, Egg Beaters, and Mushroom Scramble",
            "136;4;3;22",
            "Pam cooking spray: 0.6 g;Sliced ham: 2 oz;Mushrooms: 47 g;Egg: 120 g;Pepper: 0.1 g;Cayenne pepper: 0.36 g;Turmeric: 1/4 thìa cà phê",
            "Coat pan with non-stick spray and heat over medium. Chop mushrooms and ham. Sauté until mushrooms are tender;Whisk together the egg beaters with the pepper, cayenne, and turmeric. Pour over the mushrooms and ham and scramble until eggs have reached desired doneness. Serve immediately and enjoy!",
        ),
        (
            "70",
            "Salad with Ginger-Sesame-Miso Dressing",
            "23;1;2;0",
            "Miso: 1 g;Rice wine vinegar: 1/2 thìa cà phê;Liquid aminos: 1/8 thìa cà phê;Sesame oil: 1/2 thìa cà phê;Ginger: 0.05 g;Water: 1/8 thìa canh;Lettuce: 12 g;Tomatoes: 5.6 g;Carrots: 4g",
            "Place miso, vinegar, liquid aminos, oil, ginger, and water into a blender or food processor. Blend until smooth;Combine chopped lettuce, tomatoes, and carrots. Add dressing and toss together.",
        ),
        (
            "71",
            "Sweet Potato Hash",
            "304;32;15;11",
            "Red bell pepper: 60 g;Spinach: 60 g;Sweet potato: 130 g;Egg: 56 g;Avocado oil: 2 thìa cà phê",
            "Cook chopped bell pepper, spinach and shredded sweet potatoes in avocado oil for a few minutes, until spinach is just wilted and potatoes are tender, about 5 minutes;Cook egg in a non-stick frying pan until yolk has reached desired doneness. Serve on top of the potatoes/spinach mixture. Serve and enjoy!",
        ),
        (
            "72",
            "Cod Stir-Fry",
            "303;15;7;45",
            "Cod: 230 g;Water: 240 g;Garlic: 3 g;Olive oil: 1 thìa cà phê;Cabbage: 140 g;Zucchini: 120 g;Fennel seed: 1 thìa cà phê;Curry powder: 1 thìa cà phê;Lemon juice: 6 g",
            "Heat a large pan or wok over medium-high heat. Add water and cod. Cover and let cook about 5 minutes. Add remaining ingredients and sauté for about 5 minutes. Serve immediately and enjoy!",
        ),
        (
            "73",
            "Parmesan and Mushroom Baked Eggs",
            "244;4;18;16",
            "Olive oil: 1/2 thìa canh;Mushrooms: 72 g;Salt: 0.2 g;Pepper: 0.05 g;Egg: 2 quả;Parmesan cheese: 2 thìa cà phê",
            "Preheat oven to 400 degrees F. Spray individual baking dishes for each serving or a flat casserole dish with non-stick spray;Wash mushrooms and spin dry or dry with paper towels. Slice mushrooms into slices about 1/2 inch thick;Heat oil in a large frying pan over high heat and sauté mushrooms until they have released all their liquid and the liquid has evaporated, about 6-8 minutes. Season mushrooms with a little salt and fresh ground black pepper and quickly transfer to baking dishes;Break half the eggs over the mushrooms in each individual dish (or all eggs over all the mushrooms in a casserole dish). Season eggs with a little salt and fresh ground black pepper to taste, and sprinkle with Parmesan cheese;Bake eggs until they are done to your liking, about 10 minutes for firm whites and partly-soft yolks. Serve hot, with toast if desired. Enjoy!",
        ),
        (
            "74",
            "Papaya Flaxseed Shake",
            "124;16;5;6",
            "Water: 3 thìa canh;Flaxseed: 1 thìa canh;Papayas: 70 g;Plain yogurt: 6 thìa canh",
            "Combine all ingredients in a blender and pulse until smooth. Enjoy!",
        ),
        (
            "75",
            "Cottage Cheese Tuna Salad",
            "322;9;5;61",
            "Pickles: 40 g;Jalapeno peppers: 1 quả;Cottage cheese: 226 g;Tuna: 165 g;Mustard: 1 thìa canh",
            "Mince the pickles and jalapenos, and mix in with cottage cheese, tuna, and mustard. Mix together well and use as desired.",
        ),
        (
            "76",
            "Yogurt with Walnuts & Honey",
            "260;16;10;28",
            "Walnuts: 15 g;Nonfat greek yogurt: 240 g;Honey: 1 thìa cà phê",
            "Rough-chop walnuts and mix into yogurt;Top with honey and enjoy!",
        ),
        (
            "77",
            "Cheat n Eat Vietnamese Chicken Soup",
            "148;8;5;15",
            "Rice noodles: 7 g;Chicken breast: 2 oz;Peanut oil: 3/4 thìa cà phê;Garlic: 1.5 g;Ginger: 1/2 thìa cà phê;Crushed red pepper flakes: 0.02 g;Chicken broth: 240 g;Fish sauce: 1/2 thìa canh;Fresh cilantro: 1/2 thìa canh;Onions: 1/2 thìa canh;Basil: 1/4 thìa canh",
            "Soak noodles in very hot tap water. While noodles are soaking, cut chicken into thin julienne strips;Heat oil in deep skillet over medium-high heat, add chicken, garlic, ginger, and pepper flakes;Cook, stirring for 1 minute, then add broth and fish sauce and bring to a boil. Reduce heat to medium and simmer until chicken is done, about 8 minutes;Drain and arrange noodles in bottom of bowls, ladle soup over the top and sprinkle with cilantro, onion, and basil. Serve with sriracha or chili paste, if desired.",
        ),
        (
            "78",
            "Zucchini Hash",
            "218;13;11;17",
            "Onions: 40 g;Zucchini: 124 g;Salt: 0.4 g;Pepper: 0.1 g;Pam cooking spray: 0.3 g;Egg: 2 quả;Garlic powder: 1 thìa cà phê;Onion powder: 1 thìa cà phê",
            "Chop the onion and zucchini, and then mix everything up in a bowl;Heat a pan on medium heat, and lightly spray with a cooking spray;Spoon/pour the mixture into the pan. Cook about 5 minutes and flip. Cook another 5 min.",
        ),
        (
            "79",
            "Bean Sprouts with Tofu",
            "140;7;9;9",
            "Mung beans: 52 g;Olive oil: 1/2 thìa canh;Tofu: 3 oz;Garlic: 1.5 g;Soy sauce: 1/2 thìa canh;Scallions: 12.5 g",
            "Rinse the sprouted mung beans with cold running water, drained and set aside. Remove the roots if you desire;Heat up a wok and add some cooking oil for pan-frying the tofu. When the oil is fully heated, pan-fry the tofu until they turn light brown on the surface. Transfer them to a dish lined with paper towels;Leave about 1 tablespoon of oil in the same wok, stir-fry the garlic until aromatic, then add the tofu back into the wok for a few quick stirs before adding the mung beans. Add soy sauce, scallions, and do a few more quick stirs. Plate and serve immediately.",
        ),
        (
            "80",
            "Avocado",
            "322;17;29;4",
            "Avocados: 1 quả",
            "Cut in half and remove the pit;Optional topping ideas: Sea salt, black pepper, balsamic vinegar, lemon/lime juice, or paprika.",
        ),
        (
            "81",
            "Spinach and Mushroom Breakfast Scramble",
            "192;6;5;30",
            "Coconut oil: 1 thìa cà phê;Garlic: 3 g;Mushrooms: 70 g;Egg white: 243 g;Spinach: 30 g",
            "Add coconut oil, garlic, and mushrooms to pan over medium heat;Once mushrooms are slightly softened, add egg whites and mix well. When egg whites are almost cooked, add spinach and stir until spinach is wilted. Serve immediately and enjoy.",
        ),
        (
            "82",
            "Salami Cream Cheese Sandwich",
            "553;32;36;25",
            "Cream cheese: 8 oz;Scallions: 6 g;Dill: 0.5 g;Garlic: 0.75 g;White bread: 2 lát;Lettuce: 28 g;Italian salami: 70 g",
            "In a small bowl, combine 8 oz cream cheese, ¼ cup green onions, ¼ cup dill, and press in 1 garlic clove. Mash herbs into the cream cheese;Spread about 1-2 tbsp of the cream cheese mixture on one side of each bread slice;Top with lettuce and about 6-8 pieces of salami, or to taste. Enjoy!",
        ),
        (
            "83",
            "Ham and Avocado Egg Wrap",
            "231;6;18;12",
            "Butter: 1 thìa cà phê;Egg: 1 quả;Avocados: 50 g;Sliced ham: 30 g",
            "Heat a small nonstick skillet over medium heat. Grease with butter or oil;In a bowl, crack one egg and mix well with a fork. Pour into a hot pan and tilt pan to spread egg into a large circle on the bottom of the pan into a tortilla shape;Let cook 30 seconds or until the bottom is set. Carefully flip with a large spatula and let cook another 30 seconds;Remove from pan. Let egg wrap cool slightly (or fully), top as desired with ham and avocado, roll and serve warm or cold.",
        ),
        (
            "84",
            "Toasted Pita with Gouda, Avocado, and Tomato",
            "308;41;13;11",
            "Pita bread: 1 bánh;Gouda cheese: 14 g;Tomatoes: 40 g;Avocados: 50 g",
            "Toast pita;Mash avocado and spread into pita pocket;Top with gouda and sliced tomato. Enjoy!",
        ),
        (
            "85",
            "Turkey Hummus Wrap",
            "429;31;20;34",
            "Tortillas: 1 bánh;Sliced turkey: 116 g;Lettuce: 24 g;Avocados: 68 g;Tomatoes: 62 g;American cheese: 42 g;Hummus: 2 thìa canh",
            "Slather hummus onto tortilla;Layer with turkey, lettuce, avocado, tomato, and cheese;Roll up and enjoy!",
        ),
        (
            "86",
            "Meditteranean Salad",
            "103;17;2;6",
            "Lettuce: 28 g;Cucumber: 75 g;Kidney beans: 64 g;Hummus: 1 thìa canh;Red wine vinegar: 1 thìa canh;Oregano: 1 thìa canh",
            "Chop lettuce and cucumber. Drain kidney beans. Whisk together hummus, red wine vinegar, and oregano. Toss all ingredients together in a bowl and enjoy!",
        ),
        (
            "87",
            "Black Bean and Bacon Soup",
            "148;24;2;8",
            "Canned black beans: 130 g;Onions: 3 g;Vegetable Broth: 90 g;Salsa verde: 1 thìa canh;Cumin: 1/4 thìa canh;Bacon: 3 g",
            "Drain and rinse the beans. Thinly slice the green onion;In an electric food processor or blender, combine beans, broth, salsa, and cumin. Blend until fairly smooth;Heat the bean mixture in a saucepan over medium heat until thoroughly heated;Cook bacon in a pan over medium-high heat until bacon has reached desired crispiness. Chop and mix into the bean soup. Enjoy!",
        ),
        (
            "88",
            "Basic Vegetable Juice",
            "390;92;2;12",
            "Carrots: 512 g;Red cabbage: 90 g;Spinach: 170 g;Pineapple: 226 g",
            "Juice carrots and cabbage;Blend juice with spinach and pineapple.",
        ),
        (
            "89",
            "Brie cheese on bread",
            "204;18;10;11",
            "Multi-grain bread: 1 lát;Brie cheese: 1 oz",
            "Spread cheese on bread, eat.",
        ),
        (
            "90",
            "Post-Workout Banana Protein Smoothie",
            "225;30;1;25",
            "Water: 470 g;Banana: 1 quả;Whey protein powder: 30 g",
            "Combine all ingredients in a blender and pulse until smooth. Enjoy!",
        ),
        (
            "91",
            "Hummus Chickpea Snack Sandwiches",
            "142;21;4;7",
            "Chickpeas: 40 g;Hummus: 20 g;Celery: 3 g;Whole-wheat bread: 1 lát;Pickles: 6 g;Roasted Red Peppers: 4.5 g",
            "Place chickpeas in a large bowl and mash lightly with a fork. Add hummus and mix;Chop celery and stir into hummus mix;Slice pickle into thin rounds and line half the slices bread with these slices. Divide chickpea salad evenly over the slices. Top with roasted red pepper slices and remaining slices of bread. Press down lightly. If desired, cut away edges then cut each sandwich in half to make snack-sized sandwiches. Store in a covered container until ready to serve.",
        ),
        (
            "92",
            "Breakfast Sandwich with Egg, Cheese, and Ham",
            "298;29;12;21",
            "English muffins: 1 bánh;Egg: 1 quả;Honey ham: 1 oz;Cheddar cheese: 14 g",
            "Toast English muffin. Spray and pan over medium heat with non stick spray. Whisk together eggs in a bowl and pour into pan. Cook to desired doneness and set aside;Top toasted english muffin with ham, egg, and cheese. Return to toaster for a few more minutes to melt cheese. Enjoy!",
        ),
        (
            "93",
            "Raspberry Coconut Smoothie",
            "531;88;22;5",
            "Raspberries: 250 g;Banana: 1/2 quả;Coconut milk: 80 g;Chia seeds: 1/2 thìa canh",
            "Blend all ingredients until smooth.",
        ),
        (
            "94",
            "Strawberry Pear Juice",
            "129;34;1;1",
            "Pears: 1 quả;Raspberries: 30 g;Strawberries: 36 g",
            "Core pear. Juice ingredients and mix together well just before serving. Enjoy!",
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

        # Insert all dish data (without images)
        for dish_data in dishes_data:
            cursor.execute(
                "INSERT INTO Dish (Id, Name, Image, Nutrition, Recipe, Steps) VALUES (?, ?, NULL, ?, ?, ?)",
                dish_data,
            )

        conn.commit()
        conn.close()

        print("✅ Successfully recreated Dish table with all 94 dishes")
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
        input("Do you want to recreate the Dish table with all 94 dishes? (y/n): ")
        .lower()
        .strip()
    )

    if recreate_option == "y":
        print("\n📝 Recreating Dish table...")
        if not recreate_dish_table():
            print("❌ Failed to recreate table. Exiting.")
            return

    # Step 2: Update images
    print("\n🖼️ Updating dish images...")
    if update_database_images():
        print("\n🎉 Database image fix completed successfully!")
        print("\n💡 Next steps:")
        print(
            "1. Ensure all 94 dish images are in 'C:\\DietExercise-Companion\\images\\dishes\\'"
        )
        print("2. Images should be named as 01.jpg, 02.jpg, ..., 94.jpg")
        print("3. Run your Streamlit app to test the images")
    else:
        print("\n❌ Failed to update images. Please check the error messages above.")


if __name__ == "__main__":
    main()
