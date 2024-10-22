import plotly.graph_objects as go

def g_visualize(
    x,
    y,
    markers=(),
    markers_settings=(),
    add={}
):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Close Price'))
    for add_sett in add:
        fig.add_trace(go.Scatter(
            x=add_sett["x"],
            y=add_sett["y"],
            mode='lines',
            name=add_sett["name"]
        ))

    for mark, setting in zip(markers, markers_settings):
        for el in setting:
            if_key = mark == el["class_"]
            fig.add_trace(go.Scatter(
                x=mark[if_key].index,
                y=y[if_key],
                mode='markers',
                marker=dict(size=10, color=el["color"]),
                name=el["name"]
            ))

    fig.update_layout(
        title='Price with Predicted Buy Signals',
        xaxis_title='Date',
        yaxis_title='Price',
        legend_title='Legend',
    )
    fig.show()
