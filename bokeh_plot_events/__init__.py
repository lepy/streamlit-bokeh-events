from bokeh.embed import json_item
import json

import os
from random import choices
from string import ascii_letters
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "bokeh_plot_events", url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("bokeh_plot_events", path=build_dir)


def bokeh_plot_events(bokeh_plot=None, events="", key=None):
    div_id = "".join(choices(ascii_letters, k=16))
    fig_dict = json_item(bokeh_plot, div_id)
    json_figure = json.dumps(fig_dict)
    component_value = _component_func(
        bokeh_plot=json_figure, events=events, key=key, _id=div_id, default=None
    )
    return component_value


if not _RELEASE:
    import streamlit as st
    from random import random
    from bokeh.models import ColumnDataSource, CustomJS
    from bokeh.plotting import figure

    x = [random() for x in range(500)]
    y = [random() for y in range(500)]

    source = ColumnDataSource(data=dict(x=x, y=y))
    plot = figure(sizing_mode="scale_both", tools="lasso_select", title="Select Here")
    plot.circle("x", "y", source=source, alpha=0.6)

    source.selected.js_on_change(
        "indices",
        CustomJS(
            args=dict(source=source),
            code="""
            document.dispatchEvent(
                new CustomEvent("TestEvent", {detail: {indices: cb_obj.indices}})
            )
            document.dispatchEvent(
                new CustomEvent("SomeOtherEvent", {detail: {indices: [1, 2, 34]}})
            )
        """,
        ),
    )

    event_result = bokeh_plot_events(
        events="TestEvent,SomeOtherEvent", bokeh_plot=plot, key="foo"
    )
    st.write(event_result)