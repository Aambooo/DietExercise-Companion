import streamlit as st
from algorithm.fuzzy_logic import FuzzyLogic
import sqlalchemy
from models.eat import *
from models.fit import *
import base64
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path


def safe_create_dish(conn, dish_id):
    """
    Safely create a Dish object with error handling and local image loading
    """
    try:
        dish_result = conn.execute(
            "SELECT * FROM Dish WHERE Id = :id", {"id": dish_id}
        ).fetchone()

        if dish_result is None:
            st.warning(f"⚠️ Dish with ID '{dish_id}' not found in database")
            return create_placeholder_dish(dish_id)

        dish = Dish(*dish_result)

        # If image is None or empty, try to load from local file system
        if dish.image is None or (
            isinstance(dish.image, bytes) and len(dish.image) == 0
        ):
            dish.image = load_local_image(dish_id)

        return dish

    except Exception as e:
        st.error(f"❌ Error loading dish {dish_id}: {str(e)}")
        return create_placeholder_dish(dish_id)


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

        # If no local image found, return None
        return None

    except Exception as e:
        print(f"Error loading local image for dish {dish_id}: {e}")
        return None


def create_placeholder_dish(dish_id):
    """
    Create a placeholder dish when the actual dish is not found
    """
    return Dish(
        id=dish_id,
        name=f"Dish {dish_id} (Not Available)",
        image=None,
        nutrition="100;10;5;8",  # Default nutrition values
        recipe="Placeholder ingredient: 1 serving",
        steps="Recipe not available",
    )


def display_dish_image(dish, fallback_width="90%"):
    """
    Display dish image with proper fallback handling
    """
    if dish.image is not None and len(dish.image) > 0:
        try:
            # Try to display the image
            image_b64 = base64.b64encode(dish.image).decode("utf-8")
            st.markdown(
                f"""
                <p style="text-align: right">
                    <img src="data:image/jpeg;base64,{image_b64}" width="{fallback_width}" style="border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                </p>
                """,
                unsafe_allow_html=True,
            )
            return True
        except Exception as e:
            print(f"Error displaying image for dish {dish.name}: {e}")

    # Fallback: Show placeholder
    st.markdown(
        f"""
        <div style="text-align: center; padding: 50px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 10px; margin: 20px; border: 2px dashed #ccc;">
            <div style="font-size: 48px; margin-bottom: 10px;">🍽️</div>
            <p style="color: #666; font-size: 14px; margin: 0;">Image not available</p>
            <p style="color: #999; font-size: 12px; margin: 0;">for {dish.name}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return False


st.set_page_config(page_title="DietExercise Companion")

# A workaround using st.markdown() to apply some style sheets to the page.
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
            .css-wjbhl0, .css-hied5v {{
            padding-top: 2rem;
            padding-bottom: 0.25rem;
            }}
            
            /* Custom styles for better image display */
            .dish-image-container {{
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin: 20px 0;
            }}
        </style>
        """,
    unsafe_allow_html=True,
)

