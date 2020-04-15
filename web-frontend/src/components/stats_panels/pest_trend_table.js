import React from "react"
import moment from "moment"


export default ({ pestData, maxDate, supportedPests }) => {
  const lastDate = moment(maxDate)
  const secondToLastDate = moment(maxDate).subtract(1, "days")

  let pestCounts = supportedPests.reduce((obj, pest) => {
    obj[pest] = 0
    return obj
  }, {})
  let pestTrend = supportedPests.reduce((obj, pest) => {
    obj[pest] = 0
    return obj
  }, {})

  for (let [date, payload] of Object.entries(pestData)) {
    for (let pest of supportedPests) {
      if (payload[pest]) {
        pestCounts[pest] += payload[pest].length
      }
    }

    if (moment(date).isSame(lastDate)) {
      for (let pest of supportedPests) {
        if (payload[pest]) {
          pestTrend[pest] += payload[pest].length
        }
      }
    }

    if (moment(date).isSame(secondToLastDate)) {
      for (let pest of supportedPests) {
        if (payload[pest]) {
          pestTrend[pest] -= payload[pest].length
        }
      }
    }
  }

  const sortedPests = supportedPests.slice(0)
  sortedPests.sort((a, b) => pestCounts[b] - pestCounts[a])

  return (
    <table className="table is-hoverable is-fullwidth">
      <thead>
        <tr>
          <th>Pest</th>
          <th>Count</th>
          <th>Daily Trend</th>
        </tr>
      </thead>
      <tbody>
        {sortedPests.map((pest) => {
          const isPositiveTrend = pestTrend[pest] > 0
          const isNegativeTrend = pestTrend[pest] < 0

          return (
            <tr key={pest}>
              <td>{pest}</td>
              <td>{pestCounts[pest] === 0 ? '-' : pestCounts[pest]}</td>
              <td className={ isPositiveTrend ? `has-text-danger` : `has-text-success`}>
                {isPositiveTrend ? `▲` : '' }
                {isNegativeTrend ? `▼` : '' }
                {` `}
                {pestTrend[pest] === 0 ? '-' : pestTrend[pest]}
              </td>
            </tr>
          )
        })}
      </tbody>
    </table>
  )
}