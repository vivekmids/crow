import { Link } from "gatsby"
import PropTypes from "prop-types"
import React, { useState } from "react"
import styled from "styled-components"

import ScarecrowLogo from "../images/scarecrow_logo"

const HamburgerButton = styled.button`
  &, &:hover, &:active {
    background: inherit;
    border: inherit;
  }
`

const Header = ({ siteTitle }) => {

  const [hamburgerExpanded, setHamburger] = useState(false);

  return <header>
    <nav className="navbar" role="navigation" aria-label="main navigation">
      <div className="navbar-brand">
        <Link className="navbar-item" to="/">
          <figure className="image">
            <ScarecrowLogo />
          </figure>
        </Link>

        <HamburgerButton className="navbar-burger burger" aria-label="menu" aria-expanded="false"
            onClick={() => setHamburger(!hamburgerExpanded)}>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </HamburgerButton>
      </div>

      <div className={`navbar-menu${ hamburgerExpanded ? " is-active" : ""}`}>
        <div className="navbar-start">
          <Link className="navbar-item" activeClassName="is-active" to="/">
            Home
          </Link>
          <Link className="navbar-item" activeClassName="is-active" to="/members/">
            Members
          </Link>
          <Link className="navbar-item" activeClassName="is-active" to="/how_it_works/">
            How It Works
          </Link>
          <Link className="navbar-item" activeClassName="is-active" to="/farm_report/">
            Farm Report
          </Link>
        </div>
      </div>

    </nav>
  </header>
}

Header.propTypes = {
  siteTitle: PropTypes.string,
}

Header.defaultProps = {
  siteTitle: ``,
}

export default Header
