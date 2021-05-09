from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Course
from .models import CourseGroup
from .models import Grade
from .forms import FilterForm, GradeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.db import connection

@login_required
def home(request):
    user_grades = list(Grade.objects.filter( user=request.user ).all())
    context = {'user_grades' : user_grades}
    return render(request, 'gausscourse/home.html', context)

def courses_grades_count():
    with connection.cursor() as cursor:
        query = """SELECT gausscourse_course.id, gausscourse_course.name,
                gausscourse_course.is_public, COUNT(gausscourse_grade.grade)
                FROM gausscourse_course
                LEFT JOIN gausscourse_coursegroup
                ON gausscourse_course.id = gausscourse_coursegroup.course_id
                LEFT JOIN gausscourse_grade
                ON gausscourse_coursegroup.id = gausscourse_grade.course_group_id
                GROUP BY gausscourse_course.id"""
        cursor.execute(query)
        res_list = cursor.fetchall()
    return res_list

def course_detail(request, course_id=1):
    # essentially, mirror GET behavior exactly on POST
    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    # Prepare data grades for FIG
    test_list = courses_grades_count()
    course = Course.objects.get(id=course_id)
    course_groups = list(CourseGroup.objects.filter( course_id = course.id).all())
    crs_grp_ids = [] # example list [7, ...]
    group_name = {}  # example dict {0:'all', 7:'other group', ...}
    grds = {}        # example dict {0:[56, 99, 88, 77, 82, 66, 78, 75], 7:[56, 99, 88, 77], ...}
    group_name[0] = 'all'
    grds[0] = []
    for crs_grp in course_groups:
        crs_grp_ids.append(crs_grp.id)
        group_name[crs_grp.id] = crs_grp.group.name
        grds[crs_grp.id] = []
        #grd = list(Grade.objects.filter( course_group_id = crs_grp.id).all())
    grades = list(Grade.objects.filter( course_group_id__in=crs_grp_ids).all())
    for gr in grades:
        grds[0].append(gr.grade)
        grds[gr.course_group_id].append(gr.grade)
    # END Prepare data grades for FIG

    user_grade = (list(Grade.objects.filter( course_group_id__in=crs_grp_ids, user=request.user ).all()) or [None])[0]
    fig_dict = get_fig_dict(grds, group_name)
    context = {'course' : course,
            'course_groups' : course_groups,
            'crs_grp_ids' : crs_grp_ids,
            'group_name' : group_name,
            'grds' : grds,
            'fig_dict' : fig_dict,
            'user_grade' : user_grade}
    return render(request, 'gausscourse/course_detail.html', context)

def get_fig_dict(grd_dict, group_name):
    import matplotlib.pyplot as plt
    import numpy as np
    import mpld3 as mpld3
    from scipy import stats

    x = []              # all grades in one 2-dem list
    label = []          # group name list
    num_bins = 11
    # Start: Set fake data for grades if you have few grades
    grades_count_min = 4
    grades_generate_number = 22
    grades_gen_mu = 88.0
    grades_gen_sigma = 7.0
    x0 = np.array([])
    for grd in grd_dict:
        xl = np.array(grd_dict[grd])
        xl = xl[(xl > 0) & (xl < 100)]
        if xl.size < grades_count_min:
            xl = grades_gen_mu + grades_gen_sigma * np.random.randn(grades_generate_number)
            xl = xl[(xl > 0) & (xl < 100)]
        x.append(xl)
        label.append(group_name[grd])
        if grd != 0:
            x0 = np.concatenate([x0, xl])
    if x0.size < grades_count_min:
        x0 = grades_gen_mu + grades_gen_sigma * np.random.randn(grades_generate_number)
        x0 = x0[(x0 > 0) & (x0 < 100)]
    x[0] = x0
    # Stop: Set fake data...

    # Fitting data to normal and beta distribution (for all groups)
    x4line = np.arange(0, 100, 0.2)
    mu, sigma = stats.norm.fit(x[0])
    pdf_norm = stats.norm.pdf(x4line, mu, sigma)
    params = stats.beta.fit(x[0], floc=0, fscale=100)
    pdf_beta = stats.beta.pdf(x4line, *params)

    fig, ax = plt.subplots(figsize=(11, 4))
    fig.subplots_adjust(right=0.7)
    ax.set_xlim(55, 100)
    ax.set_xlabel('Grade')
    ax.set_ylabel('Density of students grades')
    ax.set_title(f'Test Histogram \u03bc={round(mu, 1)}, \u03C3={round(sigma, 1)} \
        N={x[0].size}, Beta Params: \
        {round(params[0],1), round(params[1],1), round(params[2],1), round(params[3],1)}')
    ax.grid(True, alpha=0.3)

    # generate histogram at temp plot, bins->X n->Y for draw it as line (fill_between)
    fig_temp, ax_temp = plt.subplots()
    n, bins, patches = ax_temp.hist(x, num_bins, density=True, histtype='bar', label=label)

    hist_number = len(label)
    i = -1
    for n_cur in n:
        i = i + 1
        if (n.ndim == 1) or (i == 0):
            l, = ax.plot(x4line, pdf_norm, '--', lw=3.0, label='Норм Розподіл для всіх')
            ax.plot(x4line, pdf_beta, ':', lw=3.0, color=l.get_color(), label='Бета Розподіл для всіх')
            ax.legend(['Norm','Beta'])
            if (n.ndim == 1):
                n_new = np.concatenate([n, [0]])
            else:
                n_new = np.concatenate([n_cur, [0]])
        else:
            mu, sigma = stats.norm.fit(x[i])
            pdf_norm = stats.norm.pdf(x4line, mu, sigma)
            l, = ax.plot(x4line, pdf_norm, '--', lw=3.0, label='Норм Розподіл для '+label[i])
            n_new = np.concatenate([n_cur, [0]])
        x_array = np.array([bins[0]])
        y_array = np.array([0.0])
        for xi, xii, yi in zip(bins, bins[1:], n_new):
            step = (xii - xi) / hist_number
            delta = step / 20.0
            #delta = 0.0
            step = step - 2 * delta
            xi_n = xi + step * i
            xi_0 = xi + step * (i + 1)
            x_array = np.concatenate([x_array, [xi_n + delta]])
            y_array = np.concatenate([y_array, [0.0]])
            x_array = np.concatenate([x_array, [xi_n + delta]])
            y_array = np.concatenate([y_array, [yi]])
            x_array = np.concatenate([x_array, [xi_0 - delta]])
            y_array = np.concatenate([y_array, [yi]])
            x_array = np.concatenate([x_array, [xi_0 - delta]])
            y_array = np.concatenate([y_array, [0.0]])
        ax.fill_between(x_array, y_array, color=l.get_color(), alpha=0.7, label='Гістограма для '+label[i])
        if (n.ndim == 1):
            break

    # define interactive legend
    handles, labels = ax.get_legend_handles_labels() # return lines and labels
    inter_leg = mpld3.plugins.InteractiveLegendPlugin(handles,labels,alpha_unsel=0.1,alpha_over=1.5,start_visible=True)
    mpld3.plugins.connect(fig, inter_leg)

    fig_dict = {}
    fig_dict[0] = mpld3.fig_to_html(fig)
    return fig_dict

