import React from "react";
import {
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Bar,
  BarChart
} from "recharts";
import moment from "moment";


export default ({ supportedPests, pestColors, pestData, minDate, maxDate }) => {
  let summarizedPestData = []
  let curDate = moment(minDate)
  while (curDate <= maxDate) {
    const curDateCopied = moment(curDate)
    let info = supportedPests.reduce((obj, pest) => {
      if (pestData[curDateCopied] && pestData[curDateCopied][pest]) {
        obj[pest] = pestData[curDateCopied][pest].length
      } else {
        obj[pest] = 0
      }

      return obj
    }, {})

    summarizedPestData.push({
      date: curDate.unix(),
      ...info
    })
    curDate = curDate.add(1, "days")
  }

  return (
    <ResponsiveContainer height={400} width="90%">
      <BarChart data={summarizedPestData}>
        <XAxis dataKey="date" tickFormatter={(val) => moment.unix(val).format("MMM DD")}/>
        <YAxis />
        <Tooltip labelFormatter={(value) => moment.unix(value).format("MMM DD")} />
        {supportedPests.map((pest) => (
          <Bar key={pest} stackId="a" dataKey={pest} fill={pestColors[pest]} />
        ))}
      </BarChart>
    </ResponsiveContainer>
  )
}