import React from "react"

import Layout from "../components/layouts/default-layout"
import PhotoVivek from "../components/images/photo_vivek"
import PhotoTina from "../components/images/photo_tina"
import PhotoCatherine from "../components/images/photo_catherine"
import PhotoAditya from "../components/images/photo_aditya"


const MemberCard = ({ name, role, children }) => {
  return (
    <div className="card">
      <div className="card-image">
        <figure className="image is-square">
          {children}
        </figure>
      </div>
      <div className="card-content">
        <p className="title is-4">{name}</p>
        <p className="title is-6">{role}</p>
      </div>
      <footer className="card-footer">
        <a href="#" className="card-footer-item">LinkedIn</a>
        <a href="#" className="card-footer-item">Whatev</a>
      </footer>
    </div>
  );
}


const MembersPage = () => {
  return (
    <Layout title="Members">
      <section className="hero is-fullheight">
        <div className="hero-body">
          <div className="container">
            <div className="columns">
              <div className="column">
                <MemberCard name="Vivek Agarwal" role="Product Manager">
                  <PhotoVivek />
                </MemberCard>
              </div>
              <div className="column">
                <MemberCard name="Catherine Cao" role="Data Scientist">
                  <PhotoCatherine />
                </MemberCard>
              </div>
              <div className="column">
                <MemberCard name="Tina Agarwal" role="Data Engineer">
                  <PhotoTina />
                </MemberCard>
              </div>
              <div className="column">
                <MemberCard name="Aditya Dhara" role="Architect">
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
