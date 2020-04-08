import os

import plotly.graph_objects as go
from dataclasses import dataclass, field

@dataclass
class TriangularGridViz(object):
    __grid_x: int = None
    __grid_y: int = None
    __grid_x_shear: int = None
    __grid_y_shear: int = None
    __points: int = None
    __data: list = []
    __frames: list = []
    __frame_data: list = []
    __figure: object = []

    def draw_grid(self, plots: list):
        # add grid points to draw
        self.__grid_x = plots[0]
        self.__grid_y = plots[1]
        self.__grid_x_zig = plots[2]
        self.__grid_y_zig = plots[3]

        straight_lines = go.Scatter(x=self.__grid_x, y=self.__grid_y,
                                    mode='lines', name="straight lines",
                                    line=dict(width=1, color='black')
        )

        sheared_lines = go.Scatter(x=self.__grid_x_shear, y=self.__grid_y_shear,
                                   mode='lines', name="sheared lines", 
                                   line=dict(width=1,color='black')
        )

        self.__data.append(straight_lines)
        self.__data.append(sheared_lines)

    def draw_nodes(self, points: list):
        # nodes are intersecting points on the grid
        nodes = go.Scatter(x=[x[0] for x in points], 
                           y=[y[1] for y in points],
                           mode='markers',
                           name='nodes',
                           line=dict(width=2, color='black')
        )
        self.__data.append(nodes)

    def draw_bots(self, bot_list: list):
        for ix, _bot in enumerate(bot_list):
            bot = go.Scatter(x=[_bot[0][0], _bot[1][0]],
                             y=[_bot[0][1], _bot[1][1]],
                             name=f"bot {ix}",
                             mode='markers',
                             marker=dict(size=10, color='black'),
                             showlegend=False
            )
            self.__data.append(bot)

    def draw_frames(self, path: list):
        mode = ["markers", "lines + markers"]
        # DO: rewrite
        self.__frames = [go.Frame(data=[go.Scatter(
                            x=[path[ix][0][jx], path[ix][2][jx]],
                            y=[path[ix][1][jx], path[ix][3][jx]],
                            name=f'bot {ix}', mode=mode[1],
                            marker=dict(size=10, color='black')) \
                            if path[ix][0][jx] != path[ix][2][jx] \
                            else go.Scatter(
                            x=[path[ix][0][jx], path[ix][2][jx]],
                            y=[path[ix][1][jx], path[ix][3][jx]],
                            name=f"bot {ix}",
                            mode=mode[0],
                            marker=dict(size=10, color='black'))
                        for ix in range(len(path))])
                    for jx in range(len(path[0][0]))]

    def draw_figure(self):
        self.__figure = go.Figure(
                        data=self.__data, 
                        layout=dict(
                            title='Demo',
                            updatemenus=[dict(type='buttons',
                                                buttons=[
                                                dict(
                                                    label='Play',
                                                    method='animate',
                                                    args=[None, 
                                                        dict(frame=dict(duration=500, 
                                                                        redraw=True),
                                                        fromcurrent=True,
                                                        transition=dict(duration=300,
                                                                        easing='quadratic-in-out'))]),
                                                dict(
                                                    label='Pause',
                                                    method='animate',
                                                args=[None, 
                                                    dict(frame=dict(duration=0, 
                                                                    redraw=False),
                                                        mode='immediate',
                                                        transition=dict(duration=0))
                                                    ]
                                                )
                                            ]
                                        )]
                            ),
            frames=self.__frames
        )

    def display_figure(self):
        self.__figure.show()
        if os.name == 'nt':
            pass
        else:
            self.__figure.write_html('demo.html', include_plotlyjs='cdn')
