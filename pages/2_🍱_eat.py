import streamlit as st
import sqlalchemy
from models.eat import *
import base64
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="DietExercise Companion - Food", page_icon="🍱")


def load_local_image(dish_id):
    """
    Try to load image from local file system
    """
    try:
        # Possible image paths and formats
        image_paths = [
            Path(f"images/dishes/{dish_id.zfill(2)}.jpg"),
            Path(f"images/dishes/{dish_id}.jpg"),
            Path(f"images/dishes/{dish_id.zfill(2)}.png"),
            Path(f"images/dishes/{dish_id}.png"),
            Path(f"images/dishes/{dish_id.zfill(2)}.jpeg"),
            Path(f"images/dishes/{dish_id}.jpeg"),
        ]

        for image_path in image_paths:
            if image_path.exists():
                with open(image_path, "rb") as img_file:
                    return img_file.read()

        return None

    except Exception as e:
        print(f"Error loading local image for dish {dish_id}: {e}")
        return None


def display_dish_image(dish, width="100%"):
    """
    Display dish image with proper fallback handling
    """
    # Try to get image from database first
    image_data = dish.image

    # If no image in database, try to load from local files
    if image_data is None or (isinstance(image_data, bytes) and len(image_data) == 0):
        image_data = load_local_image(dish.id)

    # If we have image data, display it
    if image_data is not None and len(image_data) > 0:
        try:
            image_b64 = base64.b64encode(image_data).decode("utf-8")
            st.image(image_data, width=350, caption=f"Image of {dish.name}")
            return True
        except Exception as e:
            print(f"Error displaying image for dish {dish.name}: {e}")

    # Fallback: Show text placeholder
    st.info(f"🍽️ Image not available for {dish.name}")
    return False


# Enhanced styling
st.markdown(
    """
<style>
    .main > div {
        padding-top: 2rem;
    }
    
    .stSelectbox > div > div {
        background-color: rgb(38, 39, 48);
        color: #ffffff !important;
    }
    
    .nutrition-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
    }
    
    .recipe-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 5px solid #667eea;
    }
    
    .steps-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
</style>
""",
    unsafe_allow_html=True,
)

# Header
st.markdown(
    """
    <div style="text-align: center; padding: 1.5rem 0; margin-bottom: 1.5rem;">
        <h1 style="color: #2E86AB; font-size: 2.8rem; font-weight: bold; margin-bottom: 0.3rem;">
            Your DietExercise Companion
        </h1>
        <p style="color: #666; font-size: 1.2rem; font-style: italic; margin-top: 0;">
            Know Your Workout & Nutritional Criteria
        </p>
    </div>
""",
    unsafe_allow_html=True,
)

# Database connection with error handling
try:
    engine = sqlalchemy.create_engine("sqlite:///database/dietexercise_companion.db")
    with engine.connect() as conn:
        all_dish_results = conn.execute("SELECT * FROM Dish").fetchall()

    dish_keywords = [""]
    for d in all_dish_results:
        dish = Dish(*d)
        dish_keywords.append(dish.name)

except Exception as e:
    st.error(f"❌ Database connection error: {str(e)}")
    st.info(
        "Please make sure your database file exists at: database/dietexercise_companion.db"
    )
    st.stop()

col1, col2, col3 = st.columns([0.4, 1.2, 0.4])
with col2:
    st.markdown(
        f"""
            <h1 style="text-align: center">Food & Recipe Browser</h1>
        """,
        unsafe_allow_html=True,
    )
    dish_keyword = st.selectbox("**Search**", tuple(dish_keywords))

if dish_keyword != "":
    try:
        with engine.connect() as conn:
            dish_result = conn.execute(
                "SELECT * FROM Dish WHERE Name = :name", {"name": dish_keyword}
            ).fetchone()

            if dish_result is None:
                st.error(f"❌ Dish '{dish_keyword}' not found in database")
                st.info("This might be due to database synchronization issues.")
                st.stop()

            dish = Dish(*dish_result)

        # Dish title
        st.markdown(
            f"""
            <div style="text-align: center; margin: 2rem 0;">
                <h2 style="color: #2E86AB; font-size: 2.2rem; font-weight: 600;">
                    {dish.name}
                </h2>
                <div style="width: 100px; height: 3px; 
                           background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                           margin: 10px auto; border-radius: 2px;"></div>
            </div>
        """,
            unsafe_allow_html=True,
        )

        # Main content layout
        col1, col2 = st.columns([1.5, 1])

        # Image column
        with col1:
            display_dish_image(dish)

        # Nutrition column
        with col2:
            nutrition_detail = dish.get_nutrition_detail()

            # Create a simple nutrition info box
            st.markdown("#### 📊 Nutrition Facts")

            # Display nutrition info in a clean format
            nutrition_col1, nutrition_col2 = st.columns(2)

            with nutrition_col1:
                st.metric("Calories", f"{round(nutrition_detail.calories)}")
                st.metric("Carbs", f"{nutrition_detail.carbs} g")

            with nutrition_col2:
                st.metric("Fat", f"{nutrition_detail.fat} g")
                st.metric("Protein", f"{nutrition_detail.protein} g")

            # Pie chart
            st.markdown("#### 📈 Calorie Distribution")

            matplotlib.rcParams.update({"font.size": 10})
            labels = ["Carbs", "Fat", "Protein"]
            colors = ["#F7D300", "#38BC56", "#D35454"]
            data = [
                nutrition_detail.get_carbs_percentage(),
                nutrition_detail.get_fat_percentage(),
                nutrition_detail.get_protein_percentage(),
            ]

            fig, ax = plt.subplots(figsize=(4, 4))
            wedges, texts, autotexts = ax.pie(
                data,
                labels=labels,
                colors=colors,
                explode=(0.05, 0.05, 0.05),
                autopct="%1.1f%%",
                startangle=90,
                textprops={"fontweight": "bold", "fontsize": 10},
            )

            for autotext in autotexts:
                autotext.set_color("white")
                autotext.set_fontweight("bold")

            st.pyplot(fig)

        # Recipe and Steps sections
        st.markdown("<br/>", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1.5])

        # Recipe column
        with col1:
            st.markdown("#### 🛒 Ingredients")
            recipe_detail = dish.get_recipe_detail()

            for ingredient, amount in recipe_detail.ingredients.items():
                st.markdown(f"**{ingredient}:** {amount}")

        # Steps column
        with col2:
            st.markdown("#### 👨‍🍳 Cooking Instructions")
            steps_detail = dish.get_steps_detail()

            step_number = 1
            for step, detail in steps_detail.steps.items():
                st.markdown(f"**Step {step_number}:** {detail}")
                step_number += 1

    except Exception as e:
        st.error(f"❌ Error loading dish data: {str(e)}")
        st.info("There might be an issue with the database connection or data format.")
