import React, { useState, useEffect } from "react"

import Layout from "../components/layouts/default-layout"

const FarmReport = () => {

  const [cloudData, setCloudData] = useState({
    images: [],
    summary: {
      animal_counts: {
        bird: 1,
        rabbit: 2
      },
      summary_stats: {
        count_light_deployed: 24,
        count_sound_deployed: 24,
        max_date_time: "Tue, 31 Mar 2020 14:43:26 GMT",
        min_date_time: "Tue, 31 Mar 2020 00:11:28 GMT",
        num_distinct_animals: 10,
        total_count: 24,
      }
    }
  })

  useEffect(() => {
    fetch(`/api/inferences?rows=1`)
      .then(response => response.json())
      .then(resultData => {
        setCloudData(resultData)
      })
  }, [])

  return (
    <Layout title="Farm Report">
      <section className="section">
        <div className="container">
          <p>{JSON.stringify(cloudData)}</p>
        </div>
      </section>
    </Layout>
  )
}

export default FarmReport
