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


def display_dish_image(dish, width="90%"):
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
            st.markdown(
                f"""
                <div style="text-align: right; margin: 20px 0;">
                    <img src="data:image/jpeg;base64,{image_b64}" 
                         width="{width}" 
                         style="
                             border-radius: 12px; 
                             box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                             border: 1px solid #e0e0e0;
                             max-height: 400px;
                             object-fit: cover;
                         ">
                </div>
                """,
                unsafe_allow_html=True,
            )
            return True
        except Exception as e:
            print(f"Error displaying image for dish {dish.name}: {e}")

    # Fallback: Show attractive placeholder
    st.markdown(
        f"""
        <div style="
            text-align: center; 
            padding: 60px 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px; 
            margin: 20px 0; 
            color: white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        ">
            <div style="font-size: 64px; margin-bottom: 15px; opacity: 0.9;">🍽️</div>
            <h3 style="margin: 10px 0; font-weight: 300;">Image Not Available</h3>
            <p style="margin: 0; opacity: 0.8; font-size: 14px;">for {dish.name}</p>
            <p style="margin: 5px 0; opacity: 0.6; font-size: 12px;">
                Place image as {dish.id.zfill(2)}.jpg in images/dishes/ folder
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return False


# A workaround using st.markdown() to apply some style sheets to the page
st.markdown(
    f"""
        <style>
            /* Make the default header of streamlit invisible */
            .css-18ni7ap.e8zbici2 {{
                opacity: 0
            }}

            /* Make the default footer of streamlit invisible */
            .css-h5rgaw.egzxvld1 {{
            opacity: 0
            }}

            /* Change width and padding of the page */
            .block-container.css-91z34k.egzxvld4 {{
            width: 100%;
            padding: 0.5rem 1rem 10rem;
            max-width: none;
            }}

            /* Change padding of the pages list in the sidebar */
            .css-uc76bn.e1fqkh3o9 {{
            padding-top: 2rem;
            padding-bottom: 0.25rem;
            }}
            
            /* Enhanced table styling */
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 10px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border-radius: 8px;
                overflow: hidden;
            }}
            
            th {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 12px;
                text-align: left;
                font-weight: 600;
            }}
            
            td {{
                padding: 12px;
                border-bottom: 1px solid #f0f0f0;
                background: white;
            }}
            
            tr:last-child td {{
                border-bottom: none;
            }}
            
            /* Nutrition table specific styling */
            .nutrition-table {{
                background: #f8f9fa;
                border-radius: 12px;
                padding: 5px;
            }}
        </style>
        """,
    unsafe_allow_html=True,
)

# Centered header without logo - full width and flexible
st.markdown(
    """
    <div style="text-align: center; padding: 1.5rem 0; margin-bottom: 1.5rem;">
        <h1 style="
            color: #2E86AB; 
            font-size: 2.8rem; 
            font-weight: bold; 
            margin-bottom: 0.3rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        ">Your DietExercise Companion</h1>
        <p style="
            color: #666; 
            font-size: 1.2rem; 
            font-style: italic; 
            margin-top: 0;
            font-weight: 300;
        ">Know Your Workout & Nutritional Criteria</p>
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
            <div style="text-align: center; margin: 2rem 0;">
                <h1 style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    font-size: 2.5rem;
                    font-weight: 700;
                    margin-bottom: 1rem;
                ">Food & Recipe Browser</h1>
                <p style="color: #666; font-size: 1.1rem; margin-bottom: 2rem;">
                    Discover delicious and healthy recipes for your diet plan
                </p>
            </div>
        """,
        unsafe_allow_html=True,
    )

    # Enhanced selectbox styling
    dish_keyword = st.selectbox(
        "**🔍 Search for a dish**",
        tuple(dish_keywords),
        help="Select a dish to view its recipe, nutrition info, and cooking instructions",
    )

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

        # Dish title with enhanced styling
        st.markdown(
            f"""
                <div style="text-align: center; margin: 2rem 0;">
                    <h2 style="
                        color: #2E86AB;
                        font-size: 2.2rem;
                        font-weight: 600;
                        margin-bottom: 0.5rem;
                        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
                    ">{dish.name}</h2>
                    <div style="
                        width: 100px;
                        height: 3px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        margin: 10px auto;
                        border-radius: 2px;
                    "></div>
                </div>
            """,
            unsafe_allow_html=True,
        )

        # Main content layout
        col1, col2, col3 = st.columns([1.3, 0.55, 0.15])

        # Image column
        with col1:
            display_dish_image(dish)

        # Nutrition column
        with col2:
            nutrition_detail = dish.get_nutrition_detail()

            st.markdown(
                f"""
                    <div class="nutrition-table">
                        <table style="width:100%; margin: 0;">
                            <tr>
                                <th style="font-size: 18px; text-align: center;">📊 Nutrition Facts</th>
                            </tr>
                            <tr>
                                <td style="padding: 20px;">
                                    <div style="display: flex; justify-content: space-between; margin: 8px 0; padding: 5px 0; border-bottom: 1px solid #eee;">
                                        <b style="color: #333;">Calories:</b>
                                        <span style="color: #e74c3c; font-weight: 600;">{round(nutrition_detail.calories)} cal</span>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; margin: 8px 0; padding: 5px 0; border-bottom: 1px solid #eee;">
                                        <b style="color: #333;">Carbs:</b>
                                        <span style="color: #f39c12; font-weight: 600;">{nutrition_detail.carbs} g</span>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; margin: 8px 0; padding: 5px 0; border-bottom: 1px solid #eee;">
                                        <b style="color: #333;">Fat:</b>
                                        <span style="color: #27ae60; font-weight: 600;">{nutrition_detail.fat} g</span>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; margin: 8px 0; padding: 5px 0;">
                                        <b style="color: #333;">Protein:</b>
                                        <span style="color: #8e44ad; font-weight: 600;">{nutrition_detail.protein} g</span>
                                    </div>
                                </td>
                            </tr>
                        </table>
                    </div>
                    <br/>
                    <div style="text-align:center; font-size:16px; margin: 15px 0;">
                        <b style="color: #2c3e50;">Calorie Distribution</b>
                    </div>
                """,
                unsafe_allow_html=True,
            )

            # Enhanced pie chart
            matplotlib.rcParams.update({"font.size": 8})
            label = ["Carbs", "Fat", "Protein"]
            colors = ["#F7D300", "#38BC56", "#D35454"]
            data = [
                nutrition_detail.get_carbs_percentage(),
                nutrition_detail.get_fat_percentage(),
                nutrition_detail.get_protein_percentage(),
            ]

            fig, ax = plt.subplots(figsize=(3, 3))
            wedges, texts, autotexts = ax.pie(
                data,
                labels=label,
                colors=colors,
                explode=(0.1, 0.05, 0.05),
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops={"edgecolor": "white", "linewidth": 2},
                textprops={"fontweight": "bold", "fontsize": 9},
            )

            # Make percentage text white and bold
            for autotext in autotexts:
                autotext.set_color("white")
                autotext.set_fontweight("bold")

            ax.set_facecolor("none")
            fig.patch.set_facecolor("none")
            st.pyplot(fig, transparent=True)

        # Recipe and Steps sections
        st.markdown("<br/><br/>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([0.122, 0.45, 1.278, 0.15])

        # Recipe column
        with col2:
            recipe_detail = dish.get_recipe_detail()
            recipe_table_builder = """
                <table style="width: 100%; margin-top: 0;">
                    <tr>
                        <th style="font-size: 18px; text-align: center;">🛒 Ingredients</th>
                    </tr>
                    <tr><td style="padding: 20px;">
            """

            for ingredient, amount in recipe_detail.ingredients.items():
                recipe_table_builder += f"""
                    <div style="
                        display: flex; 
                        justify-content: space-between; 
                        margin: 10px 0; 
                        padding: 8px 12px; 
                        background: #f8f9fa; 
                        border-radius: 6px;
                        border-left: 4px solid #667eea;
                    ">
                        <b style="color: #2c3e50;">{ingredient}:</b>
                        <span style="color: #7f8c8d; font-weight: 500;">{amount}</span>
                    </div>
                """
            recipe_table_builder += "</td></tr></table>"
            st.markdown(recipe_table_builder, unsafe_allow_html=True)

        # Steps column
        with col3:
            steps_detail = dish.get_steps_detail()
            steps_table_builder = """
                <table style="width: 100%; margin-top: 0;">
                    <tr>
                        <th colspan="2" style="font-size: 18px; text-align: center;">👨‍🍳 Cooking Instructions</th>
                    </tr>
            """

            step_number = 1
            for step, detail in steps_detail.steps.items():
                steps_table_builder += f"""
                    <tr>
                        <td style="
                            width: 80px; 
                            vertical-align: top; 
                            text-align: center;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white;
                            font-weight: bold;
                            border-radius: 20px;
                            padding: 10px;
                        ">
                            {step_number}
                        </td>
                        <td style="
                            padding: 15px 20px; 
                            line-height: 1.6;
                            color: #2c3e50;
                        ">{detail}</td>
                    </tr>
                """
                step_number += 1

            steps_table_builder += "</table>"
            st.markdown(steps_table_builder, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error loading dish data: {str(e)}")
        st.info("There might be an issue with the database connection or data format.")

# Add footer with tips
st.markdown(
    """
    <div style="
        margin-top: 3rem; 
        padding: 2rem; 
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
        border-radius: 12px; 
        text-align: center;
    ">
        <h4 style="color: #2c3e50; margin-bottom: 1rem;">💡 Tips for Better Experience</h4>
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
            <div style="margin: 10px;">
                <strong>🖼️ Missing Images?</strong><br/>
                <span style="color: #7f8c8d;">Add images to images/dishes/ folder</span>
            </div>
            <div style="margin: 10px;">
                <strong>🔄 Database Issues?</strong><br/>
                <span style="color: #7f8c8d;">Run the cleanup script first</span>
            </div>
            <div style="margin: 10px;">
                <strong>📱 Mobile Friendly</strong><br/>
                <span style="color: #7f8c8d;">Works great on all devices</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
