import React from "react"

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faLinkedinIn, faGithub } from "@fortawesome/free-brands-svg-icons"
import { createGlobalStyle } from "styled-components"

import Layout from "../components/layouts/default-layout"
import PhotoVivek from "../components/images/photo_vivek"
import PhotoTina from "../components/images/photo_tina"
import PhotoCatherine from "../components/images/photo_catherine"
import PhotoAditya from "../components/images/photo_aditya"

const GrayFontAwesomeStyle = createGlobalStyle`
  .gray-font-awesome-icon {
    color: gray;
  }
  .gray-font-awesome-icon:hover {
    color: black;
  }
`;

const MemberCard = ({ name, role, linkedInUsername, githubUsername, children }) => {
  return (
    <div className="card">
      <div className="card-image">
        <figure className="image">
          {children}
        </figure>
      </div>
      <div className="card-content has-text-centered">
        <p className="title is-4">{name}</p>
        <p className="title is-6">{role}</p>
      </div>
      <footer className="card-footer">
        {linkedInUsername != null
          ? <a href={`https://www.linkedin.com/in/${linkedInUsername}/`} className="card-footer-item gray-font-awesome-icon">
              <FontAwesomeIcon icon={faLinkedinIn} />
            </a>
          : ``
        }
        {githubUsername != null
          ? <a href={`https://www.github.com/${githubUsername}/`} className="card-footer-item gray-font-awesome-icon">
              <FontAwesomeIcon icon={faGithub} />
            </a>
          : ``
        }
      </footer>
    </div>
  );
}


const MembersPage = () => {
  return (
    <Layout title="Team">
      <GrayFontAwesomeStyle />
      <section className="hero is-fullheight">
        <div className="hero-body">
          <div className="container">
            <div className="columns">
              <div className="column">
                <MemberCard name="Vivek Agarwal" role="Product Manager" linkedInUsername="via">
                  <PhotoVivek />
                </MemberCard>
              </div>
              <div className="column">
                <MemberCard name="Catherine Cao" role="Data Scientist" linkedInUsername="catherinewcao">
                  <PhotoCatherine />
                </MemberCard>
              </div>
              <div className="column">
                <MemberCard name="Tina Agarwal" role="Data Engineer" linkedInUsername="tina-agarwal">
                  <PhotoTina />
                </MemberCard>
              </div>
              <div className="column">
                <MemberCard name="Aditya Dhara" role="Architect" linkedInUsername="adityadhara" githubUsername="ocamlmycaml">
                  <PhotoAditya />
                </MemberCard>
              </div>
            </div>
          </div>
        </div>
      </section>
    </Layout>
  );
}

export default MembersPage
