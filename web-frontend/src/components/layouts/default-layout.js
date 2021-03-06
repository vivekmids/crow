/**
 * Layout component that queries for data
 * with Gatsby's useStaticQuery component
 *
 * See: https://www.gatsbyjs.org/docs/use-static-query/
 */

import React from "react"
import PropTypes from "prop-types"
import { useStaticQuery, graphql, Link } from "gatsby"

import Header from "./header"
import SEO from "./seo"
import "./default-layout.scss"

const Layout = ({ title, children }) => {
  const data = useStaticQuery(graphql`
    query SiteTitleQuery {
      site {
        siteMetadata {
          title
        }
      }
    }
  `)

  return (
    <>
      <SEO title={title} />
      <Header siteTitle={data.site.siteMetadata.title} />
      <main>
        {children}
      </main>
      <footer className="footer">
        <div className="content has-text-centered">
          <p>
            <Link to="/" activeClassName="is-activate">Home</Link>{` | `}
            <Link activeClassName="is-active" to="/team/">Team</Link>{` | `}
            <Link activeClassName="is-active" to="/how_it_works/">How It Works</Link>{` | `}
            <Link activeClassName="is-active" to="/garden_report/">Garden Report</Link>
          </p>
          <p>
            Scarecrow © {new Date().getFullYear()}, Built with
            {` `}
            <a href="https://www.gatsbyjs.org">Gatsby</a>
          </p>
          <p>
            Homepage photo credits to <a href="/photographer/pixelbox-31234">Wolf Friedmann</a> from <a href="https://freeimages.com/">FreeImages</a>
          </p>
        </div>
      </footer>
    </>
  )
}

Layout.propTypes = {
  children: PropTypes.node.isRequired,
}

export default Layout
