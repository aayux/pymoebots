import plotly.express as px
import plotly.graph_objects as go

import pandas as pd


def test():
    d = dict(points=[-3, -2, -1, 0, 1, 2, 3], points_y=[0,0,0,0,0,0,0], steps=[0, 1, 2, 3, 4, 5, 6], path=[[0,1,0,-1,0,1,2], [0,-1,0,1,0,-1,-2]])

    # test_df = pd.DataFrame(d)
    # fig = px.scatter(test_df, x=test_df.path, y=test_df.points_y, animation_frame=test_df.steps, range_x=[-4,4], range_y=[-1,1])
    fig1 = px.scatter(x=d['path'][0], y=d['points_y'], animation_frame=d['steps'], range_x=[-4, 4],
                     range_y=[-1, 1])
    fig2 = px.scatter(x=d['path'][1], y=d['points_y'], animation_frame=d['steps'], range_x=[-4, 4],
                     range_y=[-1, 1])
    # fig3 = px.line(test_df, x=test_df.points, y=test_df.points_y)
                     # y=points_y, animation_frame=path, animation_group=path, range_x=[-4,4], range_y=[-1,1])
    fig1.append_trace(fig2.data[0],None,None)
    fig1.show()

def create_environment(x,x_path,y,y_path):
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
    print(line)
