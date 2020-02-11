import plotly.graph_objects as go


class GridVisualClass (object):
    def __init__(self):
        self.__grid_x = None
        self.__grid_y = None
        self.__grid_x_zig = None
        self.__grid_y_zig = None
        self.__data = []
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
                width=2,
                color="blue"
            )
        )
        zig_zags = go.Scatter(
            x=self.__grid_x_zig,
            y=self.__grid_y_zig,
            mode="lines",
            name="zig-zags",
            line=dict(
                width=2,
                color="blue"
            )
        )

        self.__data.append(straight_lines)
        self.__data.append(zig_zags)

        self.__fig = go.Figure(
            data=self.__data,
        )

    def show_fig(self):
        self.__fig.show()
