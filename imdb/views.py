from django.shortcuts import render
from movies.models import Movie


def home(request):
    return render(request, 'home.html')


def analysis(request):
    return render(request, 'analysis.html')


def search(request, page=1):
    if request.method == 'POST':
        title = request.POST['title']
        min_year = request.POST['min-year']
        max_year = request.POST['max-year']
        min_rank = request.POST['min-rank']
        max_rank = request.POST['max-rank']
        min_rating = request.POST['min-rating']
        max_rating = request.POST['max-rating']
        min_votes = request.POST['min-votes']
        max_votes = request.POST['max-votes']
        min_runtime = request.POST['min-runtime']
        max_runtime = request.POST['max-runtime']
        results = Movie.objects.filter(title__icontains=title).filter(
            year__gte=min_year).filter(year__lte=max_year).filter(
            rank__gte=min_rank).filter(rank__lte=max_rank).filter(
            rating__gte=min_rating).filter(rating__lte=max_rating).filter(
            num_votes__gte=min_votes).filter(num_votes__lte=max_votes).filter(
            runtime__gte=min_runtime).filter(runtime__lte=max_runtime)
        '''criteria = f"{results.count()} Matches. Results for titles: '{title}' Release Date: {min_year} - {max_year} "\
                   f"Ranking: {min_rank} - {max_rank} Rating: {min_rating} - {max_rating} " \
                   f"Votes: {min_votes} - {max_votes}"
                   '''

        context = {'num_results': results.count(), 'min_year': min_year, 'max-year': max_year, 'min_rank': min_rank,
                   'max-rank': max_rank, 'min_rating': min_rating, 'max-rating': max_rating, 'min_votes': min_votes,
                   'max-votes': max_votes, 'min_runtime': min_runtime, 'max-runtime': max_runtime, 'results': results,
                   #'criteria': criteria,
                   }
        return render(request, 'search.html', context=context)
    else:
        return render(request, 'home.html')
