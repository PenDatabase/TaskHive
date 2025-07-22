import os
import django
import random
from faker import Faker

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WORKit.settings')
django.setup()

from users.models import WORKitUser as User
from Tasks.models import Category, Location, Task

# Initialize Faker
fake = Faker()

def create_users(n):
    """Create n users."""
    users = []
    for _ in range(n):
        username = fake.unique.user_name()
        user = User.objects.create_user(
            username=username,
            email=fake.email(),
            password='password123',
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        users.append(user)
    print(f"Created {n} users.")
    return users

def create_categories(n):
    """Create n categories."""
    categories = []
    for _ in range(n):
        category = Category.objects.create(
            name=fake.unique.word().capitalize(),
            description=fake.text(max_nb_chars=200)
        )
        categories.append(category)
        print(f"Created {category.name} category.")
    print(f"Created {n} categories.")
    return categories

def create_locations(n):
    """Create n locations."""
    locations = []
    for _ in range(n):
        location = Location.objects.create(
            place=fake.unique.city()
        )
        locations.append(location)
        print(f"Created {location.place} location.")
    print(f"Created {n} locations.")
    return locations

def create_tasks(n, users, categories, locations):
    """Create n tasks."""
    for _ in range(n):
        name = fake.sentence(nb_words=5).rstrip('.').title()
        employer = random.choice(users)
        location = random.choice(locations)
        task = Task.objects.create(
            name=name,
            task_description=fake.text(max_nb_chars=500),
            amount=random.randint(100, 5000),
            location=location,
            extra_location_info=fake.address(),
            employer=employer
        )
        # Assign random categories to the task
        task.categories.set(random.sample(categories, random.randint(1, 5)))
        task.save()
        print(f"Created {task.name} task")
    print(f"Created {n} tasks.")

def main():
    users = create_users(10)
    categories = create_categories(5)
    locations = create_locations(15)
    create_tasks(1000, users, categories, locations)

if __name__ == "__main__":
    main()
