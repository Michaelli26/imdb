import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interpn
import os


# Credit to Guillaume for density_scatter https://stackoverflow.com/a/53865762/12056557
def density_scatter(x, y, label, sort=True, bins=20, **kwargs):
    """
    Scatter plot colored by 2d histogram
    """
    fig, ax = plt.subplots()
    data, x_e, y_e = np.histogram2d(x, y, bins=bins)
    z = interpn((0.5 * (x_e[1:] + x_e[:-1]), 0.5 * (y_e[1:] + y_e[:-1])), data, np.vstack([x, y]).T, method="splinef2d",
                bounds_error=False)
    # Sort the points by density, so that the densest points are plotted last
    if sort:
        idx = z.argsort()
        x, y, z = x[idx], y[idx], z[idx]
    cax = ax.scatter(x, y, c=z, **kwargs)
    cbar = fig.colorbar(cax)
    cbar.set_label(label)
    return ax


def mem_usage(pandas_obj):
    if isinstance(pandas_obj, pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else:  # we assume if not a df it's a series
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2  # convert bytes to megabytes
    return "{:03.2f} MB".format(usage_mb)


STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)),'imdb', 'static')

# retrieve data from multiple tsv files
basics_dtype = {'isAdult': int, 'tconst': str, 'titleType': str, 'primaryTitle': str, 'startYear': str, 'endYear': str,
         'runTimeMinutes': str, 'genres': str}
basics = pd.read_table('title.basics.tsv', dtype=basics_dtype)
ratings_dtype = {'tconst': str, 'averageRating': float, 'numVotes': int}
ratings = pd.read_table('title.ratings.tsv', dtype=ratings_dtype)
all_info = basics.merge(right=ratings, how='left', on='tconst')
# clean up data
extra = all_info['startYear'].str.extract(r'^(\d{4})', expand=False)
all_info['startYear'] = pd.to_numeric(extra, downcast='unsigned')
all_info['isAdult'] = pd.to_numeric(all_info['isAdult'], downcast='unsigned')
all_info['runtimeMinutes'] = pd.to_numeric(all_info['runtimeMinutes'], downcast='unsigned', errors='coerce')
all_info = all_info[all_info.isAdult == 0]
all_info = all_info[all_info.titleType == 'movie']
all_info['startYear'].apply(lambda x: int(x) if x == x else "")
to_drop = ['originalTitle', 'endYear', 'genres', 'isAdult', 'titleType']
all_info.drop(to_drop, axis=1, inplace=True)

# create graph displaying movies produced per year (fig1)
fig1_df = all_info[all_info.startYear <= 2018]  # data is not finished for 2019
grouped = fig1_df.groupby('startYear')
group_count = grouped.size()
movies_per_year = group_count.to_dict()
fig1, ax1 = plt.subplots()
ax1.plot(list(movies_per_year.keys()), list(movies_per_year.values()))
ax1.set_ylabel('Number of Movies Produced', fontsize=16)
ax1.set_xlabel('Year', fontsize=16)

# annotate movies produced per year (fig1)
timeline = {1895: ['Lumi\u00E8re \nbrothers \nshort films', (1895, 100), (1890, 6000)],
            1908: ['Winter Film Capital \nof the World\n(Jacksonville, FL)', (1908, 500), (1915, 14000)],
            2000: ['Rise of Modern\nTechnology', (2000, 6000), (1980, 13000)]
            }
for year, info in timeline.items():
    ax1.annotate(s=info[0], xy=info[1], xytext=info[2], arrowprops={'width': 0.2, 'headwidth': 0.2, 'headlength': 0.1})
ax1.annotate('', xy=(1920, 3000), xytext=(1965, 3000), arrowprops=dict(arrowstyle="-", connectionstyle='bar'))
ax1.text(1920, 6500, s='Golden Era of Hollywood')
plt.savefig(fname=os.path.join(STATIC_FOLDER, 'movies-vs-year.png'))
plt.tick_params(axis='y', labelsize=10)
plt.show()

