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
import moment from "moment"


export default ({ supportedPests, pestColors, pestData, minDate, maxDate }) => {
  const groupedPestData = supportedPests.reduce((obj, key) => {
    obj[key] = []
    return obj
  }, {})

  for (let [date, payload] of Object.entries(pestData)) {
    for (let [pest, occurances] of Object.entries(payload)) {
      if (occurances) {
        for (let occurance of occurances) {
          groupedPestData[pest].push({
            x: moment(date).unix(),
            y: moment(occurance).get("hour") + (moment(occurance).get("minute") / 60),
          })
        }
      }
    }
  }
  console.log(groupedPestData)

  return (
    <ResponsiveContainer height={400} width="90%">
      <ScatterChart>
        <CartesianGrid />
        <XAxis domain={['dataMin - 10000', 'dataMax + 10000']} type="number" dataKey="x" name="date"
          tickFormatter={(val) => moment.unix(val).format("MMM DD")} />
        <YAxis label="hour" type="number" dataKey="y" name="hour" label={{ value: "hour", angle:-90 }} />
        <Tooltip formatter={(value, name) => {
          if (name === 'date') {
            return moment.unix(value).format("MMM DD")
          } else {
            return `${Math.floor(value)}:${(value * 60) % 60}`
          }
        }} />
        {supportedPests.map((pest) => (
          <Scatter key={pest} name={pest} fill={pestColors[pest]} data={groupedPestData[pest]} />
        ))}
      </ScatterChart>
    </ResponsiveContainer>
  )
}