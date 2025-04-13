
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms, models


@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = forms.BlogPostForm(request.POST)
        if form.is_valid():
            parent_page = models.BlogIndexPage.objects.first()
            blog_post = form.save(commit=False)

            # Manually handle StreamField data
            if 'body' in request.POST:
                try:
                    blog_post.body = json.loads(request.POST['body'])
                except json.JSONDecodeError:
                    form.add_error('body', 'Invalid JSON format')
                    return render(request, 'blog/create_post.html', {'form': form})

            blog_post = parent_page.add_child(instance=blog_post)
            blog_post.save_revision().publish()
            return redirect('blog_post_detail', slug=blog_post.slug)
    else:
        form = forms.BlogPostForm()
    return render(request, 'blog/create_post.html', {'form': form})
