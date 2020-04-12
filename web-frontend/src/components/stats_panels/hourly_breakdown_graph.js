import React from "react";
import {
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  CartesianGrid,
} from "recharts";
import DefaultTooltipContent from 'recharts/lib/component/DefaultTooltipContent'
import moment from "moment"


export default ({ supportedPests, pestColors, pestData, minDate, maxDate }) => {
  const groupedPestData = supportedPests.reduce((obj, key) => {
    obj[key] = []
    return obj
  }, {})
  const occurancePestIndex = {}

  for (let [date, payload] of Object.entries(pestData)) {
    for (let [pest, occurances] of Object.entries(payload)) {
      if (occurances) {
        for (let occurance of occurances) {
          const x = moment(date).unix()
          const y = moment(occurance).get("hour") + (moment(occurance).get("minute") / 60)
          groupedPestData[pest].push({x, y})
          occurancePestIndex[[x, y]] = pest[0].toUpperCase() + pest.slice(1)
        }
      }
    }
  }

  const renderTooltip = props => {
    if (props.payload[0] != null) {
      let x = 0;
      let y = 0;

      for (let payload of props.payload) {
        if (payload.name === 'date') {
          x = payload.value
        } else if (payload.name === 'hour') {
          y = payload.value
        }
      }

      if (occurancePestIndex[[x, y]]) {
        const newPayload = [
          {
            name: "pest",
            value: occurancePestIndex[[x, y]]
          },
          ...props.payload,
        ]

        return <DefaultTooltipContent {...props} payload={newPayload} />
      }
    }

    return <DefaultTooltipContent {...props} />
  }

  return (
    <ResponsiveContainer height={400} width="90%">
      <ScatterChart>
        <CartesianGrid />
        <XAxis domain={['dataMin - 10000', 'dataMax + 10000']} type="number" dataKey="x" name="date"
          tickFormatter={(val) => moment.unix(val).format("MMM DD")} />
        <YAxis type="number" dataKey="y" name="hour" label={{ value: "hour", angle:-90 }} />
        <Tooltip content={renderTooltip} labelFormatter={(props) => {console.log(props); return "blah"}} formatter={(value, name) => {
          if (name === 'date') {
            return moment.unix(value).format("MMM DD")
          } else if (name === 'hour') {
            let mins = Math.floor((value * 60) % 60)
            return `${Math.floor(value)}:${ mins < 10 ? "0": ""}${mins}`
          }
          return value
        }} />
        {supportedPests.map((pest) => (
          <Scatter key={pest} name={pest} fill={pestColors[pest]} data={groupedPestData[pest]} />
        ))}
      </ScatterChart>
    </ResponsiveContainer>
  )
}