from dataclasses import dataclass
from typing import Optional


@dataclass
class UserProfile:
    age: int
    gender: str
    weight: float
    height: float
    activity_level: str
    goal: str
    training_frequency: int
    body_fat_percentage: Optional[float] = None


class ProteinIntakeAgent:

    ACTIVITY_MULTIPLIERS = {
        "sedentary": (0.8, 1.0),
        "light": (1.0, 1.2),
        "moderate": (1.2, 1.6),
        "active": (1.6, 2.2),
        "athlete": (1.8, 2.5),
    }

    GOAL_MULTIPLIERS = {
        "fat_loss": (1.6, 2.2),
        "muscle_gain": (1.6, 2.4),
        "maintenance": (1.2, 1.6),
        "recomposition": (1.8, 2.4),
    }

    LEAN_MASS_MULTIPLIER = (2.2, 3.0)

    def __init__(self, meals_per_day=4):
        self.meals_per_day = meals_per_day

    def calculate_lean_mass(self, weight, body_fat):
        return weight * (1 - body_fat / 100)

    def calculate_protein(self, profile):

        if profile.body_fat_percentage:
            base_weight = self.calculate_lean_mass(
                profile.weight,
                profile.body_fat_percentage
            )
            mult_min, mult_max = self.LEAN_MASS_MULTIPLIER
        else:
            base_weight = profile.weight
            activity = self.ACTIVITY_MULTIPLIERS[profile.activity_level]
            goal = self.GOAL_MULTIPLIERS[profile.goal]
            mult_min = max(activity[0], goal[0])
            mult_max = max(activity[1], goal[1])

        min_protein = base_weight * mult_min
        max_protein = base_weight * mult_max
        optimal = (min_protein + max_protein) / 2
        per_meal = optimal / self.meals_per_day

        return min_protein, optimal, max_protein, per_meal


# IMPORTANT: This runs the program
if __name__ == "__main__":

    user = UserProfile(
        age=26,
        gender="female",
        weight=55,
        height=160,
        activity_level="active",
        goal="fat_loss",
        training_frequency=5,
        body_fat_percentage=22
    )

    agent = ProteinIntakeAgent()

    min_p, opt_p, max_p, meal_p = agent.calculate_protein(user)

    print("\nProtein Intake Recommendation")
    print("-----------------------------")
    print("Minimum:", round(min_p, 1), "g/day")
    print("Optimal:", round(opt_p, 1), "g/day")
    print("Maximum:", round(max_p, 1), "g/day")
    print("Per Meal:", round(meal_p, 1), "g")
