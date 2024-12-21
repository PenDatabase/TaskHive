# utils/search_utils.py

from django.db.models import Q, Case, When, Value, IntegerField
from ..models import Task
                


def get_filtered_tasks(category_id, location_id, search_keyword):
    filters = Q()  # Initialize an empty filter condition
    
    # Add filters and score increments
    if category_id:
        filters |= Q(categories__id=category_id)

    if location_id:
        filters |= Q(location__id=location_id)
        
    if search_keyword:
        # Apply the search filter for name
        filters |= Q(Q(name__icontains=search_keyword) | Q(task_description__icontains=search_keyword)) 

        
    

    # Filter tasks and order them by the score
    tasks = Task.objects.filter(filters).annotate(
            match_score=(
                Case(When(categories__id=category_id, then=Value(3)), default=Value(0), output_field=IntegerField()) +

                Case(When(location__id=location_id, then=Value(3)), default=Value(0), output_field=IntegerField()) +

                Case(When(name__icontains=search_keyword, then=Value(5)), default=Value(0), output_field=IntegerField()) +

                Case(When(task_description__icontains=search_keyword, then=Value(1)), default=Value(0), output_field=IntegerField())
             )
        ).order_by('-match_score').distinct()  # Sort by score in descending order

    return tasks