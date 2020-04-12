import React from "react";
import {
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  Cell
} from "recharts";
import moment from "moment"


export default ({ supportedPests, pestColors, pestData, minDate, maxDate }) => {
  let summarizedPestData = []

  for (let pest of supportedPests) {
    let curDate = moment(minDate)
    let count = 0
    while (curDate <= maxDate) {
      if (pestData[curDate] && pestData[curDate][pest]) {
        count += pestData[curDate][pest].length
      }
      curDate = curDate.add(1, "days")
    }

    summarizedPestData.push({
      pest,
      count
    })
  }

  return (
    <ResponsiveContainer height={400} width="90%">
      <BarChart data={summarizedPestData}>
        <XAxis dataKey="pest" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="count">
          {summarizedPestData.map((entry, index) => (
            <Cell key={index} fill={pestColors[entry.pest]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}