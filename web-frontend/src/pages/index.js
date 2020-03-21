import React from "react"
import { Link } from "gatsby"

import Layout from "../components/layout"
import Squirrel from "../components/images/squirrel"
import SEO from "../components/seo"

const IndexPage = () => (
  <Layout>
    <SEO title="Home" />
    <div style={{maxWidth: `300px`, marginBottom: `1.45rem`}} >
      <div>
        <Squirrel />
        <div>
          A smarter way to save your farms from pests
        </div>
      </div>
      <div>
        <h1>Leveraging AI</h1>
        <h3>For</h3>
        <h1>non-chemical</h1>
        <h3>and</h3>
        <h1>non-invasive</h1>
        <h3>methods to</h3>
        <h1>deter farm pests</h1>
      </div>
    </div>
  </Layout>
)

export default IndexPage
