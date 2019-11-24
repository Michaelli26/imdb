import bs4
import requests
import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from movies.models import Movie
import math


def browse(request, category, page, context={}):
    '''
    This function is called when a user hits a 'browse by' button on the Home page and any pages clicked during the
    browsing session.

    :param request: HttpRequest Object
    :param category: sort by category
    :param page: page number
    :param context: constructor of django.template.Context - dictionary mapping variable names to values
    :return: a django render function that returns an HttpResponse object
    '''
    total_results = Movie.objects.count()
    results_per_page = 24
    total_pages = math.ceil(total_results/results_per_page)

    context['total_pages'] = total_pages
    movies = Movie.objects.order_by('-'+category.lower())
    if category == 'rank':
        movies = movies.reverse()
    if page == 1:
        results = movies[:results_per_page]
    else:
        results = movies[(page-1)*results_per_page:page*results_per_page]

    context['results'] = results

    # create page navigation
    min_page = page-10
    max_page = page+10
    if min_page <= 0:
        display_pages = range(1, max_page+abs(min_page))
    elif max_page > total_pages:
        display_pages = range(min_page - (max_page-total_pages), total_pages+1)
    else:
        display_pages = range(min_page, max_page)
    context['display_pages'] = display_pages
    context['page'] = page


    context['category'] = category
    if category == 'num_votes':
        context['category_display'] = 'Number of Votes'
    else:
        context['category_display'] = category.capitalize()


    return render(request, 'results.html', context=context)


'''
Found out IMDb's Terms of Service forbids web scraping

def details(request):
    if request.method == 'POST':
        movie_id = request.POST['movie']
        movie = Movie.objects.get(id=movie_id)
        # attributes haven't been set before
        if movie.genre == '' or movie.summary == '' or movie.country == '' or movie.language == '':
            res = requests.get('https://www.imdb.com/title/' + movie.id)
            try:
                res.raise_for_status()
            except requests.exceptions.HTTPError:
                return
            soup = bs4.BeautifulSoup(res.text, features='html.parser')
            genre_tag = soup.select("div[class='see-more inline canwrap'] > a")
            regex = re.compile(r'(genres=)([a-z]+)')
            matches = re.findall(regex, str(genre_tag))
            if matches:
                genres = [match[1].capitalize() for match in matches]
                movie.genre = ', '.join(genres)

            country = soup.select('a[href^="/search/title?country_of_origin"]')
            if country:
                movie.country = country[0].text

            language_tag = soup.select("a[href^='/search/title?title_type=feature&primary_language=']")
            if language_tag:
                languages = [language.text for language in language_tag]
                movie.language = ', '.join(languages)

            summary_tag = soup.select("div[class='summary_text']")
            summary = summary_tag[0].get_text().strip()
            summary = summary.replace('See full summary\xa0»', '')
            movie.summary = summary
            movie.save()

        # construct message text
        msg_text = 'Genre: ' + movie.genre
        if movie.country:
            msg_text += ' | Country: ' + movie.country
        if movie.language:
            msg_text += ' | Language: ' + movie.language
        msg_text += ' | Summary: ' + movie.summary


        # display message
        messages.success(request, msg_text)
        request.session['test'] = movie.id
        context = {'movie': movie}
        category = request.POST['category']
        page = int(request.POST['page'])
        response = browse(request, category, page, context)
        return response

'''