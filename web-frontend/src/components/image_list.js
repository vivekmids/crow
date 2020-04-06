import React from "react"
import moment from "moment"


function parseSoundUsed(fileName) {
  const splits = fileName.split("/")
  return splits[splits.length - 2]
}

const ImageCard = ({
  cam_id,
  device_id,
  date_time,
  base64_encoded_image,
  detected_animals,
  deterrent_type,
  soundfile_name,
}) => (
  <div className="box">
    <article className="media">
      <figure className="media-left">
        <p className="image is-128x128">
          <img src={`data:image/jpeg;base64,${base64_encoded_image}`} alt={date_time} />
        </p>
      </figure>
      <div className="media-content">
        <div className="content">
          <p>Detected: <em>{detected_animals}</em></p>
          <p>Deterrent Used: {deterrent_type}</p>
          <p>Device: {device_id} -- {cam_id}</p>
          <p>Date: {moment(date_time).format("YYYY-MM-DD HH:MM")}</p>
          { deterrent_type === 'sound'
            ? <p>Sound Used: {parseSoundUsed(soundfile_name)}</p>
            : ``}
        </div>
      </div>
    </article>
  </div>
)

export default ({ images }) => (
  <div className="container">
    {images.map(image => <ImageCard key={image.rowid} {...image} />)}
  </div>
)