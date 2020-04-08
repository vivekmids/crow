import React from "react"
import { useStaticQuery, Link, graphql } from "gatsby"
import Img from "gatsby-image"

import Layout from "../components/layouts/default-layout"

const IndexPage = () => {
  const data = useStaticQuery(graphql`
    query {
      garden: file(relativePath: { eq: "brick-n-green-1459012.jpg" }) {
        publicURL
      }
      opportunity: file(relativePath: { eq: "opportunity.png" }) {
        childImageSharp {
          fluid(maxWidth: 1200) {
            ...GatsbyImageSharpFluid
          }
        }
      }
    }
  `)

  return (
    <Layout title="Home">
      <section className="hero is-large" style={{
        backgroundImage: `url('${data.garden.publicURL}')`,
        backgroundSize: `cover`,
      }}>
        <div className="hero-body">
            <div className="container has-text-centered">
              <h1 className="title is-1 has-text-grey-lighter">iCrow</h1>
              <br/>
              <h3 className="title is-3 has-text-grey-lighter">An AI powered solution to protect your home garden</h3>
              <h3 className="title is-3 has-text-grey-lighter">from animal pests</h3>
            </div>
        </div>
      </section>
      <section className="hero">
        <div className="hero-body">
          <div className="container">
            <Img fluid={data.opportunity.childImageSharp.fluid} />
          </div>
        </div>
      </section>
      <section className="hero is-primary is-medium is-info">
        <div className="hero-body">
          <div className="container has-text-centered">
            <div className="columns is-centered">
              <div className="column is-half">
                <p className="subtitle is-3 is-family-secondary">
                  iCrow provides a <strong>one stop solution</strong> to
                  protect your home garden from multiple animal
                  pests <strong>without chemicals, at a low cost,
                  requiring minimal maintenance</strong> and <strong>without
                  the commitment of owning a pet</strong>
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
      <section className="hero is-primary has-text-centered">
        <div className="hero-body">
          <div className="columns is-gapless">
            <div className="column">
              <Link to="/how_it_works"><h1 className="title">Learn about the product →</h1></Link>
            </div>
            <div className="column">
              <Link to="/members"><h1 className="title">Meet the team →</h1></Link>
            </div>
            <div className="column">
              <Link to="/garden_report"><h1 className="title">See our dashboard →</h1></Link>
            </div>
          </div>
        </div>
      </section>
    </Layout>
  )
}

export default IndexPage
