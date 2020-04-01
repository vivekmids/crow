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
      <footer class="footer">
        <div className="content has-text-centered">
          <p>
            <Link to="/" activeClassName="is-activate">Home</Link>{` | `}
            <Link activeClassName="is-active" to="/members/">Members</Link>{` | `}
            <Link activeClassName="is-active" to="/how_it_works/">How It Works</Link>{` | `}
            <Link activeClassName="is-active" to="/farm_report/">Farm Report</Link>
          </p>
          <p>
            Scarecrow © {new Date().getFullYear()}, Built with
            {` `}
            <a href="https://www.gatsbyjs.org">Gatsby</a>
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
