import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";


export default ({ animal_counts }) => {
  const counts_as_list = Object.keys(animal_counts).map(key => {
    return {
      key,
      count: animal_counts[key],
    }
  })
  console.log("Displaying animal counts:", counts_as_list)

  return (
    <ResponsiveContainer height={400} width="90%">
      <BarChart data={counts_as_list}>
        <XAxis dataKey="key" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="count" fill="pink" />
      </BarChart>
    </ResponsiveContainer>
  )
}