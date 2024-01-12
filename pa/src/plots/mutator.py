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
    data = pd.read_csv('../../res/tune-mutator.csv')

    legends = [
        'Vertex Move Mutation [fc=0.05, fv=0.05]',
        'Vertex Move Mutation [fc=0.25, fv=0.25]',
        'Vertex Move Mutation [fc=0.5, fv=0.5]',
        'Vertex Move Mutation [fc=0.75, fv=0.75]'
    ]

    for legend in legends:
        iterations = get_iterations(data, 'mutator', legend)
        plt.plot(
            np.arange(0, len(iterations)),
            iterations,
            label=legend
        )

    plt.legend()
    # plt.show()

    plt.savefig("../../res/plots/tune-mutator.svg")
