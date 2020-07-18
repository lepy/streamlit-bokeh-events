import React, { ReactNode } from "react"
import {
  withStreamlitConnection,
  StreamlitComponentBase,
  Streamlit,
} from "./streamlit"
import { embed } from "@bokeh/bokehjs";

interface State {
  eventDetailMap: Map<string, object>;
}

class BokehChange extends StreamlitComponentBase<State> {
  public state = { eventDetailMap: new Map() };

  componentDidMount() {
    const chart: any = document.getElementById(this.props.args["_id"])

    // empty the element
    while (chart.lastChild) {
      chart.lastChild.remove()
    }
    const events = this.props.args["events"]

    events.split(",").forEach(
      (eventName: string) => {
        document.addEventListener(eventName,
          (event: any) => {
            this.setState(
              prevState => ({ eventDetailMap: prevState.eventDetailMap.set(eventName, event.detail) }),
              () => Streamlit.setComponentValue(Object.fromEntries(this.state.eventDetailMap))
            )
          }
        );
      }
    )

    const bokehJson = this.props.args["bokeh_plot"]
    embed.embed_item(JSON.parse(bokehJson))
    Streamlit.setFrameHeight(window.outerHeight)
  }

  public render = (): ReactNode => {
    return (
      <div id={this.props.args["_id"]} className="stBokehChart"></div>
    )
  }
}

export default withStreamlitConnection(BokehChange)