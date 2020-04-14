import React, { useState, useEffect } from "react"
import { Link, graphql } from "gatsby"
import Img from "gatsby-image"

import Layout from "../components/layouts/default-layout"

function fetchAndUpdateState(selectedImage, shouldSaveToCloud, setLoading, setIsError, setInferenceData) {
  if (!selectedImage) {
    setLoading(false)
    return
  }

  setIsError(false)

  fetch(`/simulator/process-image?image_id=${selectedImage}&save_to_cloud=${shouldSaveToCloud}`)
    .then(response => response.json())
    .then(resultData => {
      setInferenceData(resultData)
    })
    .catch(error => {
      console.log(error)
      setIsError(true)
    })
    .finally(() => {
      setLoading(false)
    })
}


function displayInferenceDataOrInfo(inferenceData) {
  if (inferenceData.inference_response) {
    return (
      <>
        <p>Inference Results:</p>
        <code>
          {JSON.stringify(inferenceData.inference_response, null, 2)}
        </code>
        <p>Deterrent Deployed:</p>
        <code>
          {JSON.stringify(inferenceData.deterrent_response, null, 2)}
        </code>
      </>
    )
  } else {
    return (
      <p>
        This simulates the device you might place in your garden.
        Select an image, and it will be sent to the simulator for inference and creating sounds
      </p>
    )
  }
}

const ImageTile = ({ node, selectedImage, setSelectedImage, setLoading }) => {
  const index = node.name.replace("pest-", "")
  const colorScheme = `${selectedImage === index ? "is-warning" : "is-danger"}`

  return (
    <article className={`tile is-child notification ${colorScheme}`}>
      <a href="#" onClick={() => {
        setLoading(true)
        setSelectedImage(index)
      }}>
        <Img fluid={node.childImageSharp.fluid} />
      </a>
    </article>
  )
}


export default ({ data }) => {

  const [loading, setLoading] = useState(false)
  const [isError, setIsError] = useState(false)

  const [selectedImage, setSelectedImage] = useState(null)
  const [shouldSaveToCloud, setShouldSaveToCloud] = useState(false)

  const [inferenceData, setInferenceData] = useState({})

  useEffect(() => {
    if (loading) {
      fetchAndUpdateState(
        selectedImage,
        shouldSaveToCloud,
        setLoading,
        setIsError,
        setInferenceData,
      )
    }
  }, [selectedImage, shouldSaveToCloud, loading])

  return (
    <Layout title="Device Simulator">
      {isError ?
        <div className="notification is-danger">
          <button className="delete" onClick={() => setIsError(false)}></button>
          Error fetching data, try again later!
        </div>
        : ``
      }
      <section className="section">
        <div className="container">
          <h3 className="title is-3">Device simulator</h3>
        </div>
        <div className="container">
          <div className="tile is-ancestor">
            <div className="tile is-4">
              <div className="tile is-parent is-vertical">
                <div className="tile is-child notification is-primary">
                  <div className="field is-grouped is-grouped-centered">
                    <p className="control">
                      <button className={`button ` + (loading ? `is-loading` : ``)} onClick={() => setLoading(true)}>
                        Retry
                      </button>
                    </p>
                    <p className="control">
                      <label className="checkbox">
                        <input type="checkbox" onChange={(e) => setShouldSaveToCloud(e.target.checked)} />
                        Save to dashboard
                      </label>
                    </p>
                  </div>
                  <div className="container">
                    { shouldSaveToCloud
                      ? <p>See results sent to our <Link to="/garden_report">Garden Report page</Link></p>
                      : ``
                    }
                    {displayInferenceDataOrInfo(inferenceData)}
                  </div>
                </div>
              </div>
            </div>
            {[0, 4, 8, 12].map((start_index) => (
              <div key={`starting-index-${start_index}`} className="tile is-vertical is-2">
                <div className="tile is-parent is-vertical">
                  {data.allFile.nodes.slice(start_index, start_index + 4).map((node) => (
                    <ImageTile
                      key={node.name}
                      node={node}
                      selectedImage={selectedImage}
                      setSelectedImage={setSelectedImage}
                      setLoading={setLoading}
                    />
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </Layout>
  )
}


export const query = graphql`
query {
  allFile(filter: {relativeDirectory: {eq: "sample_pests"}}) {
    nodes {
      name
      childImageSharp {
        fluid(maxWidth: 300, maxHeight: 300) {
          ...GatsbyImageSharpFluid
        }
      }
    }
  }
}
`