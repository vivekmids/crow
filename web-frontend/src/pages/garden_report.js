import React, { useState, useEffect } from 'react'

import Layout from "../components/layouts/default-layout"
import FilterBar from "../components/filter_bar"
import ImageList from '../components/image_list'
import PestTrendTable from "../components/stats_panels/pest_trend_table"
import AnimalCountGraph from "../components/stats_panels/animal_counts_graph"
import DailyBreakdownGraph from "../components/stats_panels/daily_breakdown_graph"
import PestSightings from "../components/stats_panels/pest_sightings"
import moment from "moment"


const DATE_FORMAT = "D MMM YYYY"
const SUPPORTED_PESTS = [
  'rodent',
  'squirrel',
  'rabbit',
  'bird',
  'deer',
  'raccoon',
  'skunk',
  'opossum',
  'other',
]
const PEST_COLORS = {
  'rodent': 'lightgray',
  'squirrel': 'brown',
  'rabbit': 'red',
  'bird': 'blue',
  'deer': 'orange',
  'raccoon': 'gray',
  'skunk': 'black',
  'opossum': 'darkgray',
  'other': 'green',
}


const DEFAULT_UI_STATE = {
  minFromDate: moment().subtract(7, "days").format(DATE_FORMAT),
  totalCount: 0,

  filteredCount: 0,
  filteredPests: []
}


function fixUpPestData(pestData, fromDate, toDate) {
  let curDate = moment(fromDate)
  let maxDate = moment(toDate)

  let fixedUp = {}
  while (curDate <= maxDate) {
    fixedUp[curDate] = SUPPORTED_PESTS.reduce((obj, pest) => {
      obj[pest] = []
      return obj
    }, {})
    curDate = curDate.add(1, "days")
  }

  let keys = Object.keys(pestData)
  for (let key of keys) {
    let newKey = moment(key)
    for (let pest of SUPPORTED_PESTS) {
      fixedUp[newKey][pest] = pestData[key][pest]
    }
  }

  return fixedUp
}


function fetchAndUpdateState(setIsError, setLoading, uiState, setUiState, setPestData, setImageList, fromDate, toDate) {
  setIsError(false)

  let fromDateString = moment(fromDate).format("DD MMM YYYY")
  let toDateString = moment(toDate).format("DD MMM YYYY")

  fetch(`/api/inferences?fetch_images=true&fromDate=${fromDateString}&toDate=${toDateString}`)
    .then(response => response.json())
    .then(resultData => {
      // some elements of the ui state needs to persist, so we remember to update it
      setUiState({
        ...uiState,
        ...resultData.uiState,
      })

      // pest data needs to processed to keys are dates
      setPestData(fixUpPestData(resultData.pestData, fromDate, toDate))

      // imageList gets completely replaced
      setImageList(resultData.imageList)
    })
    .catch(error => {
      console.log(error)
      setIsError(true)
    })
    .finally(() => {
      setLoading(false)
    })
}

function displyGraph(selectedGraph, pestData, fromDate, toDate) {
  if (selectedGraph === "PestTrendOverTime") {
    return <AnimalCountGraph
      key={selectedGraph}
      supportedPests={SUPPORTED_PESTS}
      pestColors={PEST_COLORS}
      pestData={pestData}
      minDate={fromDate}
      maxDate={toDate}
    />
  } else if (selectedGraph === "DailyBreakdown") {
    return <DailyBreakdownGraph
      key={selectedGraph}
      supportedPests={SUPPORTED_PESTS}
      pestColors={PEST_COLORS}
      pestData={pestData}
      minDate={fromDate}
      maxDate={toDate}
    />
  } else if (selectedGraph === "PestSightings") {
    return <PestSightings
      key={selectedGraph}
      supportedPests={SUPPORTED_PESTS}
      pestColors={PEST_COLORS}
      pestData={pestData}
      minDate={fromDate}
      maxDate={toDate}
    />
  } else {
    return ``
  }
}

export default () => {

  const [loading, setLoading] = useState(true)
  const [isError, setIsError] = useState(false)
  const [fromDate, setFromDate] = useState(moment(DEFAULT_UI_STATE.minFromDate))
  const [toDate, setToDate] = useState(moment().startOf('day'))
  const [selectedGraph, setSelectedGraph] = useState("PestTrendOverTime")

  const [uiState, setUiState] = useState(DEFAULT_UI_STATE)
  const [pestData, setPestData] = useState({})
  const [imageList, setImageList] = useState([])

  useEffect(() => {
    if (loading) {
      fetchAndUpdateState(setIsError, setLoading, uiState, setUiState, setPestData, setImageList, fromDate, toDate)
    }
  }, [isError, loading, uiState, pestData, imageList, fromDate, toDate])

  return (
    <Layout title="Garden Report">
      <section className="section has-background-primary">
        {isError ?
          <div className="notification is-danger">
            <button className="delete" onClick={() => setIsError(false)}></button>
            Error fetching data, try again later!
          </div>
          : ``
        }
        <FilterBar
          totalCount={uiState.totalCount}
          filteredCount={uiState.filteredCount}
          loading={loading}
          minFromDate={uiState.minFromDate}
          fromDate={fromDate}
          toDate={toDate}
          setLoading={setLoading}
          setFromDate={setFromDate}
          setToDate={setToDate}
        />
      </section>
      <section className="section">
        <div className="columns">
          <div className="column is-half">
            <div className="container">
              <div className="select is-fullwidth">
                <select defaultValue="PestTrendOverTime" onChange={(e) => setSelectedGraph(e.target.value)}>
                  <option value="PestTrendOverTime">Pests Trend over Time</option>
                  <option value="DailyBreakdown">Daily Breakdown</option>
                  <option value="PestSightings">Pest Sightings</option>
                </select>
              </div>
              {displyGraph(selectedGraph, pestData, fromDate, toDate)}
            </div>
          </div>
          <div className="column is-half">
            <section className="tile is-child">
              <PestTrendTable
                supportedPests={SUPPORTED_PESTS}
                pestData={pestData}
                maxDate={toDate}
              />
            </section>
          </div>
        </div>
        <div className="container">
          <ImageList images={imageList} />
        </div>
      </section>
    </Layout>
  )
}
