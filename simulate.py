from storeFunc import functions
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns

n_row = 50
n_col = 50
probInitBacteria = 0.15
diffusionRate = 0.125
probGrow = 75
consumeRate = 0.5
iter = 100

bioFilm = functions(n_row, n_col, probInitBacteria, diffusionRate, probGrow, consumeRate, iter)
bacteria_frames, nutrition_frames = bioFilm.simulate()


def init():
    plt.clf()
    return None

for i, frames in enumerate([nutrition_frames, bacteria_frames]):
    if i == 0:
        word = 'Nutrition Consumption Simulation'
    else:
        word = 'Bacteial Grow Simulation'
    def animate(i):
        plt.clf()
        ax = sns.heatmap(frames[i],
                        center=1,
                        square=True,
                        xticklabels=False,
                        yticklabels=False
                        )
        ax.set_title(word)
        return None

    fig = plt.figure()
    anim = animation.FuncAnimation(fig,
                                animate,
                                frames=range(0, iter, 1),
                                blit=False,
                                interval=250,
                                init_func=init)
    plt.show()