# Centered header without logo - full width and flexible
st.markdown(
    """
    <div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem;">
        <h1 style="
            color: #2E86AB; 
            font-size: 3.5rem; 
            font-weight: bold; 
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        ">Your DietExercise Companion</h1>
        <p style="
            color: #666; 
            font-size: 1.5rem; 
            font-style: italic; 
            margin-top: 0;
            font-weight: 300;
        ">Know Your Workout & Nutritional Criteria</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# A flag to show whether the page is loaded the first time or not
is_first_load = True

# Input fields in the sidebar
with st.sidebar:
    st.title("Body Parameters")

    # A workaround using st.session_state and callback to keep input value during navigating through other pages
    if "page1" not in st.session_state:
        st.session_state.page1 = {
            "is_first_load": True,
            "sex": 0,
            "height": 175.0,
            "weight": 80.0,
            "stage": 0,
        }

    for k, v in st.session_state.items():
        st.session_state[k] = v

    def submit_sex():
        st.session_state.page1["sex"] = (
            0 if st.session_state.sex_input_value == "Male" else 1
        )

    def submit_height():
        st.session_state.page1["height"] = st.session_state.height_input_value

    def submit_weight():
        st.session_state.page1["weight"] = st.session_state.weight_input_value

    def submit_stage():
        st.session_state.page1["stage"] = (
            0 if st.session_state.stage_input_value == "Yes, I'm a beginner" else 1
        )

    sex_input = st.radio(
        "**What's your sex?**",
        ("Male", "Female"),
        key="sex_input_value",
        on_change=submit_sex,
    )

    height_input = st.number_input(
        "**What's your height (in centimeters)?**",
        key="height_input_value",
        min_value=130.0,
        max_value=220.0,
        step=0.1,
        on_change=submit_height,
    )

    weight_input = st.number_input(
        "**What's your weight (in kilograms)?**",
        key="weight_input_value",
        min_value=30.0,
        max_value=150.0,
        step=0.1,
        on_change=submit_weight,
    )

    stage_input = st.selectbox(
        "**Are you new to weight loss?**",
        ("Yes, I'm a beginner", "No, I'm an intermediate"),
        key="stage_input_value",
        on_change=submit_stage,
    )

    # Align the buttons in the sidebar
    col1, col2, col3 = st.columns([1, 0.5, 0.85])
    with col1:
        if st.button("Submit"):
            st.session_state.page1["is_first_load"] = False
    with col3:
        if st.button("Reset"):
            st.session_state.page1["is_first_load"] = True

if not st.session_state.page1["is_first_load"]:
    # Perform Fuzzy Logic to determine the body state
    fuzzy_logic = FuzzyLogic()
    fuzzy_logic.do_fuzzification_of_height(
        round(st.session_state.page1["height"], 2), st.session_state.page1["sex"]
    )
    fuzzy_logic.do_fuzzification_of_weight(
        round(st.session_state.page1["weight"], 2), st.session_state.page1["sex"]
    )
    fuzzy_logic.do_fuzzy_inference()
    body = fuzzy_logic.do_defuzzification_of_body()

    # Conclusion
    body_result = ""
    match body:
        case 2:
            body_result = "overweight"
        case 3:
            body_result = "pre-obese"
        case 4:
            body_result = "obese"

    if body == 0:
        st.subheader("You are thin! You should gain weight instead of losing weight!")
    elif body == 1:
        st.subheader("You are in shape! Keep going! :sunglasses:")
    else:
        st.subheader(
            f"You are {body_result}! To lose weight, you can follow this guide:"
        )

        # Diet plan overview
        st.subheader("A. Diet")
        st.write(
            "**Carbohydrates** or ***carbs*** (including *sugars*, *starch*, and *cellulose*) are the main energy source of the human diet. To lose weight, you need to eat fewer carbs."
        )
        st.markdown(
            """
            In this diet plan, each week will consist of 3 different types of eating days:
            <ul style="padding-left: 2rem">
            <li><b>Low Carb Days</b> (below <b>26%</b> of total energy intake) - <b>3</b> days per week</li>
            <li><b>Moderate Carb Days</b> (between <b>26%</b> and <b>45%</b> of total energy intake) - <b>3</b> days per week</li>
            <li><b>High Carb Days</b> (above <b>45%</b> of total energy intake) - <b>1</b> day per week</li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

        # Get and display diet plan from the database
        st.markdown("### 📊 Your Personalized Diet Plans")
        st.markdown("---")

        # Create tabs for better organization
        tab1, tab2, tab3 = st.tabs(
            ["🥗 Low Carb Diet", "🍽️ Moderate Carb Diet", "🍕 High Carb Diet"]
        )

        matplotlib.rcParams.update({"font.size": 8})
        label = ["Carbs", "Fat", "Protein"]
        colors = ["#F7D300", "#38BC56", "#D35454"]
        engine = sqlalchemy.create_engine(
            "sqlite:///database/dietexercise_companion.db"
        )

        with engine.connect() as conn:
            # Get standard calories each day for the user
            sc_result = conn.execute(
                "SELECT * FROM StandardCalories WHERE Stage = :stage AND Body = :body AND Sex = :sex",
                {
                    "stage": st.session_state.page1["stage"],
                    "body": body,
                    "sex": st.session_state.page1["sex"],
                },
            ).fetchone()

            if sc_result is None:
                st.error(
                    "❌ No standard calories found for your profile. Please check the database."
                )
                st.stop()

            standard_calories = StandardCalories(*sc_result)

            # LOW CARB TAB
            with tab1:
                # Get low carb diet
                lc_result = conn.execute(
                    "SELECT * FROM LowCarb WHERE Calories = :calories",
                    {"calories": standard_calories.low_carb},
                ).fetchone()

                if lc_result is None:
                    st.error(
                        f"❌ Low carb diet plan not found for {standard_calories.low_carb} calories"
                    )
                else:
                    low_carb_diet = Diet(*lc_result)
                    low_carb_nutrition_detail = low_carb_diet.get_nutrition_detail()

                    # Create two columns for nutrition info and chart
                    col1, col2 = st.columns([1, 1])

                    with col1:
                        st.markdown("#### 📈 Nutrition Summary")
                        st.markdown(
                            f"""
                        **Calories:** {round(low_carb_nutrition_detail.calories)} cal  
                        **Carbs:** {low_carb_nutrition_detail.carbs} g  
                        **Fat:** {low_carb_nutrition_detail.fat} g  
                        **Protein:** {low_carb_nutrition_detail.protein} g
                        """
                        )

                    with col2:
                        # Create pie chart
                        low_carb_data = [
                            low_carb_nutrition_detail.get_carbs_percentage(),
                            low_carb_nutrition_detail.get_fat_percentage(),
                            low_carb_nutrition_detail.get_protein_percentage(),
                        ]
                        low_carb_fig, low_carb_ax = plt.subplots(figsize=(3, 3))
                        low_carb_ax.pie(
                            low_carb_data,
                            labels=label,
                            colors=colors,
                            explode=(0.1, 0.05, 0.05),
                            autopct="%1.1f%%",
                            startangle=90,
                        )
                        low_carb_ax.set_title(
                            "Calorie Distribution", fontsize=12, pad=20
                        )
                        st.pyplot(low_carb_fig)

                    # Meal plan display - SAFER VERSION
                    st.markdown("#### 🍽️ Daily Meal Plan")

                    low_carb_breakfast_detail = low_carb_diet.get_breakfast_detail()
                    low_carb_lunch_detail = low_carb_diet.get_lunch_detail()
                    low_carb_dinner_detail = low_carb_diet.get_dinner_detail()

                    # Get dish information SAFELY
                    dishes_info = {}
                    for meal_type, meal_detail in [
                        ("breakfast", low_carb_breakfast_detail),
                        ("lunch", low_carb_lunch_detail),
                        ("dinner", low_carb_dinner_detail),
                    ]:
                        dish1 = safe_create_dish(conn, meal_detail.id1)
                        dish2 = safe_create_dish(conn, meal_detail.id2)

                        dishes_info[meal_type] = {
                            "detail": meal_detail,
                            "dish1": dish1,
                            "dish2": dish2,
                        }

                    # Display meals in organized format
                    for meal_name, meal_info in [
                        ("Breakfast", dishes_info["breakfast"]),
                        ("Lunch", dishes_info["lunch"]),
                        ("Dinner", dishes_info["dinner"]),
                    ]:
                        st.markdown(
                            f"**{meal_name}** - {meal_info['detail'].calories} calories"
                        )

                        meal_col1, meal_col2 = st.columns(2)
                        with meal_col1:
                            st.markdown(
                                f"""
                            **{meal_info['dish1'].name}**  
                            Serving: {meal_info['detail'].amount1}
                            """
                            )

                        with meal_col2:
                            st.markdown(
                                f"""
                            **{meal_info['dish2'].name}**  
                            Serving: {meal_info['detail'].amount2}
                           """
                            )
                        st.markdown("---")

            # Continue with similar structure for MODERATE CARB and HIGH CARB tabs...
            # (The rest of the code remains the same as your original)

        # Add explanation about diet cycling
        st.markdown(
            """
        #### 📅 How to Use These Plans
        You may structure these days in any preferred manner. I suggest keeping the high carb day for special occasions. 
        That way you can attend family functions, or eat out with friends, and indulge a little more than normal.

        **Weekly Structure Recommendation:**
        - **3 days**: Low Carb Diet
        - **3 days**: Moderate Carb Diet  
        - **1 day**: High Carb Diet
        """
        )

        # Workout plan (rest of your existing code continues...)
        st.subheader("B. Workout")

        # Continue with the rest of your existing workout code...
        # (I've truncated this for brevity, but it continues as in your original file)