# create ratings development over the years (fig2)
fig2_df = all_info[['startYear', 'runtimeMinutes', 'averageRating']]
fig2_df.dropna(inplace=True)
fig2_df = fig2_df[fig2_df.startYear > 1914]  # issue with films being categorized as shorts instead of movies
fig2_df = fig2_df[fig2_df.startYear < 2019]
grouped_startyear = fig2_df.groupby('startYear')
fig2, ax2 = plt.subplots()
ax2.hexbin(fig2_df['startYear'], fig2_df['averageRating'], bins=[7, 7])
ax2.plot(grouped_startyear.mean()['averageRating'], 'k', linewidth=4)
ax2.set_ylabel('Average Ratting', fontsize=16)
ax2.set_xlabel('Year', fontsize=16)
plt.savefig(fname=os.path.join(STATIC_FOLDER, 'ratings-vs-year.png'))
plt.show()

# create graph displaying the change of run time lengths over the years (fig3)
fig2_df = fig2_df[fig2_df.runtimeMinutes < 300]
grouped_runtime = fig2_df.groupby('startYear')
fig3, ax3 = plt.subplots()
ax3.plot(grouped_runtime.mean()['runtimeMinutes'])
ax3.set_ylabel('Average Running time [mins]', fontsize=16)
ax3.set_xlabel('Year', fontsize=16)
ax3.set_title('Development of Running Times', fontsize=22)
plt.savefig(fname=os.path.join(STATIC_FOLDER, 'runtime-vs-year.png'))
plt.show()

# Create ratings vs number of votes plot (fig4)
ratings_fig = all_info[all_info.numVotes < 80000]
ax4 = density_scatter(ratings_fig['numVotes'], ratings_fig['averageRating'], label='Number of Movies', bins=[80, 80])
ax4.set_ylabel('Average Rating', fontsize=16)
ax4.set_xlabel('Number of Votes', fontsize=16)
plt.savefig(fname=os.path.join(STATIC_FOLDER, 'ratings-vs-votes.png'))
plt.show()

# average rating and run time (fig5)
fig5_df = all_info[['averageRating', 'runtimeMinutes', 'numVotes']]
fig5_df.dropna(inplace=True)
fig5_df = fig5_df[fig5_df.runtimeMinutes < 300]
ax5 = density_scatter(fig5_df['runtimeMinutes'], fig5_df['averageRating'], label='Number of Movies', bins=[80, 80])
ax5.set_ylabel('Average Rating', fontsize=16)
ax5.set_xlabel('Running Time [mins]', fontsize=16)
plt.savefig(fname=os.path.join(STATIC_FOLDER, 'ratings-vs-runtime.png'))
plt.show()

# num votes vs runtime (fig6)
fig6_df = fig5_df[fig5_df.numVotes < 100000]
ax6 = density_scatter(fig6_df['runtimeMinutes'], fig6_df['numVotes'], label='Number of Movies', bins=[80, 80])
ax6.set_ylabel('Total Number of Votes', fontsize=16)
ax6.set_xlabel('Running Time [mins]', fontsize=16)
plt.savefig(fname=os.path.join(STATIC_FOLDER, 'votes-vs-runtime.png'))
plt.tick_params(axis='y', labelsize=10)
plt.show()


# convert all_info startyear and runtime to int
# write dataframe to a csv that will be uploaded to Postgresql database
psql_df = all_info[['tconst', 'averageRating', 'numVotes', 'primaryTitle', 'startYear', 'runtimeMinutes']]
psql_df.dropna(inplace=True)
psql_df['runtimeMinutes'] = psql_df['runtimeMinutes'].astype('int')
psql_df['numVotes'] = psql_df['numVotes'].astype('int')
# ratings['runtimeMinutes'] = pd.to_numeric(ratings['runtimeMinutes'], errors='coerce').fillna(0).astype(np.int64)
# psql_df['startYear'] = pd.to_numeric(psql_df['startYear'], downcast='unsigned', errors='coerce')
psql_df['startYear'] = pd.to_numeric(psql_df['startYear'], downcast='unsigned', errors='coerce').fillna(0).astype(
    np.int64)

psql_df.insert(loc=3, column='weightedRating',
               value=((psql_df['averageRating'] * psql_df['numVotes']) + (7.0 * 25000)) / (psql_df['numVotes'] + 25000),
               allow_duplicates=True)
psql_df.sort_values(by='weightedRating', ascending=False, inplace=True)
psql_df = psql_df.head(9999)
psql_df.to_csv(path_or_buf=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imdb-data.csv'))
