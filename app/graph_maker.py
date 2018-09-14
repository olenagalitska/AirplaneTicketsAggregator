from plotly.offline import plot
from plotly.graph_objs import Scatter


class GraphMaker:

    @staticmethod
    def get_price_graph(dates, fares):

        n = len(fares[0])
        print(n)
        fares_matrix = []
        for i in range(0, n):
            fares_matrix.append([])

        print(fares_matrix)

        for i in range(0, n):
            print(fares_matrix[i])
            for j in range(0, len(dates)):
                print(fares[j][i]['amount'])
                fares_matrix[i].append(fares[j][i]['amount'])

        print(fares_matrix)

        random_x = dates
        traces = []
        for i in range(0, n):
            trace = Scatter(
                x=random_x,
                y=fares_matrix[i],
                mode='lines+markers',
                name='Fare' + str(i + 1)
            )
            traces.append(trace)

        my_plot_div = plot(traces, output_type='div')
        return my_plot_div
