import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data = pd.read_csv('../../res/tune-selection.csv')
    print(data)
    rank = data[data['selection'] == 'Rank Selection [f=0.5]']
    print(rank)

    plt.plot(np.arange(0,len(f)),f,label = legends[index])

    # plt.savefig("..//res/plots/heuOpt.png")

    # for improv in improvements:
    #     nbhs = [nhs.VertexMoveNeighborhood(improv),nhs.ComponentMergeNeighborhood(improv),nhs.ComponentMergeNeighborhood(improv)]
    #     for index,nbh in enumerate(nbhs):
    #         # improv = improvements[0]
    #         # nbh = nbhs[1]
    #         sol = constructed_sol.copy()
    #         ls = localsearch.LocalSearchTuning(nbh, ls_ter)
    #         sol,c,f,lo = ls.run(sol)
    #         lo_list.append(lo)
    #         f_list.append(f)
    #         plt.plot(np.arange(0,len(f)),f,label = legends[index])
    #         # break
    #     plt.legend()
    #     plt.show()
    #     # break