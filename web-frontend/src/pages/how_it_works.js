import React from "react"
import { Link, useStaticQuery, graphql } from "gatsby"
import Img from "gatsby-image"

import Layout from "../components/layouts/default-layout"

const HowItWorkspage = () => {
  const data = useStaticQuery(graphql`
    query {
      edgeArchDiagram: file(relativePath: { eq: "edge-arch-diagram.png" }) {
        childImageSharp {
          fluid(maxWidth: 1200) {
            ...GatsbyImageSharpFluid
          }
        }
      }
      modelArchDiagram: file(relativePath: { eq: "model-arch-diagram.png" }) {
        childImageSharp {
          fluid(maxWidth: 1200) {
            ...GatsbyImageSharpFluid
          }
        }
      }
      webArchDiagram: file(relativePath: { eq: "web-arch-diagram.png" }) {
        childImageSharp {
          fluid(maxWidth: 1200) {
            ...GatsbyImageSharpFluid
          }
        }
      }
      conceptualDiagram: file(relativePath: { eq: "conceptual-diagram.png" }) {
        childImageSharp {
          fluid(maxWidth: 1200) {
            ...GatsbyImageSharpFluid
          }
        }
      }
    }
  `)

  return (
    <Layout title="How it works">
      <section className="hero">
        <div className="hero-body is-large">
          <h1 className="title is-1">Enter iCrow</h1>
          <div className="columns is-vcentered">
            <div className="column is-two-thirds">
              <Img fluid={data.conceptualDiagram.childImageSharp.fluid} />
            </div>
            <div className="column">
              <p className="is-size-4">
                iCrow is an edge device with cameras watching over your garden.
                Once a pest is identified, the device will play a loud sound of its natural predator during
                the day and turn on a flashing light during the night to scare it away. You can then monitor
                the pests found and deterred using our <Link to="/garden_report">garden report</Link>
              </p>
            </div>
          </div>
        </div>
      </section>
      <section className="hero is-info">
        <div className="hero-body">
          <h1 className="title is-1">Modular edge device software</h1>
          <div className="columns is-centered">
            <div className="column is-half">
              <Img fluid={data.edgeArchDiagram.childImageSharp.fluid} />
            </div>
          </div>
        </div>
      </section>
      <section className="hero is-primary">
        <div className="hero-body">
          <h1 className="title is-1">Inception V3 for image detection</h1>
          <div className="columns is-vcentered">
            <div className="column is-two-thirds">
              <Img fluid={data.modelArchDiagram.childImageSharp.fluid} />
            </div>
            <div className="column">
              <p className="is-size-4">
                The model we use for image recognition is based on the InceptionV3 model. We selected the InceptionV3 because
                it is one of the more powerful models out there. It uses inception to add more depth to the architecture,
                but also limit the amount of trainable parameters. We use the model architecture up until the dense layers,
                as shown in the first box, and attach our own dense and softmax layers to it. We freeze the weights
                in the old body, and only train the new dense layers.
              </p>
            </div>
          </div>
        </div>
      </section>
      <section className="hero is-info">
        <div className="hero-body">
          <h1 className="title is-1">Web interface for monitoring</h1>
          <div className="columns is-vcentered">
            <div className="column">
              <p className="is-size-4">
                We then save all images of your pests that we detected in the cloud. We use a postgres database to store
                all the details of our detection, and s3 to store the actual images captured. We also provide simple
                analytical tools to inspect the kinds of animals that haunt your garden. This can help you improve your
                security, and also give you a chance to provide feedback about whether our system is correct or not
              </p>
            </div>
            <div className="column is-two-thirds">
              <Img fluid={data.webArchDiagram.childImageSharp.fluid} />
            </div>
          </div>
        </div>
      </section>
    </Layout>
  )
}

export default HowItWorkspage
