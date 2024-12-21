from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Category, Location
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.db.models import Count, Q
from .utils.get_utils import get_filtered_tasks
from django.http import HttpResponseForbidden
from django.contrib import messages



# Home View
def Home(request):
    tasks = Task.objects.select_related('location').prefetch_related('categories')[:3]
    categories = Category.objects.annotate(task_count=Count('tasks')).order_by('-task_count')[:8]
    locations = Location.objects.annotate(task_count=Count('task')).order_by('-task_count')[:3]

    context = {
        "tasks": tasks,
        "categories": categories,
        "locations": locations,
    }
    return render(request, "tasks/home.html", context)



class TaskDetail(DetailView):
    model = Task
    template_name = 'tasks/job-single.html'
    context_object_name = "task"
    queryset = Task.objects.select_related('location').prefetch_related('categories')



class CategoryList(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'tasks/job-category.html'
    queryset = Category.objects.all().annotate(task_count=Count('tasks'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["locations"] = Location.objects.all().annotate(task_count=Count('task'))

        # Efficient prefetching and filtering
        tasks = Task.objects.prefetch_related('categories').select_related('location').select_related('employer__profile')

        # Get query parameters
        query_location_id = self.request.GET.get('location')
        query_category_id = self.request.GET.get('category')
        l_amount = self.request.GET.get('l_amount')
        g_amount = self.request.GET.get('g_amount')

        # Apply filters conditionally
        if query_location_id:
            tasks = tasks.filter(location_id=query_location_id)
        if query_category_id:
            tasks = tasks.filter(categories__id=query_category_id)
        if g_amount and l_amount:
            tasks = tasks.filter(Q(amount__range = (l_amount, g_amount)))

        context["tasks"] = tasks
        context["task_count"] = tasks.count()
        return context




def TaskSearch(request):
    categories = Category.objects.all()
    locations = Location.objects.all()
    tasks = Task.objects.none()
    context = {"categories": categories,
               "locations": locations, 
               "tasks": tasks}

    if request.method == "POST":
        category_id = request.POST.get("category")
        if category_id == '':
            category_id = 0

        location_id = request.POST.get("location")
        if location_id == '':
            location_id = 0
            
        search_keyword = request.POST.get("keyword").strip()

        if category_id or location_id or search_keyword:  # Only filter if at least one field is filled
            tasks = get_filtered_tasks(category_id, location_id, search_keyword)


            
    
    context["tasks"] = tasks

    return render(request, "tasks/job-search.html", context)





def CreateTask(request):
    if request.method == "POST":
        name = request.POST.get("task-name").strip()
        task_description = request.POST.get('task_description', '')
        amount = int(request.POST["amount"])
        location = Location.objects.get(id = request.POST["location"])
        extra_location_info = request.POST.get('extra_location_info', '')
        categories = request.POST.getlist('categories')
        employer =  request.user

        task = Task.objects.create(name=name, 
                            task_description=task_description,
                            amount = amount,
                            location = location,
                            extra_location_info = extra_location_info,
                            employer = employer)
        task.categories.set(categories)
        return redirect("task-detail", slug=task.slug)

    locations = Location.objects.all()
    categories = Category.objects.all()
    return render(request, "tasks/create-task.html", {"locations": locations, "categories": categories})
    





def UpdateTask(request, slug):
    task = get_object_or_404(Task, slug=slug)
    context = {
        "task":task
    }

    if request.user != task.employer:
        return HttpResponseForbidden("You are not allowed to update this task!")
    
    if request.method == "POST":
        #manually retrieve data from the form
        name = request.POST.get("task-name", task.name).strip()
        task_description = request.POST.get('task_description', task.task_description).strip()
        amount = request.POST.get("amount", task.amount)
        location_id = request.POST.get("location", task.location.id)
        extra_location_info = request.POST.get('extra_location_info', task.extra_location_info)
        category_ids = request.POST.getlist('categories')

        # check if name, amount, location and categories
        if not name or not amount or not location_id:
            messages.error(request, "Name, amount, location and Categories are required fields")
            return render(request, "tasks/update_task.html", context)
        
        try:
            amount = int(amount)
        except ValueError:
            messages.error(request, "Amount must be a valid integer")
            return render(request, "tasks/update_task.html", context)
        
        task.name = name
        task.task_description = task_description
        task.location = get_object_or_404(Location, id=location_id)
        task.amount = amount
        task.extra_location_info = extra_location_info
        task.categories.set(category_ids)

        task.save()

        messages.success(request, "Task updated successfully")
        return redirect("task-detail", slug=task.slug)
    else:
        task_categories = task.categories.all()
        locations = Location.objects.all()
        all_categories = Category.objects.all()

        context["task_categories"] = task_categories
        context["locations"] = locations
        context["all_categories"] = all_categories

        return render(request, 'tasks/update_task.html', context)
    


def DeleteTask(request, slug):
    task = get_object_or_404(Task, slug=slug)
    if request.method == "POST":
        task.delete()
        return redirect("home")
    return render (request, "tasks/job-single.html", {"task": task})