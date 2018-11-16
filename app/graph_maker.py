from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.plotly as py
import plotly.graph_objs as go


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


    @staticmethod
    def get_dest_graph(stats, type):
        x = []
        y = []
        if type == 'country':
            for entry in stats:
                entry["country"] = entry["country"].replace('_', ' ')
                if entry["country"] in x:
                    y[x.index(entry["country"])] += entry["amount"]
                else:
                    x.append(entry["country"])
                    y.append(entry["amount"])

        elif type == 'city':
            for entry in stats:
                entry["city"] = entry["city"].replace('_', ' ')
                x.append(entry["city"])
                y.append(entry["amount"])

        tuples = []
        for i in range(0, len(x)):
            tuples.append((x[i], y[i]))

        tuples.sort(key=lambda tup: tup[1], reverse=True)

        x = []
        y = []
        for tup in tuples:
            x.append(tup[0])
            y.append(tup[1])

        data = [go.Bar(
            x=x,
            y=y,
            marker=dict(
                color='rgb(58,200,225)'
            ),
        )]

        my_plot_div = plot(data, output_type='div')
        return my_plot_div
