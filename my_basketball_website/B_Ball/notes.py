

### Built-In `UpdateView`:
#### `TeamUpdateView(UpdateView)`:
#**Class**: `UpdateView` (a subclass of `View`)
#**Handles GET and POST**: Automatically handles GET and POST requests.
"""- **URL Pattern**: Relies on the URL pattern to provide the `pk`.
- **Object Retrieval**: Fetches the object based on the `pk` provided in the URL.
- **Template Rendering**: Uses `template_name` to render the form with the object's current data.
- **Form Handling**: Automatically binds data to the form and checks for validity.
- **Redirection**: Uses `success_url` for redirection after successful update.
- **Custom Logic**: Can override methods like `post`, `form_valid`, and `form_invalid` to add custom logic.
"""

from django.views.generic.edit import UpdateView
from .models import Team
from .forms import TeamForm
from django.contrib import messages

class TeamUpdateView(UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'update_team.html'
    success_url = '/teams/'  # URL to redirect to after a successful update

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(request, "Team Updated Successfully :)")
            return redirect('team-detail', pk=self.object.pk)
        return self.form_invalid(form)


### Custom View:
#### `TeamUpdate(View)`:
"""- **Class**: `View` (base class)
- **Manual Handling**: Manually handles GET and POST requests.
- **Object Retrieval**: Manually retrieves the object using `get_object_or_404`.
- **Template Rendering**: Manually renders the template and passes the context.
- **Form Handling**: Manually binds data to the form and checks for validity.
- **Redirection and Messages**: Manually handles redirection and success messages."""



from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Team
from .forms import TeamForm

class TeamUpdate(View):
    # Handle GET requests to fetch the form with current team details
    def get(self, request, pk):
        update_teams = get_object_or_404(Team, pk=pk)
        form = TeamForm(request.POST or None, instance=update_teams)
        return render(request, 'update_team.html', {'form': form, 'update_teams': update_teams})

    # Handle POST requests to update team details
    def post(self, request, pk):
        update_teams = get_object_or_404(Team, pk=pk)
        form = TeamForm(request.POST, request.FILES, instance=update_teams)
        if form.is_valid():
            form.save()
            messages.success(request, "Team Updated Successfully :)")
            return redirect('team-detail', pk=pk)
        return render(request, 'update_team.html', {'form': form, 'update_teams': update_teams})

### Key Differences:

"""1. **Automatic Handling vs. Manual Handling**:
   - `UpdateView` automatically handles GET and POST requests, object retrieval, form binding, and validation.
   - The custom view requires you to manually implement these steps.

2. **Customizability**:
   - Both approaches are customizable, but `UpdateView` makes it easier to add custom logic by overriding built-in methods like `post`, `form_valid`, or `form_invalid`.

3. **Simplicity vs. Control**:
   - `UpdateView` simplifies common patterns, reducing boilerplate code.
   - Custom views give you more control and are useful for complex scenarios requiring specific logic, such as custom validations or file uploads.

### Summary:
- **Use `UpdateView`**: For standard update operations with minimal customization.
- **Use Custom View**: When you need specific logic that `UpdateView` cannot handle by default, such as handling file uploads or setting custom success messages.

In your case, since you need to handle file uploads and add success messages, you can use `UpdateView` and override the `post` method to include your custom logic.
"""