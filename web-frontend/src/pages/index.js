import React from "react"

import Layout from "../components/layouts/default-layout"
import Squirrel from "../components/images/squirrel"

const IndexPage = () => (
  <Layout title="Home">
    <div className="container">
      <section className="hero">
        <div className="hero-body">
          <div className="container">
            <div className="columns">
              <div className="column">
                <Squirrel />
              </div>
              <div className="column">
                <h1 className="title is-2">Leveraging AI</h1>
                <h3 className="title is-4">For</h3>
                <h1 className="title is-2">non-chemical</h1>
                <h3 className="title is-4">and</h3>
                <h1 className="title is-2">non-invasive</h1>
                <h3 className="title is-4">methods to</h3>
                <h1 className="title is-2">deter farm pests</h1>
              </div>
            </div>
          </div>
          <div className="container">
            <h3 className="title is-3">A smarter way to deter garden pests</h3>
          </div>
        </div>
      </section>
    </div>
  </Layout>
)

export default IndexPage
