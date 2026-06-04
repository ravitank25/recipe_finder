import requests
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import db
from models.favorite import Favorite

recipe_bp = Blueprint(
    "recipe",
    __name__
)

@recipe_bp.route("/")
def home():
    query = request.args.get("search", "").strip()
    meals = []
    error = None

    try:
        if query:
            url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={query}"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if data.get("meals"):
                meals = data["meals"]
            else:
                error = f"No recipes found for '{query}'"
        else:
            # Get random meals on homepage
            url = "https://www.themealdb.com/api/json/v1/1/random.php"
            for _ in range(9):
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("meals"):
                        meals.extend(data["meals"])
    except requests.exceptions.RequestException:
        error = "Failed to fetch recipes. Please try again."

    # Get user's favorites
    user_favorite_ids = []
    if current_user.is_authenticated:
        user_favorites = Favorite.query.filter_by(user_id=current_user.id).all()
        user_favorite_ids = [f.recipe_id for f in user_favorites]

    return render_template(
        "index.html",
        meals=meals,
        error=error,
        user_favorite_ids=user_favorite_ids
    )


@recipe_bp.route("/recipe/<meal_id>")
def recipe_detail(meal_id):
    try:
        url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if data.get("meals"):
            meal = data["meals"][0]
            
            # Get user's favorites
            is_favorite = False
            if current_user.is_authenticated:
                favorite = Favorite.query.filter_by(
                    user_id=current_user.id,
                    recipe_id=meal_id
                ).first()
                is_favorite = favorite is not None
            
            return render_template(
                "recipe_detail.html",
                meal=meal,
                is_favorite=is_favorite
            )
    except requests.exceptions.RequestException:
        pass
    
    return render_template("recipe_detail.html", error="Recipe not found")


@recipe_bp.route("/favorites")
@login_required
def favorites():
    user_favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    meals = []
    
    try:
        for favorite in user_favorites:
            url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={favorite.recipe_id}"
            response = requests.get(url, timeout=5)
            data = response.json()
            if data.get("meals"):
                meals.append(data["meals"][0])
    except requests.exceptions.RequestException:
        pass
    
    return render_template("favorites.html", meals=meals)


@recipe_bp.route("/add-favorite/<meal_id>", methods=["POST"])
@login_required
def add_favorite(meal_id):
    try:
        # Get meal details
        url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if data.get("meals"):
            meal = data["meals"][0]
            
            # Check if already favorited
            existing = Favorite.query.filter_by(
                user_id=current_user.id,
                recipe_id=meal_id
            ).first()
            
            if not existing:
                favorite = Favorite(
                    user_id=current_user.id,
                    recipe_id=meal_id,
                    recipe_name=meal.get("strMeal", "Unknown")
                )
                db.session.add(favorite)
                db.session.commit()
                return jsonify({"success": True, "message": "Added to favorites"})
            else:
                return jsonify({"success": False, "message": "Already in favorites"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@recipe_bp.route("/remove-favorite/<meal_id>", methods=["POST"])
@login_required
def remove_favorite(meal_id):
    try:
        favorite = Favorite.query.filter_by(
            user_id=current_user.id,
            recipe_id=meal_id
        ).first()
        
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({"success": True, "message": "Removed from favorites"})
        else:
            return jsonify({"success": False, "message": "Not in favorites"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})