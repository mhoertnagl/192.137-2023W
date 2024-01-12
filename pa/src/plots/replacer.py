import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_iterations(data: pd.DataFrame, column: str, selection: str, runs: int = 5) -> np.ndarray:
    sel = data[data[column] == selection]
    bests = sel[sel['run'] == 1]['best']
    for run in range(2, runs+1):
        best = sel[sel['run'] == run]['best']
        bests = np.sum([bests, best], axis=0)
    return np.divide(bests, 5)


if __name__ == '__main__':
    data = pd.read_csv('../../res/tune-replacer.csv')

    legends = [
        'Best Replacement',
        'Elite Replacement [f=0.1]',
        'Elite Replacement [f=0.25]',
        'Elite Replacement [f=0.5]'
    ]

    for legend in legends:
        iterations = get_iterations(data, 'replacer', legend)
        plt.plot(
            np.arange(0, len(iterations)),
            iterations,
            label=legend
        )

    plt.legend()
    # plt.show()

    plt.savefig("../../res/plots/tune-replacer.svg")
