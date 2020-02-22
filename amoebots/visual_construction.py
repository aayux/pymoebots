import plotly.graph_objects as go


class GridVisualClass(object):
    def __init__(self):
        self.__grid_x = None
        self.__grid_y = None
        self.__grid_x_zig = None
        self.__grid_y_zig = None
        self.__points = None
        self.__data = []
        self.__frames = []
        self.__frame_data = []
        self.__fig = None

    def create_grid(self, plots):
        self.__grid_x = plots[0]
        self.__grid_y = plots[1]
        self.__grid_x_zig = plots[2]
        self.__grid_y_zig = plots[3]

        straight_lines = go.Scatter(
            x=self.__grid_x,
            y=self.__grid_y,
            mode="lines",
            name="straight lines",
            line=dict(
                width=1,
                color="blue"
            )
        )
        zig_zags = go.Scatter(
            x=self.__grid_x_zig,
            y=self.__grid_y_zig,
            mode="lines",
            name="zig-zags",
            line=dict(
                width=1,
                color="blue"
            )
        )

        self.__data.append(straight_lines)
        self.__data.append(zig_zags)

    def create_nodes(self, points):
        nodes = go.Scatter(
            x=[x[0] for x in points],
            y=[y[1] for y in points],
            mode="markers",
            name="Nodes",
            line=dict(
                width=2,
                color="blue"
            )
        )
        self.__data.append(nodes)

    def create_bots(self, bots_list):
        i=0
        for bot in bots_list:
            bots = go.Scatter(
                x=[bot[0][0], bot[1][0]],
                y=[bot[0][1], bot[1][1]],
                name=f"bot {i}",
                mode="markers",
                marker=dict(size=10, color="red"),
                # line=dict(
                #     width=1,
                #     color="red",
                # ),
                showlegend=False
            )
            self.__data.append(bots)
            i+=1

    def create_frames(self, path):
        # [[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]]
        # for bot in range(len(path))
        # 0 [[],[],[],[]]
        # x = [path[bot][0][i], path[bot][2][i]]
        # for i in range(len(path[bot][0]))
        mode_set = ["markers", "lines+markers"]
        self.__frames = [go.Frame(
            data=[go.Scatter(
                x=[path[i][0][j], path[i][2][j]],
                y=[path[i][1][j], path[i][3][j]],
                name=f"bot {i}",
                mode=mode_set[1],
                marker=dict(size=10, color="red")) if path[i][0][j] != path[i][2][j] else go.Scatter(
                x=[path[i][0][j], path[i][2][j]],
                y=[path[i][1][j], path[i][3][j]],
                name=f"bot {i}",
                mode=mode_set[0],
                marker=dict(size=10, color="red"))
                for i in range(len(path))])
            for j in range(len(path[0][0]))]
        # for j in range(len(path[0][0]))
        # for i in range(len(path))
        # for i in range(1)
        # len(path)

        # self.__frames = [go.Frame(
        #     data=[go.Scatter(
        #         x=[path[i][0][0]],
        #         y=[path[i][0][1]], )
        #
        #         for i in range(len(path))])]

    def create_figure(self):
        self.__fig = go.Figure(
            data=self.__data,
            layout={'title': 'Amoebot Movement Demo',
                    'updatemenus': [dict(type="buttons",
                              buttons=[dict(label="Play",
                                            method="animate",
                                            args=[None, dict(frame=dict(duration=500, redraw=True),
                                                             fromcurrent=True,
                                                             transition=dict(duration=300,
                                                                             easing='quadratic-in-out'))]),
                                       dict(label='Pause',
                                            method='animate',
                                            args=[[None], dict(frame=dict(duration=0, redraw=False),
                                                               mode='immediate',
                                                               transition=dict(duration=0))])])]},
            frames=self.__frames
        )

    def show_fig(self):
        self.__fig.show()
        self.__fig.write_html('./Amoebot Movement Demo.html', include_plotlyjs='cdn')
