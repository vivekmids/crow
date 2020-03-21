import { Link } from "gatsby"
import PropTypes from "prop-types"
import React from "react"

import ScarecrowLogo from "./images/scarecrow_logo"

const Header = ({ siteTitle }) => {

  return <header
    style={{
      background: `rebeccapurple`,
      marginBottom: `1.45rem`,
    }}
  >
    <div
      style={{
        margin: `0 auto`,
        maxWidth: 960,
        padding: `1.45rem 1.0875rem`,
      }}
    >
      <Link
        to="/"
        style={{
          color: `white`,
          textDecoration: `none`,
        }}
      >
        <ScarecrowLogo style={{ float: `left`, marginRight: `10px` }} />
        <h1 style={{ margin: 0 }}>
            {siteTitle}
        </h1>
      </Link>
      <Link to="/">Home</Link>
      <Link to="/members/">Members</Link>
      <Link to="/how_it_works/">How It Works</Link>
      <Link to="/farm_report/">Farm Report</Link>
    </div>
  </header>
}

Header.propTypes = {
  siteTitle: PropTypes.string,
}

Header.defaultProps = {
  siteTitle: ``,
}

export default Header
