import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random


def show():
    df = px.data.gapminder()
    fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
               size="pop", color="continent", hover_name="country",
               log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90])
    fig.write_html('./show.html')


class LineArea (object):
    def __init__(self):
        self.__fig = go.Figure()

    def create_environment(self, x, x_path, y, y_path, exit_node):
        # d = dict(points=x, points_y=y, steps=np.arange(0, x_path.size),
        #          path=x_path, path_y=y_path)
        # size = [20]

        # test_df = pd.DataFrame(d)
        # fig = px.scatter(test_df, x=test_df.path, y=test_df.points_y, animation_frame=test_df.steps, range_x=[-4,4], range_y=[-1,1])
        # fig1 = px.scatter(x=d['path'][0], y=d['path_y'][0], animation_frame=d['steps'], range_x=[x.min(), x.max()],
        #                   range_y=[y.min(), y.max()], size=np.linspace(20,20, x_path.size))
        # fig2 = px.scatter(x=d['path'][1], y=d['path_y'][0], animation_frame=d['steps'], range_x=[-4, 4],
        #                   range_y=[-1, 1])
        # fig3 = px.line(x=d['points'], y=d['points_y'])
        # fig4 = px.scatter(x=[exit_node[0]], y=[exit_node[1]], size=[2])
        # y=points_y, animation_frame=path, animation_group=path, range_x=[-4,4], range_y=[-1,1])

        # Plot.ly express test.
        # d = dict(points=x, points_y=y, steps=np.arange(0, x_path.size),
        #          path=x_path, path_y=y_path)
        # size = [20]
        # fig1 = px.scatter(x=d['path'][0], y=d['path_y'][0], animation_frame=d['steps'], range_x=[x.min(), x.max()],
        #                   range_y=[y.min(), y.max()], size=np.linspace(20, 20, x_path.size))
        # fig3 = px.line(x=d['points'], y=d['points_y'])
        # fig4 = px.scatter(x=[exit_node[0]], y=[exit_node[1]], size=[2])
        # fig1.append_trace(fig3.data[0], None, None)
        # fig1.append_trace(fig4.data[0], None, None)
        # fig1.update_layout(fig4.layout)
        # fig1.write_html('./file2.html')
        # fig1.show()

        line = go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name="Line Area",
            line=dict(
                width=2,
                color="blue"
            )
        )

        nodes = go.Scatter(
            x=x,
            y=y,
            mode="markers",
            name="Line Nodes",
            marker=dict(
                size=5,
                color="blue"
            )
        )

        exit_node = go.Scatter(
            x=[exit_node[0]],
            y=[exit_node[1]],
            mode="markers",
            name="Exit Node",
            marker=dict(
                size=10,
                color="green"
            )
        )

        data = []
        for i in range(x_path.shape[0]+1):
            data.append(line)
        data.append(nodes)
        data.append(exit_node)



        colors = np.array(['black', 'gold', 'orange', 'pink', 'purple', 'red', 'yellow'])
        bot_colors = np.array([], dtype='<U20')
        for i in range(x_path.shape[0]):
            bot_colors = np.append(bot_colors, random.choice(colors))

        frames = [go.Frame(
            data=[go.Scatter(
                x=[x_path[i][k]],
                y=[y_path[i][k]],
                mode="markers",
                marker=dict(color=bot_colors[i], size=20),
                name=f'Bot {i}')
                for i in range(x_path.shape[0])], )
            for k in range(x_path.shape[1])]

        layout = go.Layout(
            xaxis=dict(range=[x.min(), x.max()], autorange=False, zeroline=False),
            yaxis=dict(range=[y.min(), y.max()], autorange=False, zeroline=False),
            title_text="Escape Algorithm", hovermode="closest",
            updatemenus=[dict(type="buttons",
                              buttons=[dict(label="Play",
                                            method="animate",
                                            args=[None, dict(frame=dict(duration=500, redraw=False),
                                                             fromcurrent=True,
                                                             transition=dict(duration=300,
                                                                             easing='quadratic-in-out'))]),
                                       dict(label='Pause',
                                            method='animate',
                                            args=[[None], dict(frame=dict(duration=0, redraw=False),
                                                               mode='immediate',
                                                               transition=dict(duration=0))])])]

        )
        self.__fig = go.Figure(
            data=data,
        )

        self.__fig.frames=frames
        self.__fig.layout=layout

        # self.__fig.data = data

        # self.__fig.append_trace(line,None,None)
        # self.__fig.append_trace(line, None, None)
        self.__fig.write_html('./file3.html', include_plotlyjs='cdn')
        # print(line)
        #

        #

