import React, { useState } from 'react'

import Layout from "../components/layouts/default-layout"
import ImageList from '../components/image_list'
import AnimalCountGraph from "../components/graphs/animal_counts"
import fetch from "node-fetch"

const DEFAULT_DATA = {
  "images": [],
  "animal_counts": {
    "bird": 0,
    "bobcat": 0,
    "cat": 0,
    "deer": 0,
    "dog": 0,
    "opossumother": 0,
    "rabbit": 0,
    "raccoon": 0,
    "rodent": 0,
    "skunk": 0,
  },
  "summary_stats": {
    "count_light_deployed": 0,
    "count_sound_deployed": 0,
    "max_date_time": null,
    "min_date_time": null,
    "num_distinct_animals": 0,
    "total_count": 0,
  },
}

function fetchAndUpdateState(setGardenData, setIsError) {
  setIsError(false)

  fetch(`/api/inferences?fetch_images=true`)
    .then(response => response.json())
    .then(resultData => {
      setGardenData(resultData)
    })
    .catch(error => {
      console.log(error)
      setIsError(true)
    })
}

export default () => {

  const [loading, setLaoding] = useState(true)
  const [isError, setIsError] = useState(false)
  const [gardenData, setGardenData] = useState(DEFAULT_DATA)

  if (loading) {
    fetchAndUpdateState(setGardenData, setIsError)
    setLaoding(false)

    console.log(gardenData)
  }

  return (
    <Layout title="Garden Report">
      <section className="section">
        <div className="container">

        </div>
        <div className="container">
          <div className="columns">
            <div className="column is-half">
              <AnimalCountGraph animal_counts={gardenData.animal_counts} />
            </div>
            <div className="column is-half">
              <ImageList images={gardenData.images} />
            </div>
          </div>
        </div>
      </section>
    </Layout>
  )
}