class CourseIndexView(ListView):
    context_object_name = 'course_list'
    template_name='gausscourse/index.html'

    def get_context_data(self, **kwargs):
        context = super(CourseIndexView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = FilterForm(self.request.GET)
        sortBy = '-name'
        if 'sort' in self.request.GET:
            if self.request.GET['sort'] == 'name':
                sortBy = '-name'
            else:
                sortBy = 'name'
        context['sort'] = sortBy
        test_list = courses_grades_count()
        context['test_list'] = test_list
        return context

    def get_queryset(self):
        if self.request.method == 'GET':
            sortBy = 'name'
            if 'sort' in self.request.GET:
                sortBy = self.request.GET['sort']
            form = FilterForm(self.request.GET)
            if form.is_valid():
                name_filter = form.cleaned_data['name_filter']
                return_obj = Course.objects.filter(name__icontains = name_filter).order_by(sortBy)
            else:
                return_obj = Course.objects.all()
        else:
            return_obj = Course.objects.all()
        return_list = list(return_obj)
        return return_list

def test(request):
    import matplotlib.pyplot as plt
    from matplotlib.pyplot import figure, title, bar
    import numpy as np
    import mpld3
    import astropy.visualization as astro
    from scipy.stats import norm
    from scipy import stats

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
    # 123 Компютерна інженерія 2020 3-курс 1-семестр
    #x = np.array([100.5, 98.75, 98.75, 97.625, 96.625, 96.375, 96.375, 96.0, 95.875, 95.875, 94.75, 94.625, 94.625, 94.5, 94.5, 93.875, 93.375, 93.0, 92.5, 92.5, 92.375, 92.375, 92.125, 92.0, 92.0, 91.875, 91.75, 91.625, 91.125, 90.375, 90.375, 89.75, 89.625, 89.625, 89.375, 87.75, 86.875, 86.5, 86.0, 85.875, 85.125, 84.75, 84.75, 84.75, 84.625, 83.5, 82.75, 81.125, 78.875, 78.125, 76.375, 74.75, 73.5, 72.5, 68.0])
    # 061 Журналістика 2020 3-курс 1-семестр
    #x = np.array([102.0,100.5,100.0,99.75,99.5,99.25,99.0,98.75,98.25,98.25,98.25,98.0,97.75,97.25,97.25,97.25,97.0,96.75,96.75,95.75,95.75,95.75,95.5,95.5,95.5,95.25,95.0,95.0,95.0,95.0,94.75,94.5,94.5,94.25,94.0,93.75,93.75,93.25,93.25,93.25,93.25,93.25,93.0,92.75,92.5,91.5,91.5,91.25,91.25,90.5,89.75,89.5,89.5,89.0,88.25,88.25,88.0,87.5,87.0,87.0,85.75,85.5,84.25,84.25,83.5,83,82.75,81.75,81.75,81.75,81.75,81.5,81.0,80.5,80.5,80.0,80.0,79.75,78.5,75.0,74.5,73.25,73.25,73.0,71.5,71.5,71.25,71.0,65.75,64.0])
    # 032 Історія та археологія 2020 3-курс 1-семестр Без додаткових балів
    #x = np.array([98.0,96.88,96.25,96.25,95.37,96.5,95.0,94.5,95.5,97.0,95.25,97.63,97.33,96.25,96.13,97.0,95.33,96.75,94.75,96.5,95.0,94.875,94.5,92.44,94.38,92.75,94.63,95.29,95.25,95.22,95.0,91.88,92.71,94.62,94.43,94.43,93.33,93.75,90.25,93.62,92.12,93.5,93.33,93.33,91.75,92.86,92.71,91.86,91.63,91.56,91.5,91.33,89.88,90.63,90.62,90.57,90.25,90.25,90.12,89.75,89.11,88.88,88.63,88.0,87.75,87.43,87.38,86.75,86.375,83.87,85.62,85.25,83.71,85.0,85.0,84.38,84,83.75,83.63,83.5,83.29,82.5,81.13,80.88,80.11,79.56,79.14,79.0,78.71,78.22,76.14,75.89,73.57,71.5,66.29,60.88])
    # 104 Фізика та астрономія (Фізфак) 2020 3-курс 1-семестр Без додаткових балів
    x = np.array([99.13,99.0,95.38,97.88,97.75,97.63,97.5,97.38,96.5,96.25,96.0,95.0,94.75,94.5,94.38,93.75,93.5,93.38,93.25,93.25,93.0,92.13,92.0,86.13,91.0,90.38,88.38,88.63,89.25,88.75,88.25,88.13,87.63,87.0,86.63,86.63,86.38,86.13,85.5,84.63,82.5,81.88,81.13,81.0,78.63,76.75,76.75,76.13,75.13,73.5,73.25,73.0,71.38,63.88])

    # some random variates drawn from a beta distribution
    # rvs = stats.beta.rvs(2, 5, loc=100, scale=50, size=102)
    # estimate distribution parameters, in this case (a, b, loc, scale)
    x_new = (x - 0) / 1.0
    x_new_max = np.max(x_new)
    params = stats.beta.fit(x_new, fscale=105)
    newScale = params[2] + params[3]
    params = stats.beta.fit(x_new, floc=0, fscale=100)
    #params = stats.beta.fit(x_new)
    # evaluate PDF
    x4beta = np.arange(0, x_new_max, 0.2)
    x4beta_new = (x4beta - 0) / 1.0
    pdf = stats.beta.pdf(x4beta_new, *params)
    r = stats.beta.rvs(params[0], params[1], size=1000)


    # aproximate by normal distribution
    mu_aprox, sigma_aprox = norm.fit(x)
    #num_bins = round( x.size / 5 )
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.set_xlim(55, x_new_max)
    # the histogram of the data
    #n, bins, patches = ax.hist(x, num_bins, width=width, density=True)
    #n, bins, patches = ax.hist(x, density=True)
    bins = 22 # 'scott', 'freedman', 'knuth', 'blocks'
    astro.hist(x_new, bins=bins, ax=ax, histtype='stepfilled', density=True)
    #astro.hist(r, bins=bins, ax=ax, alpha=0.5, histtype='stepfilled', density=True)
    # add a 'best fit' line
    x2 = np.arange(35, 110)
    y2 = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
        np.exp(-0.5 * (1 / sigma * (x2 - mu))**2))
    y3 = ((1 / (np.sqrt(2 * np.pi) * sigma_aprox)) *
        np.exp(-0.5 * (1 / sigma_aprox * (x2 - mu_aprox))**2))
    #ax.plot(x2, y2, ls=':', color='blue')
    ax.plot(x2, y3, ls='--', color='green')
    ax.plot(x4beta_new, pdf, '--r', lw=3.0)
    ax.set_xlabel('Grade')
    ax.set_ylabel('Density of students grades')
    ax.set_title(f'Test Histogram{round(params[0],1), round(params[1],1), round(params[2],1), round(params[3],1)}\
        : N={x.size}, Bins={bins}, \
        \u03bc={mu}({round(mu_aprox, 1)}), \u03C3={sigma}({round(sigma_aprox, 1)})')
    fig2_html = mpld3.fig_to_html(fig)
  # End Bar example

    """return HttpResponse("Hello, world. You're at the polls index.")"""
    course_list = [{'name':'name', 'start_date':'start_date', "finish_date":"finish_date" },
                   {'name':'sfjh', 'start_date':'rrrrrrrrrr', "finish_date":"dfjdjdyjdyj" },
                   {'name':'gjfj', 'start_date':'ggggggffff', "finish_date":"cvmn4565676" }]
    context = {'figure': fig_html, 'figure2': fig2_html, 'course_list': course_list}
    return render(request, 'gausscourse/test.html', context)
