import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_iterations(data: pd.DataFrame, column: str, selection: any, runs: int = 5) -> np.ndarray:
    sel = data[data[column] == selection]
    bests = sel[sel['run'] == 1]['best']
    for run in range(2, runs+1):
        best = sel[sel['run'] == run]['best']
        bests = np.sum([bests, best], axis=0)
    return np.divide(bests, 5)


if __name__ == '__main__':
    data = pd.read_csv('../../res/tune-iterations.csv')

    legends = [
        '100 iterations',
        '500 iterations',
        '1000 iterations'
    ]

    items = [
        100,
        500,
        1000
    ]

    for i in range(len(items)):
        iterations = get_iterations(data, 'iterations', items[i])
        plt.plot(
            np.arange(0, len(iterations)),
            iterations,
            label=legends[i]
        )

    plt.legend()
    # plt.show()

    plt.savefig("../../res/plots/tune-iterations.svg")
