import React, { useState } from "react"
import moment from "moment"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faCheckCircle, faTimesCircle } from "@fortawesome/free-regular-svg-icons"


function parseSoundUsed(fileName) {
  const splits = fileName.split("/")
  return splits[splits.length - 2]
}

function chunked(arr, chunk_size) {
  let chunked = []
  for (let i = 0; i < arr.length; i += chunk_size) {
    chunked.push({
      key: `chunk${i}`,
      images: arr.slice(i, i + chunk_size)
    })
  }
  return chunked
}

const ImageCard = ({
  cam_id,
  device_id,
  date_time,
  base64_encoded_image,
  detected_animals,
  deterrent_type,
  soundfile_name,
}) => {
  const [feedback, setFeedback] = useState(0)

  return (
    <div className={`column`}>
      <article className="media box">
        <figure className="media-left">
          <p className="image is-128x128">
            <img src={`data:image/jpeg;base64,${base64_encoded_image}`} alt={date_time} />
          </p>
        </figure>
        <div className="media-content">
          <div className="content">
            <p>
              Detected: <em>{detected_animals}</em><br />
              Deterrent Used: {deterrent_type}<br />
              Device: {device_id} -- {cam_id}<br />
              Date: {moment(date_time).format("YYYY-MM-DD HH:MM")}<br />
              { deterrent_type === 'sound'
              ? `Sound Used: ${parseSoundUsed(soundfile_name)}`
              : ``}
            </p>
          </div>
        </div>
        <div className="media-right">
          <p>Is this correct?</p>
          <div className="field has-addons">
            <p className="control">
              <button className="button" onClick={() => setFeedback(1)} disabled={feedback === 1}>
                <FontAwesomeIcon icon={faCheckCircle} />
              </button>
            </p>
            <p className="control">
              <button className="button is-danger" onClick={() => setFeedback(-1)} disabled={feedback === -1}>
                <FontAwesomeIcon icon={faTimesCircle} />
              </button>
            </p>
          </div>
        </div>
      </article>
    </div>
  )
}

export default ({ images }) => {
  return (
    <div className="container">
      {chunked(images, 2).map(({ key, images}) => (
        <div key={key} className="columns">
          {images.map((image) => <ImageCard key={image.rowid} {...image} />)}
        </div>
      ))}
    </div>
  )
}