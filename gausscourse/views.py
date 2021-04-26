from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Course
from .forms import FilterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def login(request):
    return render(request, 'gausscourse/login.html')

@login_required
def home(request):
    return render(request, 'gausscourse/home.html')

def index(request):
    """return HttpResponse("Hello, world. You're at the polls index.")"""
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            name_filter = form.cleaned_data['name_filter']
            course_list = Course.objects.filter(name__icontains = name_filter)
        else:
            course_list = Course.objects.all()
    else:
        form = FilterForm()
        course_list = Course.objects.all()
    context = {'course_list': course_list, 'form': form}
    return render(request, 'gausscourse/index.html', context)

def test(request):
    import matplotlib.pyplot as plt
    from matplotlib.pyplot import figure, title, bar
    import numpy as np
    import mpld3
    import astropy.visualization as astro
    from scipy.stats import norm

  # Play around Bar (fig_html)
    mpl_figure = figure(figsize=(9, 4))
    xvalues = range(100)  # the x locations for the groups
    yvalues = np.random.random_sample(100)
    width = 0.9  # the width of the bars
    title('Еволюційні обчислення')
    bar(xvalues, yvalues, width)
    fig_html = mpld3.fig_to_html(mpl_figure)
  # End Bar example

  # Play around Histogram (fig2_html)
    # example data
    mu, sigma = 85, 10 # mean and standard deviation of distribution
    x = mu + sigma * np.random.randn(110)
    x = x[(x > 0) & (x < 100)] # truncate to a reasonable range
    # aproximate by normal distribution
    mu_aprox, sigma_aprox = norm.fit(x)
    #num_bins = round( x.size / 5 )
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.set_xlim(45, 100)
    # the histogram of the data
    #n, bins, patches = ax.hist(x, num_bins, width=width, density=True)
    #n, bins, patches = ax.hist(x, density=True)
    bins = 22 # 'scott', 'freedman', 'knuth', 'blocks'
    astro.hist(x, bins=bins, ax=ax, histtype='stepfilled', density=True)
    # add a 'best fit' line
    x2 = np.arange(35, 110)
    y2 = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
        np.exp(-0.5 * (1 / sigma * (x2 - mu))**2))
    y3 = ((1 / (np.sqrt(2 * np.pi) * sigma_aprox)) *
        np.exp(-0.5 * (1 / sigma_aprox * (x2 - mu_aprox))**2))
    ax.plot(x2, y2, ls=':', color='red')
    ax.plot(x2, y3, ls='-', lw=3.0, color='green')
    ax.set_xlabel('Grade')
    ax.set_ylabel('Density of students grades')
    ax.set_title(f'Test Histogram: N={x.size}, Bins={bins}, \
        \u03bc={mu}({round(mu_aprox, 1)}), \u03C3={sigma}({round(sigma_aprox, 1)})')
    fig2_html = mpld3.fig_to_html(fig)
  # End Bar example

    """return HttpResponse("Hello, world. You're at the polls index.")"""
    course_list = [{'name':'name', 'start_date':'start_date', "finish_date":"finish_date" },
                   {'name':'sfjh', 'start_date':'rrrrrrrrrr', "finish_date":"dfjdjdyjdyj" },
                   {'name':'gjfj', 'start_date':'ggggggffff', "finish_date":"cvmn4565676" }]
    context = {'figure': fig_html, 'figure2': fig2_html, 'course_list': course_list}
    return render(request, 'gausscourse/test.html', context)
